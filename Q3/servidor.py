import socket
import json

class VeterinariaServidor:
    def __init__(self):
        self.animais = []

    def processar_requisicao(self, mensagem):
        # Deserializar a mensagem JSON
        mensagem_dict = json.loads(mensagem)
        operacao = mensagem_dict["operacao"]
        dados = mensagem_dict["dados"]

        if operacao == "adicionar_animal":
            self.animais.append(dados)
            return "Animal adicionado com sucesso!"

        elif operacao == "listar_animais":
            return json.dumps(self.animais)

        else:
            return "Operação desconhecida."

    def iniciar_servidor(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.bind(('192.168.0.106', 12345))
            servidor.listen()

            print("Aguardando conexão...")

            while True:
                conn, addr = servidor.accept()
                with conn:
                    print(f"Conectado por {addr}")

                    requisicao = conn.recv(4096).decode()  # Tamanho arbitrário
                    resposta = self.processar_requisicao(requisicao)

                    # Enviar a resposta
                    conn.sendall(resposta.encode())

if __name__ == "__main__":
    veterinaria_servidor = VeterinariaServidor()
    veterinaria_servidor.iniciar_servidor()