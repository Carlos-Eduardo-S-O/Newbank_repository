import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

PRIVATE_KEY = '/ssl_files/private_key.pem'

# Load private key from file
def load_private_key():
    private_key = None
    
    with open(PRIVATE_KEY, 'rb') as file:
        private_bytes = file.read()
        private_key = RSA.importKey(private_bytes)
        file.close()
    
    return private_key

# Decrypt a string from front-end
def decrypt(encrypted):
    error = None
    decrypted = ""
    private_key = load_private_key()
    
    try:
        cipher = PKCS1_v1_5.new(private_key)

        encrypted = base64.b64decode(encrypted)
        decrypted = cipher.decrypt(encrypted, None)
        decrypted = str(decrypted, 'utf-8')
    except Exception as e:
        error = {"error": e}

    return error, decrypted

def encrypt(plaintext):
    error = "ERROR_NONE()"
    encrypted = ""
    privateKey = load_private_key()

    try:
        cipher = PKCS1_v1_5.new(privateKey)

        encrypted = str.encode(plaintext)
        encrypted = cipher.encrypt(encrypted)
        encrypted = base64.b64encode(encrypted)
        encrypted = encrypted.decode('utf-8')
    except Exception as e:
        # error = ERROR_OTHER('erro: ' + str(e))
        error = "ERROR_UNABLE_TO_COMPLETE()"

        pass

    return error, encrypted


    