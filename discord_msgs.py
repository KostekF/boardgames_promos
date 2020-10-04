import requests
import json

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
