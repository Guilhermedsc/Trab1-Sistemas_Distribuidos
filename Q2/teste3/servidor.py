import socket
import struct

class InputStream:
    def __init__(self, origem):
        self.origem = origem

    def read_n_bytes(self, n):
        data = b''

        while len(data) < n:
            chunk = self.origem.read(n - len(data))
            if not chunk:
                # Não há dados suficientes
                return None
            data += chunk

        return data

class PessoasInputStream(InputStream):
    def read(self):
        # Leitura do número de pessoas
        numero_pessoas_bytes = self.read_n_bytes(4)
        
        if numero_pessoas_bytes is None:
            # Não há dados suficientes para ler o número de pessoas
            print("Erro: Não há dados suficientes para ler o número de pessoas.")
            return None

        numero_pessoas = struct.unpack('!I', numero_pessoas_bytes)[0]

        pessoas = []

        for _ in range(numero_pessoas):
            # Leitura do número de bytes do nome
            tamanho_nome_bytes = self.read_n_bytes(4)

            if tamanho_nome_bytes is None:
                print("Erro: Não há dados suficientes para ler o tamanho do nome.")
                return None

            tamanho_nome = struct.unpack('!I', tamanho_nome_bytes)[0]

            # Leitura do nome
            nome_bytes = self.read_n_bytes(tamanho_nome)

            if nome_bytes is None:
                print("Erro: Não há dados suficientes para ler o nome.")
                return None

            # Leitura do CPF (agora corrigido para 4 bytes)
            cpf_bytes = self.read_n_bytes(4)

            if cpf_bytes is None:
                print("Erro: Não há dados suficientes para ler o CPF.")
                return None

            cpf = struct.unpack('!I', cpf_bytes)[0]

            # Leitura da idade
            idade_bytes = self.read_n_bytes(2)

            if idade_bytes is None:
                print("Erro: Não há dados suficientes para ler a idade.")
                return None

            idade = struct.unpack('!H', idade_bytes)[0]

            pessoa = {"nome": nome_bytes.decode(), "cpf": cpf, "idade": idade}
            pessoas.append(pessoa)

        return pessoas

    def read_n_bytes(self, n):
        data = b''

        while len(data) < n:
            chunk = self.origem.read(n - len(data))
            if not chunk:
                # Não há dados suficientes
                return None
            data += chunk

        return data

def receber_do_cliente(conn):
    # Leitura do stream de pessoas
    input_stream_servidor = PessoasInputStream(conn.makefile('rb'))
    pessoas_lidas = input_stream_servidor.read()

    if pessoas_lidas is not None:
        # Processamento dos dados
        print("Dados recebidos do cliente:")
        for pessoa in pessoas_lidas:
            print(f"Nome: {pessoa['nome']}, CPF: {pessoa['cpf']}, Idade: {pessoa['idade']}")
            
        # Enviar os dados de volta para o cliente (opcional)
        enviar_para_cliente(conn, pessoas_lidas)

def enviar_para_cliente(conn, pessoas):
    # Criação do OutputStream
    from output_stream import PessoasOutputStream
    
    # Envio do stream de pessoas
    output_stream_tcp = PessoasOutputStream(pessoas, conn.makefile('wb'))
    output_stream_tcp.write()

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 12345))
        s.listen()

        print("Aguardando conexão...")
        conn, addr = s.accept()

        with conn:
            print(f"Conectado por {addr}")
            receber_do_cliente(conn)

if __name__ == "__main__":
    iniciar_servidor()
