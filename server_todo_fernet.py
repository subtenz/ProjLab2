import socket
from cryptography.fernet import Fernet

# Classe que representa um item de todo (tarefa)
class TodoItem:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

# Classe que representa uma lista de TodoItems
class TodoList:
    def __init__(self):
        self.items = []

    def add_item(self, title, description):
        item = TodoItem(title, description)
        self.items.append(item)

    def complete_item(self, index):
        if index < 0 or index >= len(self.items):
            raise IndexError("Índice inválido")
        item = self.items[index]
        item.completed = True

    def count_items(self):
        return len(self.items)

    def save_cipher(self, key):
        cipher = Fernet(key)
        with open('todo_list.fernet', 'w') as file:
            for item in self.items:
                plain_item = f"{item.title},{item.description},{item.completed}"
                c_item = cipher.encrypt(plain_item.encode()).decode()  # cifrando a tarefa
                file.write(f"{c_item}\n")

    def get_list_of_items(self):
        result = ""
        for i, item in enumerate(self.items):
            status = "[ ]"
            if item.completed:
                status = "[x]"
            result += f"{i}. {status} {item.title}: {item.description}\n"
        return result

# Configuração do servidor
host = 'localhost'
port = 8888

# Carregar a chave
with open('key.fernet', 'rb') as key_file:
    key = key_file.read()
    print("Chave carregada: ", key)

# Carregar as tarefas do ficheiro cifrado, se existir
todo_list = TodoList()
try:
    with open('todo_list.fernet', 'r') as file:
        for line in file:
            cipher = Fernet(key)
            c_item = line.strip()
            print("A tentar decifrar: ", c_item)
            try:
                plain_item = cipher.decrypt(c_item.encode()).decode()  # decifrando
                print("Decifrado: ", plain_item)
                title, description, completed = plain_item.split(",")
                completed = completed.lower() == 'true'  # Convertendo para booleano
                todo_list.add_item(title, description)
                todo_list.items[-1].completed = completed
            except Exception as e:
                print(f"Erro ao decifrar: {e}")
except FileNotFoundError:
    print("Ficheiro 'todo_list.fernet' não encontrado. Criando uma nova lista.")

# Criar o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Servidor iniciado na porta {port}...")
print("Servindo a lista de tarefas...")

# Loop para esperar conexões e processar comandos
while True:
    print("Aguardando conexão...")
    client_socket, address = server_socket.accept()
    print(f"Conectado a {address}")

    # Receber comando do cliente
    command = client_socket.recv(1024).decode()
    print(f"Comando recebido: {command}")
    choice, data = command.split("-")
    
    if choice == "1":
        # Adicionar tarefa
        title, description = data.split(",")
        todo_list.add_item(title, description)
        result = "Tarefa adicionada."
    elif choice == "2":
        # Mostrar tarefas
        result = todo_list.get_list_of_items()
    elif choice == "3":
        # Completar tarefa
        index = int(data)
        todo_list.complete_item(index)
        result = "Tarefa completada."
    else:
        result = "Comando inválido."

    print("Log: " + result)
    client_socket.send(result.encode())
    client_socket.close()

    # Salvar tarefas cifradas
    todo_list.save_cipher(key)
