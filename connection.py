import pymysql
def con():
    return pymysql.connect(host='mysql.j685148.myjino.ru',
                           user='j685148',
                           passwd='BvWrvc3v9',
                           db='j685148_fff',
                           charset='utf8')

