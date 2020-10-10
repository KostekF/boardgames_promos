import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    scheduler = TwistedScheduler()
    if os.environ.get('INTERVAL_SECS') is None:
        interval_secs = 20
    else:
        interval_secs = os.environ.get('INTERVAL_SECS')
    scheduler.add_job(process.crawl, 'interval', args=['pepper_promos'], seconds=interval_secs)
    scheduler.start()
    process.start(False)

