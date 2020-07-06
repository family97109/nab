import pymysql.cursors
from ua_parser import user_agent_parser
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import db.connection as dc


# Command line 參數
parser = argparse.ArgumentParser()

## DB
dbInfo = parser.add_argument_group('db', '資料庫資訊')
dbInfo.add_argument("mysql", choices = ["dev", "testDB"], help="MySQL service")
dbInfo.add_argument("db", help="db name")

## Other
otherInfo = parser.add_argument_group('other', '其他資訊')
otherInfo.add_argument("time", help="how many months advanced?")
otherInfo.add_argument("app", help="admin, member or reseller?")

## Optional
parser.add_argument('-p', '--plot', action='store_true', help="show plot or not?") # 圖片是否顯示

args = parser.parse_args()


# MySQL 連線
if args.mysql == "dev":
    db = dc.DbInfo(dc.DEV['host'], dc.DEV['port'], dc.DEV['user'], dc.DEV['password'], args.db)
if args.mysql == "testDB":
    db = dc.DbInfo(dc.TESTDB['host'], dc.TESTDB['port'], dc.TESTDB['user'], dc.TESTDB['password'], args.db)

connection = db.dbConnect(db.dbConfig())


try:
    with connection.cursor() as cursor:

        sql = "SELECT '{}' AS `user`, COUNT(*) AS `count` FROM `logging_login` WHERE `added_time` > DATE_ADD(NOW(), INTERVAL -{} MONTH) AND `app_name` = '{}';".format(args.app, args.time, args.app)
        cursor.execute(sql)

        result = cursor.fetchall()
        count_df = pd.DataFrame(result)

        print(count_df)

        if args.plot:
            count_df.plot.bar(x='user', y='count', rot=0)
            plt.show()
        
        connection.commit()

finally:
    connection.close()