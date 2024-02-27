import json
import time
from pathlib import Path

# Define the folder where requests are monitored
watch_folder = Path("./watch_folder")

# Function to create a request JSON file
def create_request(user_id, passphrase, mode, message, filename):
    request_data = {
        "userID": user_id,
        "passphrase": passphrase,
        "mode": mode,
        "message": message
    }
    file_path = watch_folder / filename
    with file_path.open('w') as file:
        json.dump(request_data, file)
    print(f"Created {mode} request: {filename}")

user_id = "John@gmail.com"
passphrase = "1234abcd"
message = "Encrypt this message for CS361"

# Create an encryption request
create_request(user_id, passphrase, "encrypt", message, "encryption_request.json")

# Wait for 30 seconds before creating a decryption request
time.sleep(20)

# Assuming the encryption service renames or moves files after processing,
# the name for the decryption request needs to be different or the file needs to be recreated.
message = "-----BEGIN PGP MESSAGE-----\n\nhQEMA2ymsDSgzeYmAQgAmh2oHmtHZ6XkabV9bjmkcqVVQrm5/KyTVTr354GLFo21\nC3wdVr0d91xJTymAlC+FzIaulQdBT8pDdVOXgQcFdEkJCFZ4FNRizSZrXrZEQgcV\nW0Hgv9fBGcJ5a4dxeNqD8hbW8PjwGGml81uJzR5cTnUswuxyhOyd9wz1WkD5EcQW\nv2+zVu01DoGtyERC8U8f2G9Kive2CBs12nzx7BVB8U9qKgKadFE8m94JBLso3Onk\n4d68zdlHFsOmBI1USKG/DzFKE4WnngHo1xzIYgtpzTFl45v6L6Kq05zq06WlWIhD\nyoCW0QPRSXBvVRIAZd4+zjPqeLUVu7TuEURzq4WVztRjAQkCEIGUAeRkyTb7POs2\njvkP5gy+694p89e+YwIaCgIPonW6ObcqdYGHKdmMAnyFDnuKphmnaXQXcTnXgurU\nKEQUpoVs9a6fIOmLNkCZnBO2j/c2Lj8kIhbhrgLPPmbzHFwX\n=yB8i\n-----END PGP MESSAGE-----\n"
create_request(user_id, passphrase, "decrypt", message, "decryption_request.json")
