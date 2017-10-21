# -*- coding: utf-8 -*-
import re
import scrapy
import psycopg2


class VanguardSpider(scrapy.Spider):
    name = 'vanguard'
    start_urls = ["https://www.vanguardngr.com/"]

    def parse(self, response):
        self.conn = psycopg2.connect(host="ec2-50-17-203-195.compute-1.amazonaws.com",database="d9riaveq1q5ftr",
            user="fpljfaqsijcukq", password="3bf3d10b8b15fcccf8fc49b2a127020c638c40ddb718445567a0381b8429c37b")
        self.cur = self.conn.cursor()
        for header in response.css("span.rtp-latest-news-title"):

            link = header.css("a::attr(href)").extract_first()
            post_detail = {
                'link': response.urljoin(link),
                'title': header.css("a::text").extract_first()
            }
            regex = re.compile(r"\d+/\d+")
            found = regex.search(post_detail['link'])
            found = found.group()
            year, month = found.split("/")
            date = '-'.join([year, month])
            title = post_detail['title']
            self.cur.execute("INSERT INTO updateinfo_newsitem (url, title, site_id, date) VALUES(%s, %s, %s, %s);", [post_detail['link'], post_detail['title'], 8, date])
                    
            self.conn.commit()
        self.cur.execute("""DELETE FROM updateinfo_newsitem a USING (
                            SELECT MIN(ctid) as ctid, title
                            FROM updateinfo_newsitem 
                            GROUP BY title HAVING COUNT(*) > 1
                            ) b
                            WHERE a.title = b.title 
                            AND a.ctid <> b.ctid""")
        self.conn.commit()
