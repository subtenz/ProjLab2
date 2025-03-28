from cryptography.fernet import Fernet

key = Fernet.generate_key()
# the key is type bytes
file = open('key.fernet', 'wb')
file.write(key)
file.close()
print("key: ", key)
file.close()

f = Fernet(key)
# encrypt the message
token = f.encrypt(b"my deep dark secret")
print("token: ", token)

# decrypt the message
msg = f.decrypt(token)
print("plain text", msg)