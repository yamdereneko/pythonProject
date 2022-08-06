import pymysql


async def connect_Mysql(sql):
    try:
        db = pymysql.connect(host="localhost", user="root", password="Qinhao123.", database="farbnamen", charset="utf8")
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        db.commit()
        res = cursor.fetchall()
        db.close()
        return res
    except Exception as e:
        print(e)
        print("连接数据库异常")


async def get_JJCWeeklyRecord(table, weekly):
    sql = "select * from %s where week='%s'" % (table, weekly)
    res = await connect_Mysql(sql)
    print(res)
    return res
