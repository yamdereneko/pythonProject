import json
import urllib

import requests
import urllib3


def request_api(**kwargs):
    action = kwargs.get("action")
    url = "https://www.jx3api.com/app/{0}".format(action)
    headers = {'content-type': 'application/json'}
    if action == "daily":
        urllib3.disable_warnings()
        response = requests.post(url, headers=headers)
    elif action == "demon":
        payload = {
            "server": "斗转星移"
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
    else:
        response = None
    return response


def main():
    daily = request_api(action="daily")
    print(daily.json())

    demon = request_api(action="demon")
    print(demon.json())


if __name__ == '__main__':
    main()
