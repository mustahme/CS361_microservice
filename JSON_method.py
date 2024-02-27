import gnupg
import os
import json
from time import sleep
from pathlib import Path

# Initialize GPG framework
gnupg_home = './gnupg_keys'
gpg_binary_path = '/opt/homebrew/bin/gpg'  # Update this path as necessary
gpg = gnupg.GPG(gnupghome=gnupg_home, gpgbinary=gpg_binary_path)

def process_request(file_path):
    """This method will process the request and assign it to the needed function"""
    with open(file_path, 'r') as f:
        request = json.load(f)

    userID = request.get('userID')
    passphrase = request.get('passphrase')
    mode = request.get('mode')
    message = request.get('message')
    keyGenerated = False

    # Ensure the user's keys exist or generate them
    if not gpg.list_keys(True, keys=userID):
        generate_keys(userID, passphrase)
        keyGenerated = True

    if mode == 'encrypt':
        encrypted_data = encrypt_message(message, userID)
        response = {
            "userID": userID,
            "passphrase": None,
            "mode": "returned_data",
            "message": encrypted_data,
            "keyGenerated": keyGenerated
        }
    elif mode == 'decrypt':
        decrypted_data = decrypt_message(message, passphrase)
        response = {
            "userID": userID,
            "passphrase": None,
            "mode": "returned_data",
            "message": decrypted_data,
            "keyGenerated": False
        }

    response_file_path = file_path.replace(".json", "_response.json")
    with open(response_file_path, 'w') as f:
        json.dump(response, f, indent=4)

    os.remove(file_path)

def generate_keys(email, passphrase):
    """This method will generate keys as needed"""
    input_data = gpg.gen_key_input(name_email=email, passphrase=passphrase)
    gpg.gen_key(input_data)

def encrypt_message(message, recipient):
    """This method will encrypt the message given to it"""
    encrypted_data = str(gpg.encrypt(message, recipients=[recipient]))
    return encrypted_data

def decrypt_message(encrypted_message, passphrase):
    decrypted_data = str(gpg.decrypt(encrypted_message, passphrase=passphrase))
    return decrypted_data

def monitor_folder(folder_path):
    while True:
        for file in os.listdir(folder_path):
            if file.endswith('_response.json') or not file.endswith('.json'):
                continue
            file_path = os.path.join(folder_path, file)
            process_request(file_path)
        sleep(5)  # Check every 5 seconds for new files

folder_path = "./watch_folder"
monitor_folder(folder_path)
