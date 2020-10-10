import os
import jsonlines
import logging

from itemadapter import ItemAdapter

import discord_msgs as dsc


class DiscordSenderPipeline:

    def __init__(self):
        self.save_promo_to_file = False
        self.first_run = False
        self.promo_dicts = []
        self.promo_dict = {}
        self.filename = './promos_scraped.jl'

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
        send_promo = True
        self.promo_dict = ItemAdapter(item).asdict()

        #if promo was scraped before discard it
        with jsonlines.open('promos_scraped.jl') as reader:
            for obj in reader:
                if self.promo_dict['promo_id'] == obj['promo_id']:
                    send_promo = False

        if send_promo:
            self.save_promo_to_file = True
            self.promo_dicts.append(self.promo_dict)
            if not self.first_run:
                dsc.send_promo_msg(self.dsc_webhook, self.promo_dict)

        return item

