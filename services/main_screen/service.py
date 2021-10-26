import jwt
import json
from flask import Flask, jsonify, request
from functools import wraps

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
        users_list = users['users']
        users_file.close()

def get_key():
    key = ''
    
    with open(KEY_PATH, 'r') as key_file:
        key_ = json.load(key_file)
        key = key_["key"]
        key_file.close()
    
    return key

def get_id():
    token = request.args.get('token')
    
    data = jwt.decode(token, get_key(), algorithm="HS256")
    
    return data['id']
    
def filter_by_id(id):
    global users_list
    response = None
    
    for user in users_list:
        if user['id'] == id:
            response = user
            break
    
    return response

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        
        if not token: 
            return jsonify({'message' : 'Token is missing!'}), 403
            
        try:
            jwt.decode(token, get_key(), algorithm="HS256")
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403
        
        return f(*args, **kwargs)
    return decorated

def run():
    service.run( 
        host=HOST,
        debug=DEBUG,
        ssl_context=(CERTIFICATE, CERTIFICATE_KEY)
    )

@service.route('/main')
@token_required
def get_main_screen_data():    
    user = filter_by_id(get_id())
    
    if user:
        account = user['account']
        return jsonify({
            'name' : user['name'],
            'account' : {
                'balance': account['balance'],
            }
        })
    else:
        return jsonify({
            'response' : 'no_matches'
        })

if __name__ == '__main__':
    start()
    run()