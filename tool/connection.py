import pymysql.cursors

DEV = {
    'host': "10.200.252.216",
    'port': 3306,
    'user': "rd_infra",
    'password': "bkinfra@DEV" ,
}

TESTDB = {
    'host': "10.200.252.125",
    'port': 3306,
    'user': "rd_infra",
    'password': "bkinfra@DEV",
}

class DbInfo():
    def __init__(self, mysql, dbName):
        if mysql == 'dev':
            self.host = DEV['host']
            self.port = DEV['port']
            self.user = DEV['user']
            self.password = DEV['password']
            self.name = dbName

        if mysql == 'testDB':
            self.host = TESTDB['host']
            self.port = TESTDB['port']
            self.user = TESTDB['user']
            self.password = TESTDB['password']
            self.name = dbName

    def dbConfig(self):
        config = {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'db': self.name,
            'charset':'utf8mb4',
            'cursorclass':pymysql.cursors.DictCursor,
        }
        return config

    def dbConnect(self, config):
        connection = pymysql.connect(**config)
        return connection