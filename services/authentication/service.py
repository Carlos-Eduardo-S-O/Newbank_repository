import jwt
import datetime
import json
from flask import Flask, request
from cipher import decrypt, encrypt
from urllib.parse import unquote
import mysql.connector as mysql

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

# Database info
MYSQL_SERVER = "database"
MYSQL_USER = "root"
MYSQL_PASS = "admin"
MYSQL_BASE_NAME = "newbank"

def get_bd_connection():
    connection = mysql.connect(
        host=MYSQL_SERVER, user=MYSQL_USER, password=MYSQL_PASS, database=MYSQL_BASE_NAME
    )
    return connection

def get_key():
    key = ''
    
    with open(KEY_PATH, 'r') as key_file:
        key_ = json.load(key_file)
        key = key_["key"]
        key_file.close()
    
    return key

def find_right_user(login, password):
    connection = get_bd_connection()
    
    cursor = connection.cursor(dictionary=True)
    
    query = f"SELECT id, publickey FROM user_login WHERE login = '{login}' AND password = '{password}'"
    cursor.execute(query)
    
    result = cursor.fetchone()
    
    if result:
        return True, result["id"], result["publickey"]
    else:
        return False, None, None

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
            token = jwt.encode({'id' : user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5000)}, get_key(), algorithm="HS256")
            
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
    run()
