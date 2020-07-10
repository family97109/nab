import click
import pymysql.cursors
import pandas as pd
import matplotlib.pyplot as plt
import tool.connection
import tool.ua_parse


@click.group()
def cli():
    """
    Hey 我是 nab
    """
    pass

@click.command()
@click.option('--mysql', help='MySQL service', required=True, prompt='MySQL Connection', type=click.Choice(['dev', 'testDB']))
@click.option('--dbname', help='DB name', required=True, prompt='DB Name')
@click.option('--time', help='"N:How many months advanced?, yyyy-mm-dd', required=True, prompt='N or yyyy-mm-dd')
@click.option('--user', help='admin, member or reseller?', required=True, prompt=True, type=click.Choice(['admin', 'member', 'reseller']))
@click.option('-p', '--plot', help='Show plot or not?', is_flag=True, expose_value=True, prompt='Show plot or not?')
def login_count(mysql, dbname, time, user, plot):
    # MySQL 連線
    db = tool.connection.DbInfo(mysql, dbname)
    connection = db.dbConnect(db.dbConfig())


    try:
        with connection.cursor() as cursor:

            if len(time) < 10:
                sql = "SELECT '{}' AS `user`, COUNT(*) AS `count` FROM `logging_login` WHERE `added_time` > DATE_ADD(NOW(), INTERVAL -{} MONTH) AND `app_name` = '{}';".format(user, time, user)
            else:
                sql = "SELECT '{}' AS `user`, COUNT(*) AS `count` FROM `logging_login` WHERE `added_time` > '{}' AND `app_name` = '{}';".format(user, time, user)
            cursor.execute(sql)

            result = cursor.fetchall()
            count_df = pd.DataFrame(result)

            # 印出結果
            print(count_df)

            # 圖片顯示
            if plot:
                count_df.plot.bar(x='user', y='count', rot=0)
                plt.show()
            
            connection.commit()

    finally:
        connection.close()

@click.command()
@click.option('--mysql', help='MySQL service', required=True, prompt='MySQL Connection', type=click.Choice(['dev', 'testDB']))
@click.option('--dbname', help='DB name', required=True, prompt='DB Name')
@click.option('--time', help='"How many months advanced?', required=True, prompt=True)
@click.option('--user', help='admin, member or reseller?', required=True, prompt=True, type=click.Choice(['admin', 'member', 'reseller']))
@click.option('--info', help='os or browser or both', type=int, prompt='Info (os:1, browser:2, both:3)')
@click.option('-p', '--plot', help='Show plot or not?', is_flag=True, expose_value=True, prompt='Show plot or not?')
def user_agent_os_browser(mysql, dbname, time, user, info, plot):
    # MySQL 連線
    db = tool.connection.DbInfo(mysql, dbname)
    connection = db.dbConnect(db.dbConfig())


    try:
        with connection.cursor() as cursor:

            # 清空 user_agent_parse table
            sql = "TRUNCATE TABLE `user_agent_parse`;"
            cursor.execute(sql)

            # 選取 user agent 資料
            sql = "SELECT UA.`user_agent` \
                        FROM \
                        (SELECT DISTINCT `login_name` , `user_agent` \
                        FROM `logging_login` \
                        WHERE `app_name` = '{}' AND `user_agent` != '' AND `added_time` > DATE_ADD(NOW(), INTERVAL -{} MONTH)) UA;".format(user, time)
            cursor.execute(sql)
            result = cursor.fetchall()

            for member in result:
                parseString = tool.ua_parse.user_agent_parser.Parse(list(member.values())[0])

                # os, browser info
                os = tool.ua_parse.os(parseString)
                os_version = tool.ua_parse.os_version(parseString)
                browser = tool.ua_parse.browser(parseString)
                browser_version = tool.ua_parse.browser_version(parseString)

                # 將資料插入 user_agent_parse table
                sql = "INSERT INTO `user_agent_parse` (`brand`, `os`, `os_version`, `browser`, `browser_version`) VALUE (%s, %s, %s, %s, %s);"
                data = ("lv", os, os_version, browser, browser_version)
                cursor.execute(sql, data)

            if (info == 1) or (info == 3):
                ## 全品牌 os 個數
                sql = "SELECT OS.`os`, OS.`count` FROM (SELECT `os`, COUNT(*) AS `count` FROM `user_agent_parse` GROUP BY `os`) OS"
                cursor.execute(sql)
                result = cursor.fetchall()
                os_df = pd.DataFrame(result)
                print("全品牌 os 個數")
                print(os_df)
                os_df.plot.bar(x='os', y='count', rot=0, figsize=(6, 7))

                ## 全品牌 os version 個數
                sql = "SELECT OS_VERSION.`os`, OS_VERSION.`os_version`, OS_VERSION.`count` FROM (SELECT `os`, `os_version`, COUNT(*) AS `count` FROM `user_agent_parse` GROUP BY `os`, `os_version`) OS_VERSION"
                cursor.execute(sql)
                result = cursor.fetchall()
                osVersion_df = pd.DataFrame(result)
                print("\n全品牌 os version 個數")
                print(osVersion_df)

                # if excel:
                #     os_df.to_excel('os.xlsx', sheet_name = 'os')
                #     osVersion_df.to_excel('os_version.xlsx', sheet_name = 'os_version')
            
            if (info == 2) or(info == 3):
                ## 全品牌browser 個數
                sql = "SELECT BROWSER.`browser`, BROWSER.`count` FROM (SELECT `browser`, COUNT(*) AS `count` FROM `user_agent_parse` GROUP BY `browser`) BROWSER"
                cursor.execute(sql)
                result = cursor.fetchall()
                browser_df = pd.DataFrame(result)
                print("\n全品牌browser 個數")
                print(browser_df)
                browser_df.plot.bar(x='browser', y='count', figsize=(6, 7))

                ## 全品牌rowser version 個數
                sql = "SELECT BROWSER_VERSION.`browser`, BROWSER_VERSION.`browser_version`, BROWSER_VERSION.`count` FROM (SELECT `browser`, `browser_version`, COUNT(*) AS `count` FROM `user_agent_parse` GROUP BY `browser`, `browser_version`) BROWSER_VERSION"
                cursor.execute(sql)
                result = cursor.fetchall()
                browserVersion_df = pd.DataFrame(result)
                print("\n全品牌rowser version 個數")
                print(browserVersion_df)

                # if excel:
                #     browser_df.to_excel('browser.xlsx', sheet_name = 'browser')
                #     browserVersion_df.to_excel('browser_version.xlsx', sheet_name = 'browser_version')

            if plot:
                plt.show()

            connection.commit()

    finally:
        connection.close()

@click.command('hello')
def hello():
    print("Hello")



cli.add_command(login_count)
cli.add_command(user_agent_os_browser)
cli.add_command(hello)