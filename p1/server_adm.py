#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
UFG-INF-Sistemas Distribuidos
Trabalho final da disciplina
Versão: V002 - 18/07/2019
Dependencias:(pip install -r requirements.txt)
"""

#Packs
import sys
import paho.mqtt.client as mqtt
import time
from datetime import datetime

import redis
conn = redis.Redis('localhost')

import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

cls()

data_e_hora_atuais = datetime.now()
data_e_hora_str = data_e_hora_atuais.strftime('%H:%M:%S %d/%m/%Y')

# Definicão do broker (server). Opções online: test.mosquitto.org; iot.eclipse.org ou outro qualquer
broker_init = "test.mosquitto.org"

# broker = input("Informe o broker, sugestão: 'test.mosquitto.org' ou ENTER  para localhost: ")
broker = broker_init

# nclientname = input("Informe o número da catraca/porta de acesso: ")
nclientname = 'cliente'
clientname = nclientname + '-' + str(datetime.now()) 

# o datatime é só para não criar cliente com nomes iguais. "gamb" (arrumar uma forma mais elegante)
tpc_base = "projetosd:teste"
tpc = str(tpc_base)

def on_log(client, userdata, level, buf):
	print("log: "+buf)

def on_connect(client, userdata, flags, rc):
	if rc==0:
		rc = 0
	else:
		print ("falha de conexao, codigo = ",rc)

def on_disconnet (client, userdata, flags, rc=0):
	print("Desconectado, codigo"+str(rc))	

def on_message(client,userdata,msg):
	topic    = msg.topic
	m_decode = str(msg.payload.decode("utf-8","ignore"))
	
	print("Mensagem recebida: ",m_decode)
	print("Cliente: ",client)
	print("Topico: ", topic)

	data_e_hora_atuais = datetime.now()
	data_e_hora_str    = data_e_hora_atuais.strftime('%H:%M:%S %d/%m/%Y')
	print("Horario: ", data_e_hora_str)

	##################### Inicio operações com Redis #######################
	operacao = int(m_decode[0])

	if operacao == 1:
		operacao, id_politica, nome, acesso_livre, limitado_por_capacidade = m_decode.split('#')

		politica = {"id_politica": id_politica,
					"nome": nome,
					"acesso_livre": acesso_livre,
					"limitado_por_capacidade": limitado_por_capacidade}

		conn.hmset("politica:" + id_politica, politica)

		print("Comando para consulta no Redis: hgetall politica:" + id_politica)

	elif operacao == 2:
		operacao, id_matricula, nome, politica, complexo, predio, andar, ativo = m_decode.split('#')

		user = {"id_matricula": id_matricula,
				"nome": nome,
				"politica": politica,
				"complexo": complexo,
				"predio": predio,
				"andar": andar,
				"ativo": ativo}

		conn.hmset("user:" + id_matricula, user)

		print("Comando para consulta no Redis: hgetall user:" + id_matricula)

	elif operacao == 3:
		operacao, matricula, predio, andar, tipo_de_acesso = m_decode.split('#')

		acesso = {"matricula": matricula,
				  "predio": predio,
				  "andar": andar,
				  "tipo_de_acesso": tipo_de_acesso}

		conn.hmset("acesso:" + matricula, acesso)

		print("Comando para consulta no Redis: hgetall acesso:" + matricula)

	elif operacao == 4:
		operacao, id, nome, numero_de_andares, capacidade_de_pessoas_por_andar = m_decode.split('#')

		predio = {"id": id,
				  "nome": nome,
				  "numero_de_andares": numero_de_andares,
				  "capacidade_de_pessoas_por_andar": capacidade_de_pessoas_por_andar}

		conn.hmset("predio:" + id, predio)

		print("Comando para consulta no Redis: hgetall predio:" + id)

	elif operacao == 5:
		operacao, id_local, complexo, predio, andar, capacidade, ocupantes = m_decode.split('#')

		local = {"id_local": id_local,
				 "complexo": complexo,
				 "predio": predio,
				 "andar": andar,
				 "capacidade": capacidade,
				 "ocupantes": ocupantes}

		conn.hmset("local:" + complexo + ":" + predio + ":" + andar, local)

		print("Comando para consulta no Redis: hgetall local:" + complexo + ":" + predio + ":" + andar)

	elif operacao == 6:
		print("Operacao 6 sendo executada")


	##################### Final operações com Redis #######################

	print("-------------------------------------------------------------------------------")

# instanciando o cliente. 
client = mqtt.Client (clientname) 
client.on_connect = on_connect
client.on_disconnet = on_disconnet
client.on_message = on_message

print("Conectado no broker", broker)
print("Horario: ", data_e_hora_str)

print("\n                             RECEBENDO MENSAGENS                             ")
print("-------------------------------------------------------------------------------")

# conectar ao broker
client.connect(broker)

# se inscreve no tópico para receber reposta do server (via broker) 
client.subscribe(str(tpc))

# inicia loop
client.loop_start()	

time.sleep(999999) 
