data = {
    "code": 200,
    "msg": "success",
    "data": {
        "date": "2022-08-17",
        "week": "三",
        "war": "英雄武氏别院",
        "battle": "云湖天池",
        "camp": "洛阳城北",
        "prestige": [
            "雁门关之役",
            "太原之战·夜守孤城"
        ],
        "relief": "少林·乱世",

        "team": [
            "经首道源·越海珠贝;侠客岛·雾岛寻丹",
            "英雄雁门关之役;华清宫回忆录;英雄刀轮海厅",
            "河阳之战;秦皇陵;风雷刀谷·千雷殿"
        ]
    },
    "time": 1660554416
}

print(data.get("data").get("draw"))
if data.get("data").get("draw"):
    print("draw")