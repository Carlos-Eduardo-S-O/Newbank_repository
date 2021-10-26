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
NOTIFICATION_PATH = '/dictionaries/notifications.json'
# RSA Files
CERTIFICATE_KEY =  '/ssl_files/certificate_key.pem'
CERTIFICATE =   '/ssl_files/certificate.pem'


def start():
    global notification_list
    
    with open(NOTIFICATION_PATH, 'r') as notifications_file:
        notification = json.load(notifications_file)
        notification_list = notification['notifications']
        notifications_file.close()
    
    global users_list
    
    with open(USERS_PATH, 'r') as users_file:
        users = json.load(users_file)
        users_list = users['users']
        users_file.close()

def get_key():
    key = ''
    
    with open(KEY_PATH, 'r') as key_file:
        key_ = json.load(key_file)
        key = key_['key']
        key_file.close()
    
    return key

def get_user_public_key(id):
    public_key = None
    
    for user in users_list:
        if user['id'] == id:
            public_key = user['publickey']
            break
    
    return public_key

def get_id():
    id = None
    
    error, token = decrypt(unquote(request.args.get('token')))
    
    if not error:
        data = jwt.decode(token, get_key(), algorithm="HS256")
        id = data['id']
    
    return id

def filter_by_id(id):
    global notification_list
    response = list()
    
    for notification in notification_list:
        if notification['user_id'] == id:
            response.append(notification)
    
    return response

def get_last_notification(notification_list):
    return notification_list[len(notification_list) - 1]

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

@service.route('/notification')
@token_required
def get_notification_by_id():
    id = get_id()
    response = None
    public_key = get_user_public_key(id)
    
    if id:
        notifications = filter_by_id(id)
    
        if notifications:
            notification = get_last_notification(notifications)
            
            response = {
                'notification' : notification['notification']
            }
        else:
            response = {
                'response' : 'no_matches'
            }
    else:
        response = {
            'response' : 'no_matches'
        }
    
    # Encrypt the data to return
    error, encrypted = encrypt(public_key, json.dumps(response, separators=(',', ':')))
    response = encrypted
    
    # If something  goes wrong with the encryption the text error will be returned
    if error:
        response = jsonify({ "result" : "Something went wrong, please try again later"})
    
    return response

if __name__ == '__main__':
    start()
    run()
