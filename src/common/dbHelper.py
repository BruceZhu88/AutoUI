

import sqlite3


def SQL(db_path, sql):
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    value = []
    c = conn.cursor()
    print(sql)
    cursor = c.execute(sql)
    if ("select" or "SELECT") not in sql:
        conn.commit()
        conn.close()
    else:
        for row in cursor:
            value.append(row)
    conn.close()
    return value


if __name__ == '__main__':
    create_table = '''CREATE TABLE RUNNING_STATUS
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                    NAME           TEXT    NOT NULL,
                    STATUS               TEXT    NOT NULL,
                    START_TIME                TEXT    NOT NULL,
                    OVER_TIME                TEXT    NOT NULL,
                    LINK_REPORT                TEXT    NOT NULL);'''

    SQL('./running_status.db', create_table)
