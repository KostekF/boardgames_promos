from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    scheduler = TwistedScheduler()
    scheduler.add_job(process.crawl, 'interval', args=['pepper_promos'], seconds=60)
    scheduler.start()
    process.start(False)

