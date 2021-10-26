import json
from flask import Flask, jsonify

service = Flask(__name__)

DEBUG = True
PATH = '/dictionaries/users.json'

def start():
    global users_list
    
    with open(PATH, 'r') as users_file:
        users = json.load(users_file)
        users_list = users["users"]
        users_file.close()

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

@service.route('/authenticate/<string:login>/<string:password>')
def authenticate(login, password):
    
    is_authenticated = 'unauthenticated'
    
    response, user_id = find_right_user(login, password)
    if response:
        is_authenticated = 'authenticated'
        
    return jsonify({
        "result" : is_authenticated, 
        "id" : user_id
    }) 

if __name__ == '__main__':
    start()
    service.run(
        host='0.0.0.0',
        debug=DEBUG
    )