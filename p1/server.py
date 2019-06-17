"""
UFG-INF-Sistemas Distribuidos
Cliente MQTT usando o paho - funciona como server
Documentação: https://pypi.org/project/paho-mqtt/
Versão: V002 - 15/06/2019 
Dependencias: paho-mqtt;  (pip install -r requirements.txt)
"""

import sys
import paho.mqtt.client as mqtt
import json
from random import *
import time
from datetime import datetime
import redis

# Configurações
nclientname = 'server-'
clientname = nclientname + (str(randint(1,1000) * randint(0,9999))) 
# lendo o arquivo JSON e montando as configurações do equipamento. 
try:
	file_json = open('server_config.json', 'r')
	dados_json = json.load(file_json)
	config_json = dados_json['config']
	config_str = json.dumps(config_json)
	config_parse = json.loads(config_str)
	
	# montagem tópicos
	broker = config_parse['broker']
	tpc1 = config_parse['topic1']
	tpc =   tpc1 + "/#"  #todos os níveis deste tópico

except Exception as erro:
	print("Falha ao carregar o arquivo")
	print("Erro: {}".format(erro))
#

# Instanciando Redis
conn = redis.Redis(host='localhost', port=6379, db=0)

# Falta tratar as excessões
def on_log(client, userdata, level, buf):
	print("log: "+buf)

def on_connect(client, userdata, flags, rc):
	if rc==0:		
		print("")
	else:
		print ("falha de conexao, codigo = ",rc)

def on_disconnet (client, userdata, flags, rc=0):
	print("Desconectado, codigo"+str(rc))	

def on_message(client,userdata,msg):
	
	"""
	ATENÇÃO! VAMOS MODULARIZAR (SEPARAR)
 	- verificar permissão e capacidade
	- gravar no db_local (+/-) (atributo: ocupantes)
	- gravar no db_acessos: id, matricula, data_hora, complexo, predio, andar, catraca_porta, in_out
	"""

	# topico e msg recebida
	topic=msg.topic
	m_decode=str(msg.payload.decode("utf-8","ignore"))
	# print("msg: ["+str(msg.topic)+"]:", m_decode)
	
	# parse msg
	msg_parse = json.loads(m_decode)
	
	# organiza o local (separa tópicos em local)
	local = str(msg.topic).split('/')
	complexo =	local[1]
	predio = local[2]
	andar = local[3]
	catraca_porta = local[4]

	# organiza conteúdo da  msg
	id_msg = msg_parse['id']
	id_obj = msg_parse['id_obj_pessoa']
	data_hora = msg_parse['data_time']
	tipo_acesso = msg_parse['in_out']

	# reposta para o cliente (catraca). provisório
	matricula = input (">> ")
	user = "user:" + str(matricula)
	
	# Excluir o "replace" (ver documentação do redis-py)  
	# verifica permissão 
	if conn.exists(user):    
	    ativo = str(conn.hmget(user, 'ativo'))    
	    ativo = ativo.replace("[b'", '')
	    ativo = ativo.replace("']", '')
	    nome = str(conn.hmget(user, 'nome'))
	    nome = nome.replace("[b'", '')
	    nome = nome.replace("']", '')
	    if ativo == "S":
	        retorno1 = 'liberado'        
	    else:
	        retorno1 = 'negado'
	else:
	    retorno1 = 'não cadastrado'


	# verifica capacidade 
	complexo = "UFG" 
	predio = "CA-A"
	andar = "1"
	local_p = "local"+":"+complexo+":"+predio+":"+andar
	if conn.exists(local_p) and (retorno1 == 'liberado'):
	    capacidade = str(conn.hmget(local_p, 'capacidade'))
	    capacidade = capacidade.replace("[b'", '')
	    capacidade = capacidade.replace("']", '')
	    capacidade = int(capacidade)
	    ocupantes = str(conn.hmget(local_p, 'ocupantes'))
	    ocupantes = ocupantes.replace("[b'", '')
	    ocupantes = ocupantes.replace("']", '')
	    ocupantes = int(ocupantes)
	    if (capacidade == ocupantes):
	        retorno2 = 'lotado'
	    else:
	        retorno2 = 'livre'
	else:
	    retorno2 = 'nao encontrado'

	# verifica política
	politica = str(conn.hmget(user, 'politica'))    
	politica = politica.replace("[b'", '')
	politica = politica.replace("']", '')
	if politica != 'Administracao':
	    if retorno2 == 'livre':
	        retorno3 = 'liberado'
	    else:
	        retorno3 = 'lotado'
	else:
	    retorno3 = 'acesso livre'


	# validação
	if (retorno1 == 'liberado') and (retorno2 == 'livre' or retorno3 == 'acesso_livre'):
	    acesso = "<<liberado>>"
	elif (retorno1 == 'liberado') and (retorno2 == 'livre') and (retorno3 == 'liberado'):
	    acesso = "<<liberado>>"
	else:
	    acesso = "negado"

	print("acesso: ", acesso)
	print("permissão: ", retorno1)
	print("capacidade: ", retorno2)
	print("politica: ", retorno3)












	# Gravar no Redis: Estrutura mensagem do acesso (se liberado)
	acesso = {
				"id": id_msg, 
				"matricula": id_obj, 
				"data_hora": data_hora, 
				"complexo": complexo,
				"predio": predio,
				"andar": andar,
				"catraca_porta": catraca_porta,
				"tipo_de_acesso": tipo_acesso
			}
	# Seta a chave
	key = "acesso:" + str(id_msg)
	print ("valor chave =", key)
	conn.hmset(key, acesso)













# instanciando o cliente. 
client = mqtt.Client (clientname) 
client.on_connect=on_connect
client.on_disconnet=on_disconnet
client.on_message=on_message
print("\nConectado ao broker: ", broker)

# conectar ao broker
client.connect(broker)

# se inscreve no tópico para receber reposta do server (via broker) 
client.subscribe(str(tpc))

# inicia loop
client.loop_start()	

# Tempo conexão .
#parar loop
time.sleep(1000) 
client.loop_stop()
#desconetar cliente
client.disconnect()