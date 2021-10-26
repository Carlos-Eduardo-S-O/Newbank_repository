import jwt
import datetime
import json
from flask import Flask, jsonify, request
from cipher import decrypt, encrypt
from urllib.parse import unquote

service = Flask(__name__)

# Service data
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000 

# Dictionaries
USERS_PATH = '/dictionaries/users.json' 
KEY_PATH = '/dictionaries/config.json' 

# SSL files
CERTIFICATE_KEY = '/ssl_files/certificate_key.pem'
CERTIFICATE = '/ssl_files/certificate.pem'

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
            public_key = user['publickey']
            break

    if response == True:
        return response, user_id, public_key
    else:
        return response, None, None

def run():
    service.run( 
        host=HOST,
        debug=DEBUG,
        ssl_context=(CERTIFICATE, CERTIFICATE_KEY)
    )

@service.route('/authenticate')
def authenticate():
    response = None 
    public_key = None
    # Prepare data from front-end to decrypt
    data = unquote(request.args.get("data"))
    
    # Decrypt data from front end
    error, decrypted_data = decrypt(data)
    
    if not error:
        # Load string to json format
        credentials = json.loads(decrypted_data)
        
        login = credentials["login"]
        password = credentials["password"]        
        
        response, user_id, pub_key = find_right_user(login, password)
        public_key = pub_key
        
        if response:
            token = jwt.encode({'id' : user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, get_key(), algorithm="HS256")
            
            response = {
                "result" : 'authenticated', 
                "token" : token.decode('UTF-8'),
            }
        else:
            response = { "result" : 'unauthenticated'} 
    else:
        response = { "result" : "Something went wrong, please try again later"}

    # Encrypt the data to return
    error, encrypted = encrypt(public_key, json.dumps(response, separators=(',', ':')))
    response = encrypted
    
    # If something  goes wrong with the encryption the text error will be returned
    if error:
        response = "error user not found"

    return response

if __name__ == '__main__':
    start()
    run()
