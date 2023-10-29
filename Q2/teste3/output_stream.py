import struct

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
