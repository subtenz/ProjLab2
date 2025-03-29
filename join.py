import os
from subprocess import run

# Função para copiar um intervalo de bytes do ficheiro origem para o ficheiro destino
def copy_binary_file(src_file, dest_file, start, end):
    with open(src_file, 'rb') as src, open(dest_file, 'wb') as dest:
        src.seek(start)
        dest.write(src.read(end - start))

# Função para juntar dois ficheiros
def join_binary_file(file1, file2, dest_file):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2, open(dest_file, 'wb') as dest:
        dest.write(f1.read())
        dest.write(f2.read())

# Função para cifrar o corpo da imagem com OpenSSL
def encrypt_body(input_file, output_file, cipher_mode):
    command = [
        'openssl', 'enc', '-aes-256-' + cipher_mode, '-in', input_file, '-out', output_file
    ]
    run(command)

# Caminhos dos ficheiros
input_image = 'c-academy.bmp'
header_file = 'header'
body_file = 'body'
output_file_ecb = 'body_enc_ecb'
output_file_cbc = 'body_enc_cbc'
output_image_ecb = 'c-academy_ecb.bmp'
output_image_cbc = 'c-academy_cbc.bmp'

# Passo 1: Separar o cabeçalho (primeiros 54 bytes) e o corpo da imagem
copy_binary_file(input_image, header_file, 0, 54)
copy_binary_file(input_image, body_file, 54, os.path.getsize(input_image))

# Passo 2: Cifrar o corpo da imagem com AES-ECB e AES-CBC
encrypt_body(body_file, output_file_ecb, 'ecb')  # Cifrar com AES-ECB
encrypt_body(body_file, output_file_cbc, 'cbc')  # Cifrar com AES-CBC

# Passo 3: Juntar cabeçalho com corpo cifrado (AES-ECB)
join_binary_file(header_file, output_file_ecb, output_image_ecb)

# Passo 4: Juntar cabeçalho com corpo cifrado (AES-CBC)
join_binary_file(header_file, output_file_cbc, output_image_cbc)

print("Cifras com sucesso: ", output_image_ecb, " e ", output_image_cbc)
