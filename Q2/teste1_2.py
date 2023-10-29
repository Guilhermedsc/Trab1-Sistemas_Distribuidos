import struct
import io

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
            # Envie o nome, CPF e idade
            self.destino.write(struct.pack('!I', len(pessoa.nome)))
            self.destino.write(pessoa.nome.encode())
            self.destino.write(struct.pack('!I', pessoa.cpf))  # Corrigido para 4 bytes
            self.destino.write(struct.pack('!H', pessoa.idade))

class PessoasInputStream:
    def __init__(self, origem):
        self.origem = origem

    def read(self):
        # Leitura do número de pessoas
        numero_pessoas = struct.unpack('!I', self.origem.read(4))[0]

        pessoas = []

        for _ in range(numero_pessoas):
            # Leitura do número de bytes do nome
            tamanho_nome = struct.unpack('!I', self.origem.read(4))[0]

            # Leitura do nome
            nome_bytes = self.origem.read(tamanho_nome)
            
            # Leitura do CPF (agora corrigido para 4 bytes)
            cpf = struct.unpack('!I', self.origem.read(4))[0]

            # Leitura da idade
            idade = struct.unpack('!H', self.origem.read(2))[0]

            pessoa = Pessoa(nome_bytes.decode(), cpf, idade)
            pessoas.append(pessoa)

        return pessoas

pessoas = [Pessoa("Alice", 123456789, 25), Pessoa("Bob", 987654321, 30)]

# Teste utilizando a saída padrão (System.out)
# output_stream_stdout = PessoasOutputStream(pessoas, io.BytesIO())
# output_stream_stdout.write()

# # Obtendo bytes da saída
# saida_bytes = output_stream_stdout.destino.getvalue()

# # Teste utilizando a entrada padrão (System.in)
# input_stream_stdin = PessoasInputStream(io.BytesIO(saida_bytes))
# pessoas_lidas = input_stream_stdin.read()

# # Exibindo os dados lidos
# print("Dados lidos de System.in:")
# for pessoa in pessoas_lidas:
#     print(f"Nome: {pessoa.nome}, CPF: {pessoa.cpf}, Idade: {pessoa.idade}")

# ---|---

# Teste utilizando um arquivo (FileInputStream)
with open('Q2\pessoas.bin', 'rb') as file:
    input_stream_file = PessoasInputStream(file)
    pessoas_lidas_arquivo = input_stream_file.read()

# Exibindo os dados lidos do arquivo
print("\nDados lidos do arquivo:")
for pessoa in pessoas_lidas_arquivo:
    print(f"Nome: {pessoa.nome}, CPF: {pessoa.cpf}, Idade: {pessoa.idade}")
