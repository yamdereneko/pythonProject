import sqlite3


def sqlite(role: str):
    conn = sqlite3.connect("../ymProject/API/farbnamen.v4.db")
    sql = "select * from InfoCache where name=\'{0}\'".format(role)
    cursor = conn.execute(sql)
    role_id = None
    for info in cursor:
        role_id = info[0]
    conn.close()
    return role_id