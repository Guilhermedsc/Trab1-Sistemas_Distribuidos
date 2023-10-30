import socket
import json

# Função para exibir a lista de candidatos
def exibir_candidatos(candidatos):
    print("Candidatos disponíveis:")
    for candidato in candidatos:
        print(f"{candidato['id']}. {candidato['nome']}")

# Função para exibir os resultados das eleições
def exibir_resultados(resultados):
    print("Eleições já encerradas!")
    print("\nResultados das eleições:")
    for candidato in resultados["candidatos"]:
        print(f"{candidato['nome']}: {candidato['votos']} votos")
    print(f"Total de votos: {resultados['total_votos']} votos")
    print(f"Vencedor: {resultados['nome_vencedor']} com {resultados['votos_vencedor']} votos ({resultados['percentual_vencedor']:.2f}% dos votos)")

# Configuração do cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("192.168.0.3", 12345))

try:
    id_eleitor = input("Digite seu CPF: ")
    cliente.send(id_eleitor.encode())
    resposta = cliente.recv(1024).decode()

    if resposta:
        if "Acesso de administrador concedido!" in resposta:
            # O usuário é um administrador
            print("Acesso adm concedido!")
            print("Opções de adm:")
            print("1. Add candidato")
            print("2. Delete candidato")
            escolha_admin = input("Escolha uma opção de adm: ")
            cliente.send(escolha_admin.encode())

            if escolha_admin == "1":
                # Adicionar candidato
                nome_novo_candidato = input("Nome do novo candidato: ")
                cliente.send(nome_novo_candidato.encode())
                resposta = cliente.recv(1024).decode()
                print("Candidato adicionado com sucesso!")
            elif escolha_admin == "2":
                # Remover candidato
                indice_candidato = input("Digite o índice do candidato que deseja deletar: ")
                cliente.send(indice_candidato.encode())
                resposta = cliente.recv(1024).decode()
                print("Candidato deletado com sucesso!")
        else:
            try:
                candidatos = json.loads(resposta)
                if "nome_vencedor" in candidatos:
                    # Se a resposta inclui o nome do vencedor, então são os resultados
                    exibir_resultados(candidatos)
                else:
                    exibir_candidatos(candidatos)

                    # Escolha do candidato
                    id_candidato = int(input("Número do candidato que deseja votar: "))
                    cliente.send(str(id_candidato).encode())

                    resposta = cliente.recv(1024).decode()
                    print(resposta)
            except json.decoder.JSONDecodeError:
                print("Você já votou!")
    else:
        print("Erro na conexão com o servidor.")
except ConnectionRefusedError:
    print("Não foi possível conectar ao servidor!")
finally:
    cliente.close()