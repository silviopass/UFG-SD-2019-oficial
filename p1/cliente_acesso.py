"""
UFG-INF-Sistemas Distribuidos
Cliente MQTT usando o paho (porta de acesso - catraca)
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

# Configurações
nclientname = 'client-'
clientname = nclientname + (str(randint(1,1000) * randint(0,9999))) 
# lendo o arquivo JSON e montando as configurações do equipamento. 
try:
	file_json = open('client_config.json', 'r')
	dados_json = json.load(file_json)
	config_json = dados_json['config']
	config_str = json.dumps(config_json)
	config_parse = json.loads(config_str)
	
	# montagem tópicos
	broker = config_parse['broker']
	tpc_base = config_parse['tpc_base']
	tpc_1 = config_parse['local1']
	tpc_2 = config_parse['local2']
	tpc_3 = config_parse['local3']
	hard_name = config_parse['hard_name']
	tpc =  tpc_base +"/"+ tpc_1 +"/"+ tpc_2 +"/" + tpc_3 +"/"+ hard_name

except Exception as erro:
	print("Falha ao carregar o arquivo")
	print("Erro: {}".format(erro))
#  

# Falta tratar as excessões e ocultar a própria mensagem
def on_log(client, userdata, level, buf):
	print("log: "+buf)

def on_connect(client, userdata, flags, rc):
	if rc==0:		
		print("")
	else:
		print ("falha de conexao, codigo = ",rc)

def on_disconnet (client, userdata, flags, rc=0):
	print("Desconectado, codigo" + str(rc))	

def on_message(client,userdata,msg):
	topic=msg.topic
	m_decode=str(msg.payload.decode("utf-8","ignore"))
	#print("msg: ["+str(msg.topic)+"]:", m_decode)
	print(m_decode)
	print(">>")

# instanciando o cliente. 
client = mqtt.Client (clientname) 
client.on_connect=on_connect
client.on_disconnet=on_disconnet
#client.on_log=on_log #ativar recebimento de logs
client.on_message=on_message  #ativar recebimento de mensagem (inclui a própria mensagem, tratar isso)
print("\nConectado ao broker: ", broker)

# conectar ao broker
client.connect(broker)

# inicia loop
client.loop_start()	

# se inscreve no tópico para receber reposta do server
client.subscribe(str(tpc))

# Entrada de dados (acesso) --> modularizar depois, usar loop e sleep
print(" \n ... Aguardando  matricula ... ")
cnt = 1
while(cnt > 0):
	
	msg_acess_mt = input("\n>> ")
	msg_acess_in_out = input(">> Entrada = 'in'  ou  saída = 'out': ")
	while (msg_acess_in_out != 'in') & (msg_acess_in_out != 'out'):
		msg_acess_in_out = input(">> Valor inválido, digite novamente 'in' ou 'out': ")
	data_e_hora_atuais = datetime.now()
	data_e_hora_str = data_e_hora_atuais.strftime('%Y/%m/%d %H:%M:%S')
	
	# Montando a mensagem (vem da configuração do equipamento config.json)
	msg_acess_comp = {}
	msg_acess_comp ['id'] = (randint(1,100)*randint(0,999)) #id aleatorio
	msg_acess_comp ['id_obj_pessoa'] = msg_acess_mt
	msg_acess_comp ['data_time'] = data_e_hora_str
	msg_acess_comp ['in_out'] = msg_acess_in_out
	
	# convert to JSON:
	msg_env = json.dumps(msg_acess_comp)
	
	# publica no tópico
	client.publish(tpc, str(msg_env)) 

	#print("\n")

"""
time.sleep(200) 
client.loop_stop()
client.disconnect()
"""