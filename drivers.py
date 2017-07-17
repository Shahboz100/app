"""
	В этом файле находятся все запросы с таблицы driver
	v1.0
"""
import connection
import hashlib

"""
    Регистрация водителя
"""
def post_driver(name,surname,password,tel):
    try:
        conn = connection.con()
        cur  = conn.cursor()
        #p = hashlib.sha512()
        #p.update(password.encode('UTF-8'))
        #password = p.hexdigest()
        sql = "INSERT INTO driver(name, surname, password, tel) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (name, surname, password, tel))
        conn.commit()
        return "success"
    except:
        return "incomplete data"
    finally:
        conn.close()

"""
    Получение информации о всех водителях
"""
def get_drivers():
    try:
        conn = connection.con()
        cur  = conn.cursor()
        drivers = []
        cur.execute("SELECT id_driver, name, surname, tel, location,status, balance FROM driver")

        for driver in cur:
            drivers.append(dict(id_driver=driver[0],name=driver[1],surname=driver[2],tel=driver[3],location=driver[4],status=driver[5],balance=driver[6]))
        return drivers
    except:
        return "server is unvailable"
    finally:
        conn.close()

"""
    Получение информации об одном водителе
"""
def get_driver(id_driver):
    try:
        conn = connection.con()   #Соединение с сервером
        cur  = conn.cursor()

        cur.execute('SELECT name,surname,tel,location,status FROM driver WHERE id_driver=%s',(int(id_driver)))
        result=cur.fetchone()   #Получение ответа запроса

        if result == None:
            return 'not found'
        res={'id_driver':id_driver,
             'name':result[0],

             'surmane':result[1],
             'tel':result[2],

             'location':result[3],
             'status':result[4]
            }
        return res
    except:
        return 'service is unavailable'
    finally:
        conn.close()
