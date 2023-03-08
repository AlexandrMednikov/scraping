from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from spiders.InstagramUserFollows import instagram_parser_Spider
import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(instagram_parser_Spider)

    process.start()
