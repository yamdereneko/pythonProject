import json
import requests
import urllib3

import jx3Data.jxDatas as JX3Data


def request_api(size, school, page):
    bodyType = JX3Data.bodyType
    school_type = JX3Data.school_number
    url = "https://api-wanbaolou.xoyo.com/api/buyer/goods/list?game_id=jx3&filter%5Brole_sect%5D={0}&filter%5Brole_shape%5D={1}&game=jx3&page={2}&size=10&goods_type=2".format(
        school_type[school], bodyType[size], page)
    payload = {}
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers, data=payload)
    return response.json()


def main(size, school, page = 1):
    man = request_api(size, school, page)
    # print(man.get("data").get("total_record"))
    roles_dict = []
    roles = {}
    for role in man.get("data").get("list"):
        print(role)
        roles["门派"] = role.get("attrs").get("role_sect")
        roles["装分"] = role.get("attrs").get("role_equipment_point")
        roles["资历"] = role.get("attrs").get("role_experience_point")
        roles["阵营"] = role.get("attrs").get("role_camp")
        roles["体型"] = role.get("attrs").get("role_shape")
        roles["价格"] = role.get("single_unit_price") / 100
        roles["点赞"] = role.get("followed_num")
        roles["服务器"] = role.get("info").split("-")[1]
        roles["链接"] = "https://jx3.seasunwbl.com/role?consignment_id=" + role.get("consignment_id")
        print(roles)
    return roles


if __name__ == '__main__':
    main("萝莉","蓬莱")
