import socket
import json

class VeterinariaCliente:
    def enviar_requisicao(self, operacao, dados):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect(('192.168.0.106', 12345))

            # Montar a mensagem como um dicionário JSON
            mensagem = {"operacao": operacao, "dados": dados}
            mensagem_json = json.dumps(mensagem)

            # Enviar a mensagem
            cliente.sendall(mensagem_json.encode())

            # Receber a resposta
            pacote_resposta = cliente.recv(4096)  # Tamanho arbitrário
            resposta = pacote_resposta.decode()

            print(f"Resposta do servidor: {resposta}")

if __name__ == "__main__":
    veterinaria_cliente = VeterinariaCliente()

    # Exemplo de operação: Adicionar Animal
    animal_exemplo = {"nome": "Fido", "especie": "Cachorro", "idade": 3}
    veterinaria_cliente.enviar_requisicao("adicionar_animal", animal_exemplo)

    # Exemplo de operação: Listar Animais
    veterinaria_cliente.enviar_requisicao("listar_animais", None)