import requests
import json


def send_promo_msg(webhookurl, promo_dict, *, bot_name='PromoOffersBOT'):
    redacted_message = ''
    embed = {}
    embed['title'] = promo_dict['title']
    redacted_message += promo_dict['title'] + '\n'
    redacted_message += promo_dict['price'] + '\n'
    redacted_message += promo_dict['promo_link'] + '\n'
    redacted_message += promo_dict['short_descr'][:150] + '\n'

    embed['description'] = redacted_message
    send_msg(webhookurl, "@everyone Nowa promocja planszówkowa!", embed=embed, bot_name=bot_name)


def send_msg(webhookurl, message="@here Your info is here!", *, embed=None, bot_name='temp'):
    data = {}
    data['content'] = message
    data['username'] = bot_name
    if embed:
        data['embeds'] = []
        data['embeds'].append(embed)

    result = requests.post(webhookurl, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        pass
