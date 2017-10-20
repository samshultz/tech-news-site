# -*- coding: utf-8 -*-
import re
import scrapy
import psycopg2

class TechCrunchSpider(scrapy.Spider):
    name = 'techcrunch'
    start_urls = ["https://www.techcrunch.com"]

    def parse(self, response):
        site = "Tech Crunch"

        self.conn = psycopg2.connect(host="localhost",database="info",
            user="postgres", password="reductionism==12345")
        self.cur = self.conn.cursor()
        for header in response.css("h2.post-title"):

            post_detail = {
                'link': header.css("a::attr(href)").extract_first(),
                'title': header.css("a::text").extract_first()
            }
            if post_detail['link'] != None:
                regex = re.compile(r"\d+/\d+/\d+")
                found = regex.search(post_detail['link'])
                if found:
                    found = found.group()
                    year, month, day = found.split("/")
                    date = '-'.join([year, month, day])
                    title = post_detail['title']
                
                    self.cur.execute("INSERT INTO updateinfo_newsitem (url, title, site_id, date) VALUES(%s, %s, %s, %s);", [post_detail['link'], post_detail['title'], 2, date])
                    
                    self.conn.commit()
        self.cur.execute("""DELETE FROM updateinfo_newsitem a USING (
                            SELECT MIN(ctid) as ctid, title
                            FROM updateinfo_newsitem 
                            GROUP BY title HAVING COUNT(*) > 1
                            ) b
                            WHERE a.title = b.title 
                            AND a.ctid <> b.ctid""")
        self.conn.commit()