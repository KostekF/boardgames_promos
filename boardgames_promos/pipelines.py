import os
import jsonlines
import logging

from itemadapter import ItemAdapter

import discord_msgs as dsc
import settings_offers


class DiscordSenderPipeline:
    def __init__(self):
        self.save_promo_to_file = False
        self.first_run = False
        self.promo_dicts = []
        self.promo_dict = {}
        self.filename = './promos_scraped.jl'

        self.words_blacklist = settings_offers.words_blacklist
        self.price_range = settings_offers.price_range

        if os.environ.get('DSC_WEBHOOK') is None:
            import config
            self.dsc_webhook = config.dsc_webhook
        else:
            self.dsc_webhook = os.environ.get('DSC_WEBHOOK')

    def open_spider(self, spider):
        if not os.path.isfile(self.filename):
            logging.info("File does not exists, creating empty file.")
            self.first_run = True
            open(self.filename, 'w').close()
        elif os.stat(self.filename).st_size == 0:
            self.first_run = True

    def close_spider(self, spider):
        if self.save_promo_to_file:
            with jsonlines.open('promos_scraped.jl', mode='a') as writer:
                for promo in self.promo_dicts:
                    writer.write(promo)

    def process_item(self, item, spider):
        promo_first_seen = True
        send_promo = True
        self.promo_dict = ItemAdapter(item).asdict()

        #if promo was scraped before - discard it
        with jsonlines.open('promos_scraped.jl') as reader:
            for obj in reader:
                if self.promo_dict['promo_id'] == obj['promo_id']:
                    promo_first_seen = False

        #if promo contains blacklisted word - discard it
        for word in self.words_blacklist:
            if word in self.promo_dict['title'].lower():
                send_promo = False

        #if promo price is not in min<price<max and price is not None - discard it
        if self.promo_dict['price'] is not None:
            promo_price = float(self.promo_dict['price'][:-2].replace(',', '.'))
            if not (self.price_range['min'] < promo_price < self.price_range['max']):
                send_promo = False

        if promo_first_seen:
            self.save_promo_to_file = True
            self.promo_dicts.append(self.promo_dict)

            if send_promo and not self.first_run:
                dsc.send_promo_msg(self.dsc_webhook, self.promo_dict)

        return item

