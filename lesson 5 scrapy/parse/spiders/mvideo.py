import random

import scrapy
from scrapy.http import HtmlResponse
from parse.items import ParseItem
import json


class MvideoSpider(scrapy.Spider):
    name = "mvideo"
    allowed_domains = ["mvideo.ru"]
    start_urls = ["https://www.mvideo.ru/promo/hity-prodazh-mark134112626"]

    def parse(self, response=HtmlResponse):
        next_page = 'https://www.mvideo.ru'+response.xpath('//a[contains(@class, "c-pagination__next font-icon icon-up ")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        product_card = response.xpath("//a[contains(@class, 'fl-product-tile-title__link sel-product-tile-title')]/@data-product-info").getall()
        for item in product_card:
            item = json.loads(item)
            yield ParseItem(name=item["productName"], price=float(item["productPriceLocal"]), category=item["productCategoryName"])
