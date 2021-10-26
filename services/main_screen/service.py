import jwt
import json
from flask import Flask, jsonify, request
from functools import wraps
from cipher import decrypt, encrypt
from urllib.parse import unquote

service = Flask(__name__)

# Service Data
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Dictionaries
USERS_PATH = '/dictionaries/users.json'
KEY_PATH = '/dictionaries/config.json'

# RSA Files
CERTIFICATE_KEY =  '/ssl_files/certificate_key.pem'
CERTIFICATE =   '/ssl_files/certificate.pem'

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
    id = None
    
    error, token = decrypt(unquote(request.args.get('token')))
    
    if not error:
        data = jwt.decode(token, get_key(), algorithm="HS256")
        id = data['id']
    
    return id
    
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
        error, token = decrypt(unquote(request.args.get('token')))
        
        if not token and not error: 
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
    public_key = None
    id = get_id()
    response = None
    
    if id:
        user = filter_by_id(get_id())
        
        if user:
            public_key = user['publickey']
            account = user['account']
            
            response = {
                'name' : user['name'],
                'account' : {
                    'balance': account['balance'],
                }
            }
        else:
            response = {
                'response' : 'no_matches'
            }
    else:
        response = {
            'response' : 'no_matches'
        }
    
    error, encrypted = encrypt(public_key, json.dumps(response, separators=(',', ':')))
    response = encrypted
    
    if error: 
        response = response = jsonify({ "result" : "Something went wrong, please try again later"})
    
    return response

if __name__ == '__main__':
    start()
    run()
