import jwt
import datetime
import json
from flask import Flask, jsonify, request

service = Flask(__name__)

DEBUG = True
USERS_PATH = '/dictionaries/users.json'  
KEY_PATH = '/dictionaries/config.json'   
CERTIFICATE_KEY = '/certificate/key.pem'  
CERTIFICATE = '/certificate/cert.pem'    
HOST = '0.0.0.0'
PORT = 5000

def start():
    global users_list
    
    with open(USERS_PATH, 'r') as users_file:
        users = json.load(users_file)
        users_list = users["users"]
        users_file.close()

def get_key():
    key = ''
    
    with open(KEY_PATH, 'r') as key_file:
        key_ = json.load(key_file)
        key = key_["key"]
        key_file.close()
    
    return key

def find_right_user(login, password):
    global users_list
    response = False
    user_id = None 
    
    for user in users_list:
        if user['login'] == login and user['password'] == password:
            response = True
            user_id = user['id']
            break
    
    return response, user_id

def run():
    service.run( 
        host=HOST,
        debug=DEBUG,
        ssl_context=(CERTIFICATE, CERTIFICATE_KEY)
    )

@service.route('/authenticate')
def authenticate():
    data = json.loads(request.args.get('data'))
    
    login = data['login']
    password = data['password']
    
    response, user_id = find_right_user(login, password)
    if response:
        token = jwt.encode({'id' : user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, get_key(), algorithm="HS256")
        
        return jsonify({
            "result" : 'authenticated', 
            "token" : token.decode('UTF-8')
        }) 
        
    return jsonify({ "result" : 'unauthenticated' }) 

if __name__ == '__main__':
    start() 
    run()
