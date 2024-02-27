import gnupg
import os
from time import sleep
import time
from pathlib import Path


def check_text():
    try:
        f = open("watch_folder/local.txt", "r")
        current_contents = f.read()
        return current_contents
    except:
        print("Error in reading text files")
        return None


def generate_keys(email, passphrase):
    """This method generates a public and private key for PGP encryption"""

    gnupg_home = './gnupg_keys'
    gpg_binary_path = '/opt/homebrew/bin/gpg'  # Define the path correctly

    # Check if gnupghome directory exists, create if it doesn't
    if not os.path.exists(gnupg_home):
        os.makedirs(gnupg_home)
    gpg = gnupg.GPG(gnupghome=gnupg_home, gpgbinary=gpg_binary_path)
    input_data = gpg.gen_key_input(
        name_email=email,
        passphrase=passphrase,
    )
    key = gpg.gen_key(input_data)
    return str(key)


def encrypt_file(file_path, recipient):
    try:
        with open(file_path, "rb") as f:
            status = gpg.encrypt_file(
                f, recipients=[recipient],
                output=f"{file_path}.gpg"
            )
        if status.ok:
            print(f"File encrypted: {file_path}.gpg")
        else:
            print(f"Encryption failed: {status.stderr}")
    except:
        print("File may not exist in current path. Please verify file is present.")
        return


def decrypt_file(file_path, passphrase, gpg):
    try:
        with open(file_path, "rb") as f:
            status = gpg.decrypt_file(
                f,  # Corrected to directly pass the file object
                passphrase=passphrase,
                output=file_path.rstrip(".gpg")
            )
        if status.ok:
            print(f"File decrypted: {file_path.rstrip('.gpg')}")
            os.remove(file_path)  # Remove the encrypted file after decryption
        else:
            print(f"Decryption failed: {status.stderr}")
    except Exception as e:
        print(f"File decryption error: {e}")


def monitor_folder(folder_path, recipient):
    encrypted_ext = '.gpg'
    while True:
        for file in os.listdir(folder_path):
            if file.endswith(encrypted_ext) or not file.endswith('.txt'):
                continue
            file_path = os.path.join(folder_path, file)
            encrypt_file(file_path, recipient)
            # Optionally, delete the original file after encryption
            os.remove(file_path)
        sleep(5)  # Check every 5 seconds






def ensure_keys(email, passphrase):
    # Check if we already have keys
    if not list(gpg.list_keys()):
        input_data = gpg.gen_key_input(name_email=email, passphrase=passphrase)
        key = gpg.gen_key(input_data)
        return str(key)
    return list(gpg.list_keys())[0]['keyid']  # Assuming the first key is ours


# Method to check and encrypt unencrypted .txt files
def check_and_encrypt_files(folder_path, email="place@holder.com", passphrase="abcd1234"):
    recipient_key_id = ensure_keys(email, passphrase)

    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            file_path = os.path.join(folder_path, file)
            # Simplistic check: If an encrypted version does not exist, encrypt the file
            if not os.path.exists(f"{file_path}.gpg"):
                encrypt_file(file_path, email)
                print(f"Encrypted {file} with key ID: {recipient_key_id}")
            else:
                print(f"File already encrypted: {file}")


default_email = "place@holder.com"
passphrase = "your_strong_passphrase"
gpg_binary_path = '/opt/homebrew/bin/gpg'  # Update this path as necessary
gpg = gnupg.GPG(gnupghome='./gnupg_keys', gpgbinary=gpg_binary_path)

folder_path = "./watch_folder"
encrypted_file_path = "./watch_folder/example.txt.gpg"

# Uncomment the line below to generate keys, if necessary
# generate_keys(default_email, passphrase)

# Uncomment the line below to start monitoring the folder
# monitor_folder(folder_path, default_email, gpg)

# Call decrypt_file function to decrypt an encrypted file
decrypt_file(encrypted_file_path, passphrase, gpg)