# -*- coding: utf-8 -*-
import scrapy
import psycopg2


class VanguardSpider(scrapy.Spider):
    name = 'vanguard'
    start_urls = ["https://www.vanguardngr.com/"]

    def parse(self, response):
        self.conn = psycopg2.connect(host="localhost",database="scrape",
            user="postgres", password="reductionism==12345")
        self.cur = self.conn.cursor()
        for header in response.css("span.rtp-latest-news-title"):

            link = header.css("a::attr(href)").extract_first()
            a = {
                'link': response.urljoin(link),
                'title': header.css("a::text").extract_first()
            }
            self.cur.execute("INSERT INTO scraped_data (links, title) VALUES(%s, %s);", [a['link'], a['title']])
            
            self.conn.commit()
