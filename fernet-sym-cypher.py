from cryptography.fernet import Fernet

# Gerar a chave
key = Fernet.generate_key()

# Gravar a chave no ficheiro 'key.fernet'
with open('key.fernet', 'wb') as file:
    file.write(key)

print("Chave gerada e guardada em 'key.fernet'")
