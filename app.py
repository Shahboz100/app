from flask import Flask, abort, request, jsonify, make_response
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from datetime import timedelta
import connection
import json
from datetime import date


'''
    Внешние файлы проекта
'''
import clients
import drivers
import carcase
import ads

class Driver(object):
    def __init__(self, id, name, surname, tel, password,location,status,balance,email,date,access):
        self.id = id
        self.tel = tel
        self.name = name
        self.surname = surname
        self.password = password
        self.location = location
        self.status = status
        self.balance = balance
        self.email = email
        self.date = date
        self.access = access

    def __str__(self):
        return json.dumps({'id_driver':self.id,
                           'name':self.name,
                           'surname':self.surname,
                           'tel':self.tel,
                           'location':self.location,
                           'status':self.status,
                           'balance':self.balance,
                           'e-mail':self.email,
                           'date':self.date.isoformat(),
                           'access':int(self.access)})
class Client(object):
    def __init__(self,id, name, surname, tel, password, location):
        self.id = id
        self.name = name
        self.surname = surname
        self.tel = tel
        self.password = password
        self.location = location
    def __str__(self):
        return json.dumps({'id_client':self.id,
                           'name':self.name,
                           'surname':self.surname,
                           'tel':self.tel,
                           'location':self.location})

conn = connection.con() #Соединение с сервером
cur = conn.cursor()

cur.execute("SELECT * FROM driver")

users = []
for u in cur:
    users.append(Driver(u[0], u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8],u[9],u[10]))

cur.execute("SELECT * FROM client")
conn.close()
for u in cur:
    users.append(Client(u[0], u[1],u[2],u[3],u[4],u[5]))

tel_user = {u.tel: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(tel, password):
    user = tel_user.get(tel, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'mega-super-secret'
#app.config['JWT_EXPIRATION_DELTA']=timedelta(seconds=300)
jwt = JWT(app, authenticate, identity)

"""
    Информации авторизовавшего пользователя
"""
@app.route('/', methods=['GET'])
@jwt_required()
def protected():
    return '%s' % current_identity
"""
    Получение информации о всех водителях
"""
@app.route('/drivers', methods=['GET'])
def get_drivers():
    return jsonify({'drivers': drivers.get_drivers()})

"""
    Регистрация водителя
"""
@app.route('/driver', methods=['POST'])
def post_driver():
    """
        Проверка целостности POST запроса
    """
    if not request.json or not 'name' in request.json or not 'surname' in request.json or not 'password' in request.json or not 'tel' in request.json:
        return make_response(jsonify({'error':'incomplete data'}))
    
    """
        Получение информации из POST запроса
        Запись в базу данных
    """    
    return jsonify(response=drivers.post_driver(json.loads(json.dumps(request.json['name'])),
        json.loads(json.dumps(request.json['surname'])),json.loads(json.dumps(request.json['password'])),
        json.loads(json.dumps(request.json['tel']))))

"""
    Получение информации об одном водителе
"""
@app.route('/driver/<int:id_driver>', methods=['GET'])
@jwt_required()
def driver(id_driver):
    return jsonify(response=drivers.get_driver(id_driver))

'''
    Получение информации о кузове
'''
@app.route('/carcase', methods=['GET'])
@jwt_required()
def get_carcase():
    return jsonify({'carcase':carcase.get_carcase()})

"""
    Получить информацию о всех клиентах
"""
@app.route('/clients', methods=['GET'])
@jwt_required()
def get_clients():
    return jsonify({'clients': clients.get_clients()})

'''
    Регистрация КЛИЕНТА
'''
@app.route('/client', methods=['POST'])
def client():
    
    if not request.json or not 'name' in request.json or not 'surname' in request.json or not 'password' in request.json or not 'tel' in request.json:
        return make_response(jsonify({'error':'incomplete data'}))

    return jsonify(response=clients.client(json.loads(json.dumps(request.json['name'])),
                    json.loads(json.dumps(request.json['surname'])),
                    json.loads(json.dumps(request.json['password'])),
                    json.loads(json.dumps(request.json['tel']))))
'''
    Получение информации об одном клиенте
'''
@app.route('/client/<int:id_clienta>', methods=['GET'])
@jwt_required()
def get_client(id_clienta):
    return jsonify(response=clients.get_client(id_clienta))


"""
    Получение объявлений
"""
@app.route('/news',methods=['GET'])
def get_ads():
    add = None
    if request.args.get('addres')!=None:
        add = request.args.get('addres')
    return jsonify(response=ads.get_ads(add))

if __name__ == '__main__':
    app.run()
