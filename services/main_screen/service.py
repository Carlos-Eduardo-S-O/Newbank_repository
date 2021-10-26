import json
from flask import Flask, jsonify

service = Flask(__name__)

DEBUG = True
PATH = '/dictionaries/users.json'

def start():
    global users_list
    
    with open(PATH, 'r') as users_file:
        users = json.load(users_file)
        users_list = users['users']
        users_file.close()

def filter_by_id(id):
    global users_list
    response = None
    
    for user in users_list:
        if user['id'] == id:
            response = user
            break
    
    return response

@service.route('/main/<int:id>')
def get_main_screen_data(id):    
    user = filter_by_id(id)
    
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
    service.run(
        host='0.0.0.0',
        debug=DEBUG
    )
