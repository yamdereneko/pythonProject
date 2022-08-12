# import asyncio
#
# import dufte
# import matplotlib
# from matplotlib import pyplot as plt
# matplotlib.rc("font", family='PingFang HK')
#
# var = [{'match_id': 76018395, 'won': True, 'official_recommended': False, 'mvp': False, 'start_time': 1654015570,
#         'end_time': 1654015829, 'kungfu': 'lingsu', 'total_mmr': 2198, 'mmr': 12, 'level': 95, 'avg_grade': 11,
#         'global_role_id': '378302368709802699', 'role_id': '10681035', 'zone': '电信一区', 'server': '龙争虎斗', 'pvp_type': 3,
#         'hidden': False, 'person_name': '不似从前', 'person_id': '41f8afea176a4b44aaa2147b0bfc91e1',
#         'person_avatar': 'https://qdla.pvp.xoyo.com/prod/avatar/tmp/a8165fb8d45449e8b65a4e197c109301/avatar.jpg/8b8f7756c99f4b208f32e8872a288235.jpg',
#         'role_name': '时岁岁', 'status': '', 'medalUrl': '', 'videoNum': 0},
#        {'match_id': 76017782, 'won': True, 'official_recommended': False, 'mvp': False, 'start_time': 1654015375,
#         'end_time': 1654015461, 'kungfu': 'lingsu', 'total_mmr': 2186, 'mmr': 12, 'level': 95, 'avg_grade': 11,
#         'global_role_id': '378302368709802699', 'role_id': '10681035', 'zone': '电信一区', 'server': '龙争虎斗', 'pvp_type': 3,
#         'hidden': False, 'person_name': '不似从前', 'person_id': '41f8afea176a4b44aaa2147b0bfc91e1',
#         'person_avatar': 'https://qdla.pvp.xoyo.com/prod/avatar/tmp/a8165fb8d45449e8b65a4e197c109301/avatar.jpg/8b8f7756c99f4b208f32e8872a288235.jpg',
#         'role_name': '时岁岁', 'status': '', 'medalUrl': '', 'videoNum': 0},
#        {'match_id': 76017248, 'won': False, 'official_recommended': False, 'mvp': True, 'start_time': 1654015217,
#         'end_time': 1654015290, 'kungfu': 'lingsu', 'total_mmr': 2174, 'mmr': -7, 'level': 95, 'avg_grade': 11,
#         'global_role_id': '378302368709802699', 'role_id': '10681035', 'zone': '电信一区', 'server': '龙争虎斗', 'pvp_type': 3,
#         'hidden': False, 'person_name': '不似从前', 'person_id': '41f8afea176a4b44aaa2147b0bfc91e1',
#         'person_avatar': 'https://qdla.pvp.xoyo.com/prod/avatar/tmp/a8165fb8d45449e8b65a4e197c109301/avatar.jpg/8b8f7756c99f4b208f32e8872a288235.jpg',
#         'role_name': '时岁岁', 'status': '', 'medalUrl': '', 'videoNum': 0},
#        {'match_id': 76016726, 'won': False, 'official_recommended': False, 'mvp': True, 'start_time': 1654015065,
#         'end_time': 1654015128, 'kungfu': 'lingsu', 'total_mmr': 2181, 'mmr': -4, 'level': 95, 'avg_grade': 11,
#         'global_role_id': '378302368709802699', 'role_id': '10681035', 'zone': '电信一区', 'server': '龙争虎斗', 'pvp_type': 3,
#         'hidden': False, 'person_name': '不似从前', 'person_id': '41f8afea176a4b44aaa2147b0bfc91e1',
#         'person_avatar': 'https://qdla.pvp.xoyo.com/prod/avatar/tmp/a8165fb8d45449e8b65a4e197c109301/avatar.jpg/8b8f7756c99f4b208f32e8872a288235.jpg',
#         'role_name': '时岁岁', 'status': '', 'medalUrl': '', 'videoNum': 0},
#        {'match_id': 76016353, 'won': False, 'official_recommended': False, 'mvp': False, 'start_time': 1654014946,
#         'end_time': 1654014982, 'kungfu': 'lingsu', 'total_mmr': 2185, 'mmr': -8, 'level': 95, 'avg_grade': 11,
#         'global_role_id': '378302368709802699', 'role_id': '10681035', 'zone': '电信一区', 'server': '龙争虎斗', 'pvp_type': 3,
#         'hidden': False, 'person_name': '不似从前', 'person_id': '41f8afea176a4b44aaa2147b0bfc91e1',
#         'person_avatar': 'https://qdla.pvp.xoyo.com/prod/avatar/tmp/a8165fb8d45449e8b65a4e197c109301/avatar.jpg/8b8f7756c99f4b208f32e8872a288235.jpg',
#         'role_name': '时岁岁', 'status': '', 'medalUrl': '', 'videoNum': 0},
#        {'match_id': 76015292, 'won': True, 'official_recommended': False, 'mvp': False, 'start_time': 1654014631,
#         'end_time': 1654014833, 'kungfu': 'lingsu', 'total_mmr': 2193, 'mmr': 27, 'level': 95, 'avg_grade': 11,
#         'global_role_id': '378302368709802699', 'role_id': '10681035', 'zone': '电信一区', 'server': '龙争虎斗', 'pvp_type': 3,
#         'hidden': False, 'person_name': '不似从前', 'person_id': '41f8afea176a4b44aaa2147b0bfc91e1',
#         'person_avatar': 'https://qdla.pvp.xoyo.com/prod/avatar/tmp/a8165fb8d45449e8b65a4e197c109301/avatar.jpg/8b8f7756c99f4b208f32e8872a288235.jpg',
#         'role_name': '时岁岁', 'status': '', 'medalUrl': '', 'videoNum': 0},
#        {'match_id': 76014607, 'won': True, 'official_recommended': False, 'mvp': False, 'start_time': 1654014436,
#         'end_time': 1654014533, 'kungfu': 'lingsu', 'total_mmr': 2179, 'mmr': 21, 'level': 95, 'avg_grade': 10,
#         'global_role_id': '378302368709802699', 'role_id': '10681035', 'zone': '电信一区', 'server': '龙争虎斗', 'pvp_type': 3,
#         'hidden': False, 'person_name': '不似从前', 'person_id': '41f8afea176a4b44aaa2147b0bfc91e1',
#         'person_avatar': 'https://qdla.pvp.xoyo.com/prod/avatar/tmp/a8165fb8d45449e8b65a4e197c109301/avatar.jpg/8b8f7756c99f4b208f32e8872a288235.jpg',
#         'role_name': '时岁岁', 'status': '', 'medalUrl': '', 'videoNum': 0},
#        {'match_id': 76013810, 'won': True, 'official_recommended': False, 'mvp': False, 'start_time': 1654014218,
#         'end_time': 1654014347, 'kungfu': 'lingsu', 'total_mmr': 2166, 'mmr': -13, 'level': 95, 'avg_grade': 9,
#         'global_role_id': '378302368709802699', 'role_id': '10681035', 'zone': '电信一区', 'server': '龙争虎斗', 'pvp_type': 3,
#         'hidden': True, 'person_name': '不似从前', 'person_id': '41f8afea176a4b44aaa2147b0bfc91e1',
#         'person_avatar': 'https://qdla.pvp.xoyo.com/prod/avatar/tmp/a8165fb8d45449e8b65a4e197c109301/avatar.jpg/8b8f7756c99f4b208f32e8872a288235.jpg',
#         'role_name': '时岁岁', 'status': '', 'medalUrl': '', 'videoNum': 0},
#        {'match_id': 76013198, 'won': False, 'official_recommended': False, 'mvp': False, 'start_time': 1654014043,
#         'end_time': 1654014139, 'kungfu': 'lingsu', 'total_mmr': 2158, 'mmr': -7, 'level': 95, 'avg_grade': 10,
#         'global_role_id': '378302368709802699', 'role_id': '10681035', 'zone': '电信一区', 'server': '龙争虎斗', 'pvp_type': 3,
#         'hidden': False, 'person_name': '不似从前', 'person_id': '41f8afea176a4b44aaa2147b0bfc91e1',
#         'person_avatar': 'https://qdla.pvp.xoyo.com/prod/avatar/tmp/a8165fb8d45449e8b65a4e197c109301/avatar.jpg/8b8f7756c99f4b208f32e8872a288235.jpg',
#         'role_name': '时岁岁', 'status': '', 'medalUrl': '', 'videoNum': 0},
#        {'match_id': 76011387, 'won': False, 'official_recommended': False, 'mvp': False, 'start_time': 1654013567,
#         'end_time': 1654013796, 'kungfu': 'lingsu', 'total_mmr': 2165, 'mmr': -5, 'level': 95, 'avg_grade': 11,
#         'global_role_id': '378302368709802699', 'role_id': '10681035', 'zone': '电信一区', 'server': '龙争虎斗', 'pvp_type': 3,
#         'hidden': False, 'person_name': '不似从前', 'person_id': '41f8afea176a4b44aaa2147b0bfc91e1',
#         'person_avatar': 'https://qdla.pvp.xoyo.com/prod/avatar/tmp/a8165fb8d45449e8b65a4e197c109301/avatar.jpg/8b8f7756c99f4b208f32e8872a288235.jpg',
#         'role_name': '时岁岁', 'status': '', 'medalUrl': '', 'videoNum': 0}]
#
# data = [{'mainServer': '青梅煮酒', 'mainZone': '双线四区', 'connectState': True},
#        {'mainServer': '天鹅坪', 'mainZone': '双线一区', 'connectState': True},
#        {'mainServer': '破阵子', 'mainZone': '双线一区', 'connectState': True},
#        {'mainServer': '飞龙在天', 'mainZone': '双线二区', 'connectState': True},
#        {'mainServer': '长安城', 'mainZone': '电信一区', 'connectState': True},
#        {'mainServer': '龙争虎斗', 'mainZone': '电信一区', 'connectState': True},
#        {'mainServer': '蝶恋花', 'mainZone': '电信一区', 'connectState': True},
#        {'mainServer': '斗转星移', 'mainZone': '电信五区', 'connectState': True},
#        {'mainServer': '乾坤一掷', 'mainZone': '电信五区', 'connectState': True},
#        {'mainServer': '梦江南', 'mainZone': '电信五区', 'connectState': True},
#        {'mainServer': '唯我独尊', 'mainZone': '电信五区', 'connectState': True},
#        {'mainServer': '幽月轮', 'mainZone': '电信五区', 'connectState': True},
#        {'mainServer': '剑胆琴心', 'mainZone': '电信五区', 'connectState': True},
#        {'mainServer': '绝代天骄', 'mainZone': '电信八区', 'connectState': True}]
#
# async def get_figure():
#     fig, ax = plt.subplots(figsize=(8, 9), facecolor='white', edgecolor='white')
#     plt.style.use(dufte.style)
#     ax.axis([0, 10, 0, 14])
#     ax.set_title("区服信息", fontsize=19, color='#303030', fontweight="heavy",
#                  verticalalignment='top',)
#     ax.axis('off')
#     for x, y in enumerate(data):
#         mainServer = y.get("mainServer")
#         mainZone = y.get("mainZone")
#         connectState = y.get("connectState")
#         serverState = connectState is True and "已开服" or "未开服"
#         ax.text(1, x, f'{mainServer}', verticalalignment='bottom', horizontalalignment='left',
#                 color='#404040')
#         ax.text(4, x, f'{mainZone} ', verticalalignment='bottom', horizontalalignment='left', color='#404040')
#         fontColor = serverState == "已开服" and 'green' or 'red'
#         ax.text(7, x, f'{serverState}', verticalalignment='bottom', horizontalalignment='left', color=fontColor)
#     plt.show()
#     plt.savefig(f"/tmp/serverState.png")
# asyncio.run(get_figure())

aa = "姨妈 小丛兰"
if aa.find(" ") == -1:
    print("no")
else:
    print("yes")