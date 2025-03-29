import socket

# Criar o socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor (localhost e porta 8888)
client_socket.connect(('localhost', 8888))

# Enviar comando para adicionar uma tarefa
#client_socket.send("1-Tarefa de rotina,Descrição de Teste".encode())  # Comando para adicionar uma tarefa
#client_socket.send("2-".encode())                                      # Comando para mostrar uma tarefa
# Enviar comando para completar uma tarefa (opção 3)
index_tarefa = 0  # Alterar para o índice da tarefa que você quer completar
client_socket.send(f"3-{index_tarefa}".encode())  # Comando para completar a tarefa

# Receber a resposta do servidor
response = client_socket.recv(1024).decode()
print("Resposta do servidor:", response)

# Fechar a conexão
client_socket.close()
