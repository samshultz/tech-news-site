import schedule
import time
import future
import hacker
import techcrunch
from scrapy.crawler import CrawlerProcess

def job():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(future.BBCFutureSpider)
    process.crawl(hacker.HackerNewsSpider)
    process.crawl(techcrunch.TechCrunchSpider)
    process.start()


schedule.every().day.at("6:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)