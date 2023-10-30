# Trabalho 01 - Sistemas Distribuídos

# DUPLA: `Guilherme Santos` e `Carlos Samuel`

## Comunicação entre processos

### Relatório e comentários sobre os códigos

- **Q1**
1. **Definição da Classe `Pessoa`:**
   - Aqui, é definida uma classe simples chamada `Pessoa`, que tem atributos como `nome`, `cpf` e `idade`. Esta classe representa uma entidade básica de dados.

2. **Definição da Classe `PessoasOutputStream`:**
   - Esta classe representa um fluxo de saída para uma lista de objetos `Pessoa`. Ela recebe uma lista de pessoas e um destino para a saída (como um arquivo ou uma saída padrão).

3. **Método `write` da Classe `PessoasOutputStream`:**
   - O método `write` faz a serialização dos objetos `Pessoa` e os envia para o destino. Ele segue a lógica de escrever o número de pessoas, e para cada pessoa, escrever o número de bytes do nome, o nome codificado, o CPF e a idade.

4. **Teste usando a Saída Padrão (`sys.stdout`):**
   - Aqui, é criada uma lista de pessoas e um objeto `PessoasOutputStream` que escreve para a saída padrão (`sys.stdout`). O método `write` é chamado para imprimir os dados no console.

5. **Teste usando um Arquivo (`FileOutputStream`):**
   - Um teste adicional é realizado, onde os dados são escritos em um arquivo chamado 'pessoas.bin'. O arquivo é aberto no modo de escrita binária (`'wb'`). O método `write` é chamado para gravar os dados no arquivo.

6. **Teste usando servidor TCP**:
    - Para esse teste foi criado mais um `arquivo` definido como servidor.

7. **Módulo do Servidor:**
   - A função `receber_do_cliente` no módulo do servidor é responsável por receber dados do cliente. Ela lê o número de pessoas, seguido pelos detalhes individuais de cada pessoa, decodifica os dados e realiza o processamento (neste caso, imprime as informações).

8. **Módulo do Servidor:**
   - A função `iniciar_servidor` no módulo do servidor cria um socket, vincula-o a um endereço e porta específicos, e aguarda conexões. Uma vez conectado, chama `receber_do_cliente` para processar os dados recebidos do cliente.

9. **Módulo do Cliente:**
   - A função `enviar_pessoas_para_servidor` no módulo do cliente cria um socket, conecta-se ao servidor e, em seguida, envia a lista de pessoas usando a classe `PessoasOutputStream`.

- **Q2**
1. Essa questão é um acrescimo da questão anterior, então serão abordadas as novas partes adicionadas.

2. **Método `__init__`:**
   - O método `__init__` inicializa um objeto `PessoasInputStream` com uma fonte de dados (`origem`), que pode ser um arquivo ou um soquete.

3. **Método `read`:**
   - O método `read` realiza a leitura dos dados da fonte. Ele começa lendo o número de pessoas, descompacta esse valor e, em seguida, itera sobre o número de pessoas para ler cada uma delas.
  
4. **Leitura do Número de Pessoas:**
   - `numero_pessoas` é lido da fonte usando `struct.unpack`. Este valor indica quantas pessoas estão presentes nos dados.

5. **Leitura dos Detalhes de Cada Pessoa:**
   - Em um loop, o método lê o tamanho do nome, o nome em bytes, o CPF e a idade para cada pessoa. O tamanho do nome é usado para ler corretamente a quantidade de bytes necessária para o nome.

6. **Criação da Lista de Pessoas:**
   - As informações lidas para cada pessoa são usadas para instanciar objetos `Pessoa`, que são então adicionados à lista `pessoas`.

7. **Retorno da Lista de Pessoas:**
   - A lista de pessoas construída é retornada pelo método `read`.

- **Q3**
- **Q4**