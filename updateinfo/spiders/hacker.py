# -*- coding: utf-8 -*-
import scrapy
import psycopg2

class HackerNewsSpider(scrapy.Spider):
    name = 'HN'
    start_urls = ["https://www.thehackernews.com"]

    def parse(self, response):
        site="Hacker News"
        self.conn = psycopg2.connect(host="localhost",database="info",
            user="postgres", password="reductionism==12345")
        self.cur = self.conn.cursor()
        for header in response.css("article.post"):

            a = {
                'link': header.css("h2.post-title a::attr(href)").extract_first(),
                'title': header.css("h2.post-title a::text").extract_first(),
                'date': header.css("span.updated::text").extract_first()
            }
            self.cur.execute("INSERT INTO updateinfo_newsitem (url, title, site_id, date) VALUES(%s, %s, %s, %s);", [a['link'], a['title'], 3, a['date'].split("T")[0]])
            
            self.conn.commit()
        self.cur.execute("""DELETE FROM updateinfo_newsitem a USING (
                            SELECT MIN(ctid) as ctid, title
                            FROM updateinfo_newsitem 
                            GROUP BY title HAVING COUNT(*) > 1
                            ) b
                            WHERE a.title = b.title 
                            AND a.ctid <> b.ctid""")
        self.conn.commit()