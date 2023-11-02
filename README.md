# Trabalho 01 - Sistemas Distribuídos

## Dupla: `Guilherme Santos` e `Carlos Samuel`

## Comunicação entre processos

### Relatório e comentários sobre os códigos

### **Q1**
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

### **Q2**
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

### **Q3**
**Servidor (VeterinariaServidor):**
1. **`__init__`:** Inicializa o servidor com uma lista vazia de animais.
2. **`processar_requisicao`:** Recebe uma mensagem (JSON), a deserializa e executa a operação solicitada. Suporta "adicionar_animal" e "listar_animais".
3. **`iniciar_servidor`:** Configura e inicia o servidor socket. Aguarda conexões, recebe requisições, processa e envia respostas.

**Cliente (VeterinariaCliente):**
1. **`enviar_requisicao`:** Cria uma conexão socket com o servidor, monta uma mensagem JSON com a operação e dados, envia a mensagem, recebe e imprime a resposta do servidor.

**Funcionamento Geral:**
1. **Adicionar Animal:**
   - Cliente cria um dicionário representando um animal.
   - Cliente chama `enviar_requisicao` com a operação "adicionar_animal" e os dados do animal.
   - Servidor recebe, processa e adiciona o animal à lista.

2. **Listar Animais:**
   - Cliente chama `enviar_requisicao` com a operação "listar_animais".
   - Servidor recebe, processa e retorna a lista de animais em formato JSON.
   - Cliente imprime a resposta do servidor.

**Notas Adicionais:**
- A comunicação entre cliente e servidor é feita via socket.
- As mensagens são serializadas em JSON para facilitar a comunicação e interpretação.
- A comunicação é iniciada pelo cliente, que envia uma operação e dados para o servidor.
- O servidor processa a requisição e retorna uma resposta ao cliente.
- O exemplo usa a operação "adicionar_animal" para inserir um animal e "listar_animais" para obter a lista de animais.

### **Q4**
**Cliente:**
1. **`exibir_candidatos`:** Função para exibir a lista de candidatos recebida como parâmetro.
2. **`exibir_resultados`:** Função para exibir os resultados das eleições recebidos como parâmetro.
3. **Configuração do Cliente:**
   - Cria um socket cliente e estabelece conexão com o servidor.
   - Solicita o login do eleitor.
   - Envia o login ao servidor e aguarda a resposta.
   - Interpreta a resposta do servidor:
     - Se for "Acesso de administrador concedido!", permite operações de administração.
     - Se for uma lista de candidatos, exibe os candidatos e permite ao eleitor votar.
     - Se contiver resultados, exibe os resultados.

**Servidor:**
1. **`__init__`:** Inicializa o servidor com dados iniciais a partir do arquivo JSON.
2. **`is_admin`:** Verifica se um login pertence a um administrador.
3. **`adicionar_candidato`:** Adiciona um novo candidato à lista de candidatos e atualiza o arquivo JSON.
4. **`remover_candidato`:** Remove um candidato pelo índice da lista e atualiza o arquivo JSON.
5. **`lidar_com_cliente`:** Lida com a conexão de um cliente, processa operações de administração, votação ou mensagens informativas.
6. **Configuração do Servidor:**
   - Cria um socket servidor e aguarda conexões.
   - Para cada conexão recebida, cria uma thread para lidar com o cliente.
   - Controla o tempo de votação e envia resultados quando o tempo expira.

**Funcionamento Geral:**
1. **Operações de Administração (Cliente):**
   - Se "Acesso de administrador concedido!", o cliente pode realizar operações de administração.
   - Operações incluem "1. Add candidato" e "2. Delete candidato".
   - Adiciona ou remove candidatos conforme a escolha do administrador.

2. **Operações de Eleição (Cliente):**
   - Se a resposta contém uma lista de candidatos, o cliente pode votar em um candidato.
   - Se a resposta contém resultados, exibe os resultados das eleições.

3. **Operações de Administração (Servidor):**
   - Verifica se o login pertence a um administrador.
   - Adiciona ou remove candidatos.
   - Envia lista de candidatos para votação.
   - Recebe votos, atualiza dados e envia resultados quando a votação é encerrada.

4. **Operações de Mensagens Informativas (Servidor):**
   - Admins podem enviar mensagens informativas para os eleitores durante a votação.