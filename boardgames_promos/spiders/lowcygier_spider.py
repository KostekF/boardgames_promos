import os
import scrapy


class PepperSpider(scrapy.Spider):
    name = 'lowcygier_promos'

    if os.environ.get('LOWCYGIER_ADDR') is None:
        start_urls = ['https://lowcygier.pl/gry-planszowe/']
    else:
        start_urls = [os.environ.get('LOWCYGIER_ADDR')]

    def parse(self, response):
        for promo_block in response.css('main article'):
            promo_id = 'PROMO-' + promo_block.css('time.timeago::attr(datetime)').get()
            price = promo_block.css('h2.post-title a::text').re_first(
                r'[0-9]+(?:,[0-9]+)?\040?zł')
            if price is not None:
                price = price.strip().replace(' ', '')
            title = promo_block.css('h2.post-title a::text').get()
            if title is not None:
                title = title.strip()
            promo_link = promo_block.css('h2.post-title a::attr(href)').get()
            short_descr = promo_block.css('div.text-wrapper.lead-wrapper p::text').get()
            if short_descr is not None:
                short_descr = short_descr.strip()

            if promo_id is not None:
                yield {
                    'promo_id': promo_id,
                    'price': price,
                    'title': title,
                    'promo_link': promo_link,
                    'short_descr': short_descr,
                }

