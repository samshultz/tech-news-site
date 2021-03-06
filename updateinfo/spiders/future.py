# -*- coding: utf-8 -*-
import re
import scrapy
# from updateinfo.models import NewsItem
import psycopg2



class BBCFutureSpider(scrapy.Spider):
    name = "BBC Future"
    start_urls = ['http://www.bbc.com/future']

    def parse(self, response):
        site="BBCFuture"
        self.conn = psycopg2.connect(host="ec2-50-17-203-195.compute-1.amazonaws.com",database="d9riaveq1q5ftr",
            user="fpljfaqsijcukq", password="3bf3d10b8b15fcccf8fc49b2a127020c638c40ddb718445567a0381b8429c37b")
        self.cur = self.conn.cursor()
        for header in response.css("div.promo-unit-header"):

            link = header.css("a[data-cs-element-type=story-promo-link]::attr(href)").extract_first()
            a = {
                'link': response.urljoin(link),
                'title': header.css("a[data-cs-element-type=story-promo-link] h3.promo-unit-title::text").extract_first()
            }
            regex = re.compile(r'\d{8}')
            found = regex.search(link).group()
            year, month, day = found[:4], found[4:6], found[6:]
            date = '-'.join([year, month, day])
            # NewsItem.objects.create(url=a['link'], title=a['title'], site="BBCFuture", date=date)
            self.cur.execute("INSERT INTO updateinfo_newsitem (url, title, site_id, date) VALUES(%s, %s, %s, %s);", [a['link'], a['title'], 5, date])
            
            self.conn.commit()            
        self.cur.execute("""DELETE FROM updateinfo_newsitem a USING (
                            SELECT MIN(ctid) as ctid, title
                            FROM updateinfo_newsitem 
                            GROUP BY title HAVING COUNT(*) > 1
                            ) b
                            WHERE a.title = b.title 
                            AND a.ctid <> b.ctid""")
        self.conn.commit()