    
#!/usr/bin/python
# -- coding: utf-8 --

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
host_redis = 'localhost'
port_redis = 6379
nclientname = 'server-'
clientname = nclientname + (str(randint(1,1000) * randint(0,9999))) 
# Lendo o arquivo JSON e montando as configurações do equipamento. 
try:
	file_json = open('server_config.json', 'r')
	dados_json = json.load(file_json)
	config_json = dados_json['config']
	config_str = json.dumps(config_json)
	config_parse = json.loads(config_str)
	
	# Montagem dos tópicos
	broker = config_parse['broker']
	tpc1 = config_parse['topic1']
	tpc =   tpc1 + "/#"  #todos os níveis deste tópico

except Exception as erro:
	print("Falha ao carregar o arquivo")
	print("Erro: {}".format(erro))

# Instanciando Redis
conn = redis.Redis(host=host_redis, port=port_redis, db=0)



# def's
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


###### REFATORAR (código longo com muitas responsabilidade) ######
def on_message(client,userdata,msg):		

	# Topico e msg recebida
	topic = msg.topic
	m_decode = str(msg.payload.decode("utf-8","ignore"))
	
	# INICIO 'processa mensagem'

	# Inicio: formata mensagem
	msg_parse = json.loads(m_decode)
	id_msg = msg_parse['id']
	id_obj = msg_parse['id_obj_pessoa']
	data_hora = msg_parse['data_time']
	tipo_acesso = msg_parse['in_out']

	tpc_tipo = topic.split("/")[0]
	complexo = topic.split("/")[1]
	predio = topic.split("/")[2]
	andar = topic.split("/")[3]
	catraca_porta = topic.split("/")[4]

	local_a = complexo +":"+ predio +":"+ andar #leitura equipamento
	local_read = "local:" + local_a	#monta chave local (lida)	
	user = "user:" + str(id_obj)	#monta chave usuário (lida)
	
	print("\n** LEITURA **")
	print(local_read, user)
	print("tipo: ", tpc_tipo)
	print("complexo: ", complexo)
	print("predio: ", predio)
	print("andar: ", andar)
	print("equipamento: ", catraca_porta)
	print("conteudo (msg): ", id_msg, id_obj, data_hora, tipo_acesso, "\n")
	
	# Fim: formata mensagem

	# CÓDIGOS DE RESPOSTAS
	resposta = {
            "000": "LIBERADO", 
            "001": "BLOQUEADO: usuário inativo!", 
            "002": "BLOQUEADO: local cheio!",
            "003": "BLOQUEADO: local não permitido",
            "201": "ERRO: politica não cadastrada!", 
            "202": "ERRO: local não cadastrado!",
            "203": "ERRO: usuário não cadastrado!"
        }

	# Verificação 1: verifica se local está no bd
	if conn.exists(local_read):
		test_local = 0 
	else:
	    test_local = 1 # erro: local não cadastrado
	
	# Verificação 2: verifica se user existe e está ativo no bd
	if conn.exists(user):	#verifica a chave se existe
		# verifica se usuário está ativo
		ativo = ((conn.hmget(user, 'ativo'))[0]).decode('utf-8')
		nome = ((conn.hmget(user, 'nome'))[0]).decode('utf-8') 
		local_cad = ((conn.hmget(user, 'complexo'))[0]).decode('utf-8') +":"+ ((conn.hmget(user, 'predio'))[0]).decode('utf-8') +":"+ ((conn.hmget(user, 'andar'))[0]).decode('utf-8')
		if ativo == "S": 
			test_ativo = 0
		else: 
			test_ativo = 1			
	else:
	    test_ativo = 1 # não localizado
	    client.publish(topic, resposta['203'])
	
	# Verificação 3: capacidade
	if test_local == 0: #positivo
		capacidade = int(((conn.hmget(local_read, 'capacidade'))[0]).decode('utf-8'))
		ocupantes = int(((conn.hmget(local_read, 'ocupantes'))[0]).decode('utf-8'))
		if capacidade > ocupantes:
			test_capacidade = 0
		else:
			test_capacidade = 1
	
	# Verificação 4: política	
	politica = "politica:"+((conn.hmget(user, 'politica'))[0]).decode('utf-8')
	if conn.exists(politica):	#verifica a chave se existe
		test_politica = 0
		acesso_livre = ((conn.hmget(politica, 'acesso_livre'))[0]).decode('utf-8')
		limitado_por_capacidade = ((conn.hmget(politica, 'limitado_por_capacidade'))[0]).decode('utf-8')
	else:
		test_politica = 1
	
	# Validação (verificação 1 a 4)
	if	test_local == 0: 					#existência de local
		if test_ativo == 0: 				#existencia de usuario (ativo)
			if test_politica == 0: 			#existencia de politica
				if 	acesso_livre == "S" and limitado_por_capacidade == "N":
					retorno = resposta['000']
				elif acesso_livre == "S" and limitado_por_capacidade == "S":
					if test_capacidade == 0:						
						retorno = resposta['001']
					else:
						retorno = resposta['002'] 
				elif acesso_livre == "N" and limitado_por_capacidade == "N":
					if local_a == local_cad:
						retorno = resposta['000']
					else:
						retorno = resposta['003']
				elif acesso_livre == "N" and limitado_por_capacidade == "S":
					if local_a == local_cad:
						if test_capacidade == 0:
							retorno = resposta['000']
						else:
							retorno = resposta['002']
					else:
						retorno = resposta['003']
				else:
					retorno = ""
			else:
				retorno = resposta['201']	
		else:
			retorno = resposta['001']
	else:
		retorno = resposta['202']

	# ----------------------
	# FIM 'processa mensagem'

	
	# Envia resposta
	if len(retorno) > 1:		
		client.publish(topic, retorno)
	else:
		client.publish(topic, "SEM RESPOSTA")

	# Se liberado atualiza os acessos e numero de ocupantes do andar
	if retorno == resposta['000']:		
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
		# Adiciona acesso
		key = "acesso:" + str(id_obj) +":"+ str(id_msg)
		print ("valor chave =", key)
		conn.hmset(key, acesso)
		
		# Atualiza o numero de ocupantes do andar
		tp = tipo_acesso
		update_local = "local:" + acesso ['complexo'] + ":" + acesso ['predio'] + ":" + acesso ['andar']
		update_chave = 'ocupantes'
		if tp == "in": 
			update_valor = 1
		else:
			update_valor = -1		
		conn.hincrby(update_local, update_chave, update_valor)

		# gerar alerta de andar com capacidade exedida - fazer loop monitorar/ prédio e andar	
		# criar topico alertas e publicar (em cliente-monitor?)



# Instanciando o cliente mqtt
client = mqtt.Client (clientname) 
client.on_connect=on_connect
client.on_disconnet=on_disconnet
client.on_message=on_message
print("\nConectado ao broker: ", broker)

# Conecta ao broker
client.connect(broker)

# Assina o tópico para receber reposta do broker 
client.subscribe(str(tpc))

# inicia loop
client.loop_start()	

# Tempo conexão .
#parar loop
time.sleep(999999) 
client.loop_stop()
#desconetar cliente
client.disconnect()
