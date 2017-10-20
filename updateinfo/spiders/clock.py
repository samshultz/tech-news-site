import future
import hacker
import techcrunch
from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy.crawler import CrawlerProcess


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=60)
def timed_job():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(future.BBCFutureSpider)
    process.crawl(hacker.HackerNewsSpider)
    process.crawl(techcrunch.TechCrunchSpider)
    process.start()

sched.start()
