import struct
import socket

def receber_do_cliente(conn):
    # Leitura do número de pessoas
    numero_pessoas = struct.unpack('!I', conn.recv(4))[0]

    for _ in range(numero_pessoas):
        # Leitura do número de bytes do nome
        tamanho_nome = struct.unpack('!I', conn.recv(4))[0]

        # Leitura do nome, CPF e idade
        nome = conn.recv(tamanho_nome).decode()
        cpf = struct.unpack('!I', conn.recv(4))[0]
        idade = struct.unpack('!H', conn.recv(2))[0]

        # Processamento dos dados (pode ser impressão, salvamento em banco de dados, etc.)
        print(f"Nome: {nome}, CPF: {cpf}, Idade: {idade}")

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('192.168.0.106', 12345))
        s.listen()

        print("Aguardando conexão...")
        conn, addr = s.accept()

        with conn:
            print(f"Conectado por {addr}")
            receber_do_cliente(conn)

if __name__ == "__main__":
    iniciar_servidor()