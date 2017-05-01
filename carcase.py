"""
    В этом файле находятся все запросы с таблицы carcase
    v1.0
"""
import connection

'''
    Получение информации о кузове
'''
def get_carcase():
    try:
        conn = connection.con() #Соединение с сервером
        cur = conn.cursor()
        
        carcase=[]
        cur.execute("SELECT * FROM carcase")

        for case in cur:
            carcase.append(dict(id_carcase = case[0],type=case[1]))
        return carcase
    except:
        return 'server is unvailable'
    finally:
        conn.close()
