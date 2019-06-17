# Disciplina Sistemas de Distribuídos

# Instalação
### Broker: Mosquitto (opcional, se usar broker online)
    wwww.mosquitto.org 
### Redis 
    https://redis.io/
### Pacotes Python
#### Redis
    pip install redis
#### Paho MQTT
    pip install redis 



# Execução
Siga os passos abaixo para execução

### Executar o Redis (servidor de dados)
    redis-server

### Excutar o Mosquitto (é opcional, ser for usar broker online não é necessário)
    mosquitto  -v

### Excutar o sever (server mqtt)
    python server.py

### Excutar o cliente-adm (opcional: apenas para cadastrar usuários, locais e políticas)
Provisoriamente instanciar manualmente usando o arquivo 'instanciar.py'
    python instanciar.py

### Excutar o cliente_acesso (cliente mqtt, faz o papel de catraca ou ponto de acesso)
    python cliente_acesso.py
