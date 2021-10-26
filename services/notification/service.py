import jwt
import json
from flask import Flask, jsonify, request
from functools import wraps


service = Flask(__name__)

DEBUG = True
NOTIFICATION_PATH = '/dictionaries/notifications.json'
KEY_PATH = '/dictionaries/config.json'
CERTIFICATE_KEY = '/certificate/key.pem'
CERTIFICATE = '/certificate/cert.pem'   
HOST = '0.0.0.0'
PORT = 5000

def start():
    global notification_list
    
    with open(NOTIFICATION_PATH, 'r') as notifications_file:
        notification = json.load(notifications_file)
        notification_list = notification['notifications']
        notifications_file.close()

def get_key():
    key = ''
    
    with open(KEY_PATH, 'r') as key_file:
        key_ = json.load(key_file)
        key = key_['key']
        key_file.close()
    
    return key

def get_id():
    token = request.args.get('token')
    
    data = jwt.decode(token, get_key(), algorithm="HS256")
    
    return data['id']

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

@service.route('/notification')
@token_required
def get_notification_by_id():    
    notifications = filter_by_id(get_id())
    
    if notifications:
        notification = get_last_notification(notifications)
        
        return jsonify({
            'notification' : notification['notification']
        })
    else:
        return jsonify({
            'response' : 'no_matches'
        })

if __name__ == '__main__':
    start()
    run()
