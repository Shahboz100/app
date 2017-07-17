import pymysql
def con():
    return pymysql.connect(host='localhost',
                           user='root',
                           passwd='',
                           db='database',
                           charset='utf8')
