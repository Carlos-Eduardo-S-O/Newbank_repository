import json
from flask import Flask, jsonify

service = Flask(__name__)

DEBUG = True
PATH = '/dictionaries/notifications.json'

def start():
    global notification_list
    
    with open(PATH, 'r') as notifications_file:
        notification = json.load(notifications_file)
        notification_list = notification['notifications']
        notifications_file.close()

def filter_by_id(id):
    global notification_list
    response = list()
    
    for notification in notification_list:
        if notification['user_id'] == id:
            response.append(notification)
    
    return response

def get_last_notification(notification_list):
    return notification_list[len(notification_list) - 1]

@service.route('/notification/<int:id>')
def get_notification_by_id(id):    
    notifications = filter_by_id(id)
    
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
    service.run(
        host='0.0.0.0',
        debug=DEBUG
    )