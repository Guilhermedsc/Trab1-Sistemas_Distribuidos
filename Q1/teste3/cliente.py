import socket
import struct
class Pessoa:
    def __init__(self, nome, cpf, idade):
        self.nome = nome
        self.cpf = cpf
        self.idade = idade

class PessoasOutputStream:
    def __init__(self, pessoas, destino):
        self.pessoas = pessoas
        self.destino = destino

    def write(self):
        # Envie o número de pessoas
        numero_pessoas = len(self.pessoas)
        self.destino.write(struct.pack('!I', numero_pessoas))

        for pessoa in self.pessoas:
            # Envie o nome, CPF e idade
            self.destino.write(struct.pack('!I', len(pessoa.nome)))
            self.destino.write(pessoa.nome.encode())
            self.destino.write(struct.pack('!I', pessoa.cpf))
            self.destino.write(struct.pack('!H', pessoa.idade))

def enviar_pessoas_para_servidor(pessoas):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12345))

        # Envio do stream de pessoas
        output_stream_tcp = PessoasOutputStream(pessoas, s.makefile('wb'))
        output_stream_tcp.write()

def criar_pessoas_de_teste():
    return [Pessoa("Alice", 123456789, 25), Pessoa("Bob", 987654321, 30)]

if __name__ == "__main__":
    pessoas_teste = criar_pessoas_de_teste()
    enviar_pessoas_para_servidor(pessoas_teste)