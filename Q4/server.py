import socket
import json
import threading
import time

# Carregando os dados iniciais a partir do arquivo JSON
with open("voting_data.json", "r") as arquivo:
    dados = json.load(arquivo)

lista_candidatos = dados["candidatos"]
dados_eleitores = dados["eleitores"]
tempo_limite_votacao = 60  
tempo_inicio = time.time()

# Carregando dados de administradores a partir do arquivo JSON
with open("admins.json", "r") as arquivo_admin:
    dados_admin = json.load(arquivo_admin)
admins_lista = dados_admin["admins"]

# Função para verificar se um CPF é de um administrador
def is_admin(cpf):
    for admin in admins_lista:
        if admin["cpf"] == cpf:
            return admin
    return None

# Função para adicionar um novo candidato
def adicionar_candidato(nome_candidato):
    novo_candidato = {"id": len(lista_candidatos) + 1, "nome": nome_candidato, "votos": 0}
    lista_candidatos.append(novo_candidato)
    with open("voting_data.json", "w") as arquivo:
        json.dump(dados, arquivo)

# Função para remover um candidato pelo índice
def remover_candidato(indice_candidato):
    if 0 <= indice_candidato < len(lista_candidatos):
        candidato_removido = lista_candidatos.pop(indice_candidato)
        with open("voting_data.json", "w") as arquivo:
            json.dump(dados, arquivo)
        return candidato_removido
    return None

# Função para lidar com a conexão de um cliente
def lidar_com_cliente(cliente_soquete):
    id_eleitor = cliente_soquete.recv(1024).decode()
    admin = is_admin(id_eleitor)

    if admin:
        # Se o usuário é um administrador, permita o acesso direto às opções do administrador
        cliente_soquete.send(b"Acesso adm concedido!\n")
        cliente_soquete.send(b"Opcoes de adm:\n")
        cliente_soquete.send(b"1. Add candidato\n")
        cliente_soquete.send(b"2. Delete candidato\n")
        escolha_admin = cliente_soquete.recv(1024).decode()

        if escolha_admin == "1":
            # Adicionar candidato
            cliente_soquete.send(b"Nome do novo candidato: ")
            nome_novo_candidato = cliente_soquete.recv(1024).decode()
            adicionar_candidato(nome_novo_candidato)
            print(f"Novo candidato adicionado: {nome_novo_candidato}")
        elif escolha_admin == "2":
            # Remover candidato
            cliente_soquete.send(b"Indice do candidato que deseja deletar: ")
            try:
                indice_candidato = int(cliente_soquete.recv(1024).decode())
                candidato_removido = remover_candidato(indice_candidato)
                if candidato_removido:
                    mensagem = f"Candidato deletado: {candidato_removido['nome']}\n"
                    try:
                        cliente_soquete.send(mensagem.encode())
                    except ConnectionResetError:
                        print("Erro ao enviar mensagem ao cliente.")
                else:
                    cliente_soquete.send(b"indice de candidato invalido.\n")
            except ValueError:
                cliente_soquete.send(b"indice de candidato invalido.\n")
        else:
            cliente_soquete.send(b"Opcao de adm invalida.\n")
    elif time.time() - tempo_inicio >= tempo_limite_votacao:
        # Se o tempo de votação já acabou, envie os resultados
        resultados = {"candidatos": lista_candidatos}
        total_votos = sum(candidato["votos"] for candidato in lista_candidatos)
        vencedor = max(lista_candidatos, key=lambda x: x["votos"])
        if total_votos > 0:
            percentual_vencedor = (vencedor["votos"] / total_votos) * 100
        else:
            percentual_vencedor = 0
        resultados["total_votos"] = total_votos
        resultados["nome_vencedor"] = vencedor["nome"]
        resultados["votos_vencedor"] = vencedor["votos"]
        resultados["percentual_vencedor"] = percentual_vencedor
        cliente_soquete.send(json.dumps(resultados).encode())
    else:
        if id_eleitor not in dados_eleitores:
            cliente_soquete.send(json.dumps(lista_candidatos).encode())
            try:
                id_candidato = int(cliente_soquete.recv(1024).decode())
            except ValueError:
                id_candidato = 0
                print("Candidato desconectado antes de votar.")

            if 1 <= id_candidato <= len(lista_candidatos):
                lista_candidatos[id_candidato - 1]["votos"] += 1
                dados_eleitores[id_eleitor] = id_candidato

                # Atualizando os dados no arquivo JSON
                with open("voting_data.json", "w") as arquivo:
                    json.dump(dados, arquivo)

                cliente_soquete.send(b"Voto registrado com sucesso!\n")
            else:
                cliente_soquete.send(b"Candidato invalido!\n")
        else:
            cliente_soquete.send(b"Voce ja votou!\n")

    cliente_soquete.close()
    print(f"Conexão encerrada.")

# Configuração do servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("192.168.0.3", 12345))
servidor.listen(5)

print("Aguardando conexões...")
while True:
    cliente, addr = servidor.accept()
    print(f"Conexão recebida de {addr[0]}:{addr[1]}")
    manipulador_cliente = threading.Thread(target=lidar_com_cliente, args=(cliente,))
    manipulador_cliente.start()