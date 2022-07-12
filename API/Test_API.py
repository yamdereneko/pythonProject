import json
import requests


def request_api(**kwargs):
    action = kwargs.get("action")
    if action == "daily":
        url = "https://www.jx3api.com/app/{0}".format(action)
        headers = {'content-type': 'application/json'}
        response = requests.post(url, headers=headers)
    else:
        response = None
    return response


def main():
    result = request_api(action="daily")
    print(result.json())


if __name__ == '__main__':
    main()
