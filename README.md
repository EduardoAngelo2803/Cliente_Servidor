# Cliente_Servidor

Este projeto foi desenvolvido por estudantes da Cesar school, da disciplina de Infraestrutura de Comunicação, ministrada pelo prof Dr. Petrônio.
Tem como finalidade, desenvolver uma aplicação cliente-servidor capaz de, na camada de aplicação, fornecer uma comunicação que tenha todas as caracteristicas do transporte confiável para os dados trocados entre os sistemas finais, considerando um canal com perda de dados e erros.

Para isto, implementamos um protocolo baseano num protocolo de transferência confiável paralela, utilizando Python e sockets UDP. O objetivo é fornecer uma simulação de perda/corrupção e uma solução simples para transmitir dados confiáveis em uma rede, onde os pacotes podem ser perdidos ou corrompidos.

## Arquivos
O projeto é composto pelos seguintes arquivos:

- **client.py**: Contendo o código do cliente que envia as mensagens;
- **server.py**: Contendo o código do servidor que recebe as mensagens;

Adicionalmente por:
- **msg_utils.py**: Funções auxiliares para construir e manipular mensagens;
- **checksum_utils.py**: Funções para calcular e verificar a integridade dos dados transmitidos.

Pré-requisitos:
Os requisitos minimos para utilizar este projeto, é ter Python 3 instalado em seu computador.

## Como utilizar
1. Faça o download ou clone este repositório em sua máquina.
2. Abra dois terminais (um para o servidor e outro para o cliente).
3. No terminal do servidor, execute o seguinte comando:
```
python3 servidor.py
```
4. No outro terminal, execute o mesmo comando, agora, para o executar o codigo do cliente:
```
python3 cliente.py
```
5. Após isto, haverá a conexão entre o cliente com o servidor e os envios de mensagens (tanto simples como em pacotes) poderão ser realizados, bem como a devida simulação de perda ou corrupção, bem como a solução:

Quando em batch, o cliente envia pacotes de tamanho fixo. O servidor confirmará o recebimento de cada pacote e enviará um ACK (acknowledgment) ou um NACK (negative acknowledgment) para o cliente. Se um determinado pacote chegar corrompido, o servidor enviará um NACK e o cliente reenviará o pacote corrompido da sequencia.
Se um ACK ou NACK for perdido, o cliente reenviará o pacote. O cliente só enviará o próximo pacote quando receber um ACK do servidor.

Quando em single, o cliente enviará uma única mensagem por vez ao servidor e aguardará o recebimento do ACK correspondente antes de enviar a próxima mensagem. Caso o ACK correspondente não seja recebido, o cliente reenviará a mensagem original, após um timeout. Se a mensagem original for corrompida, o servidor enviará um NACK e o cliente reenviará a mensagem original. 
O cliente só enviará a próxima mensagem após receber o ACK correspondente do servidor para a mensagem anterior até o máximo de 3 tentativas.
