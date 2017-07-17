"""
    В этом файле находятся все запросы с таблицы client
    v1.0
"""
import connection


"""
    Получить информацию о всех клиентах
"""
def get_clients():
    try:
        
        conn = connection.con()  #Соединение с сервером
        cur = conn.cursor()

        clients = []
        cur.execute("SELECT id_client, name, surname, tel, location FROM client")

        for client in cur:
            clients.append(dict(id_client=client[0],name=client[1],surname=client[2],tel=client[3],location=client[4]))

        return clients
    except:
        return 'server is unvailable'
    finally:
        conn.close()

'''
    Регистрация КЛИЕНТА
'''
def client(name,surname,password,tel):
    try:    
        conn = connection.con()  #Соединение с сервером
        cur  = conn.cursor()
    
        sql = "INSERT INTO client(name, surname, password, tel) VALUES (%s, %s, %s, %s)"

        cur.execute(sql,(name,surname,password,tel))
        conn.commit()

        return 'success'
    except:
        return 'incomplete data'
    finally:
        conn.close()

'''
    Получение информации об одном клиенте
'''
def get_client(id_clienta):
    
    try:
        conn = connection.con()  #Соединение с сервером
        cur  = conn.cursor()

        cur.execute('SELECT name, surname, tel, location FROM client WHERE id_client=%s',(int(id_clienta)))
        result=cur.fetchone()   #Получение ответа запроса
        
        if result == None:
            return 'not found'
        res={'id_client':id_clienta,
             'name':result[0],

             'surmane':result[1],
             'tel':result[2],
             'location':result[3],
            }
        return res
    except:
        return 'service is unavailable'
    finally:
        conn.close()
