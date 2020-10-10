import os
import scrapy


class PepperSpider(scrapy.Spider):
    name = 'pepper_promos'

    if os.environ.get('PEPPER_ADDR') is None:
        start_urls = ['https://www.pepper.pl/grupa/gry-bez-pradu']
    else:
        start_urls = [os.environ.get('PEPPER_ADDR')]

    def parse(self, response):
        for promo_block in response.css('#toc-target-deals article'):
            promo_id = promo_block.css('article::attr(id)').get()
            price = promo_block.css('span.thread-price::text').get()
            if price is not None:
                price = price.strip()
            title_block = promo_block.css('strong.thread-title')
            title = title_block.css('a::attr(title)').get()
            if title is not None:
                title = title.strip()
            promo_link = title_block.css('a::attr(href)').get()
            short_descr = promo_block.css('div.cept-description-container::text').get()
            if short_descr is not None:
                short_descr = short_descr.strip()
            #time = promo_block.css('span.hide--toBigCards1::text').re(r'(([0-9]*) g, )?([0-9]* min)?')
            if promo_id is not None:
                yield {
                    'promo_id': promo_id,
                    'price': price,
                    'title': title,
                    'promo_link': promo_link,
                    'short_descr': short_descr,
                }

