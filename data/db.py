
import sqlite3


def SQL(db_path, sql):
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    values = []
    c = conn.cursor()
    cursor = c.execute(sql)
    if "select" not in sql.lower():
        print(sql)
        conn.commit()
    else:
        for row in cursor:
            print(row)
            values.append('1')
        print(values)
    conn.close()
    return values


create_table = '''CREATE TABLE RUNNING_STATUS
                (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                NAME           TEXT    NOT NULL,
                STATUS               TEXT    NOT NULL,
                START_TIME                TEXT    NOT NULL,
                OVER_TIME                TEXT    NOT NULL,
                LINK_REPORT                TEXT    NOT NULL);'''


conn = sqlite3.connect('D:/PingAn/AutoUI/AutoUI/data/running_status.db')
c = conn.cursor()
sql = "DELETE FROM RUNNING_STATUS"
cursor = c.execute(sql)
conn.commit()
conn.close()


# sql = "INSERT INTO RUNNING_STATUS (NAME, STATUS, START_TIME, OVER_TIME, LINK_REPORT) VALUES ('D','DFD','DFD','','')"

'''
cursor = c.execute("SELECT * FROM RUNNING_STATUS ORDER BY id DESC")

for row in cursor:
    print(row)
'''


