import struct
import sys

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
        self.destino.write(struct.pack('!I', len(self.pessoas)))

        for pessoa in self.pessoas:
            # Envie o número de bytes do nome
            self.destino.write(struct.pack('!I', len(pessoa.nome)))

            # Envie o nome, CPF e idade
            self.destino.write(pessoa.nome.encode())
            self.destino.write(struct.pack('!I', pessoa.cpf))
            self.destino.write(struct.pack('!H', pessoa.idade))

pessoas = [Pessoa("Alice", 123456789, 25), Pessoa("Bob", 987654321, 30)]

# Teste utilizando a saída padrão (System.out)
output_stream_stdout = PessoasOutputStream(pessoas, sys.stdout.buffer)
output_stream_stdout.write()

# ---|---

# Teste utilizando um arquivo (FileOutputStream)
with open('pessoas.bin', 'wb') as file:
    output_stream_file = PessoasOutputStream(pessoas, file)
    output_stream_file.write()