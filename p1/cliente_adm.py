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

#Limpar tela
import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#broker local -> mudar depois para o local certo (ip ou nome da máq. na aws)
broker_init = "test.mosquitto.org"

#broker = input("Informe o broker, sugestão: 'test.mosquitto.org' ou ENTER  para localhost: ")
broker = broker_init

#nclientname = input("Informe o número da catraca/porta de acesso: ")
nclientname = 'cliente'
clientname = nclientname + '-' + str(datetime.now()) 

# o datatime é só para não criar cliente com nomes iguais. "gamb" (arrumar uma forma mais elegante)
# registrando o nome do topico --- aqui será dinâmico configurado pelo usuário
tpc = str("projetosd:teste")

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
	topic    = msg.topic
	m_decode = str(msg.payload.decode("utf-8","ignore"))

# instanciando o cliente. 
client = mqtt.Client (clientname) 
client.on_connect=on_connect
client.on_disconnet=on_disconnet

#ativar recebimento de mensagem / inclui a própria mensagem (tratar isso)
client.on_message=on_message
print("Conectado no broker", broker)

# conectar ao broker
client.connect(broker)

# se inscreve no tópico para receber reposta do server (via broker) 
client.subscribe(str(tpc))

# inicia loop
client.loop_start()	

cnt = 1
while(cnt > 0):
		cls()
		print("\n\n")
		print("                     CONTROLE DE ACESSO DE CONDOMINIO                          ")
		print("                      GERENCIAMENTO - MENU PRINCIPAL                           ")
		print("\n")
		print(" ##############################################################################")
		print(" |                                                                            |")
		print(" |   Digite um comando para prosseguir:                                       |")
		print(" |   1 - Cadastrar local                                                      |")
		print(" |   2 - Cadastrar politica de acesso                                         |")
		print(" |   3 - Cadastrar usuarios                                                   |")
		print(" |   4 - Cadastrar predios                                                    |")
		print(" |                                                                            |")
		print(" ##############################################################################")
		men = input("  Digite a opcao escolhida: ")

		men_int = int(men)  # Convertendo a mensagem em um inteiro

		if men_int == 2:
			cls()
			print("\n\n")
			print("                        CADASTRAR POLITICA DE ACESSO                           ")
			print("\n")
			print(" ##############################################################################")
			print(" |                                                                            |")
			print(" |   Voce deve informar a que usuario a politica de acesso se destina.        |")
			print(" |   - ID = um numero                                                         |")
			print(" |   - Nome = Administração, aluno ou visitante                               |")
			print(" |   - Acesso livre = S para sim ou N para não                                |")
			print(" |   - Limitado por capacidade = S para sim ou N para não                     |")
			print(" |                                                                            |")
			print(" ##############################################################################")

			id_politica = input(" ID: ")
			nome = input(" Nome: ")
			acesso_livre = input(" Acesso livre S/N: ")
			limitado_por_capacidade = input(" Limitado por capacidade S/N: ")

			men = "1#" + id_politica + "#" + nome + "#" + acesso_livre + "#" + limitado_por_capacidade

			client.publish(tpc, str(men))

		elif men_int == 3:
			cls()
			print("\n")
			print("                              CADASTRAR USUARIOS                               ")
			print(" ##############################################################################")
			print(" |                                                                            |")
			print(" |   Veja as informacoes de como preencher                                    |")
			print(" |   - ID = um numero                                                         |")
			print(" |   - Nome = nome do usuario, por exemplo Jose                               |")
			print(" |   - Politica = o numero de uma politica de acesso ja cadastrada            |")
			print(" |   - Complexo = UFG                                                         |")
			print(" |   - Predio = CA-A, CA-B ou CA-C                                            |")
			print(" |   - Andar = um numero de 1 a 3                                             |")
			print(" |   - Ativo = S para sim ou N para não                                       |")
			print(" |                                                                            |")
			print(" ##############################################################################")
			id_matricula = input(" ID: ")
			nome = input(" Nome: ")
			politica = input(" Politica: ")
			complexo = input(" Complexo: ")
			predio = input(" Predio: ")
			andar = input(" andar: ")
			ativo = input(" ativo: ")

			men = "2#" + id_matricula + "#" + nome + "#" + politica + "#" + complexo + "#" + predio + "#" + andar + "#" + ativo

			client.publish(tpc, str(men))

		elif men_int == 7:
			cls()
			print("\n\n")
			print("                              CADASTRAR ACESSO                                 ")
			print("\n")
			print(" ##############################################################################")
			print(" |                                                                            |")
			print(" |   Cadastrar acesso dos usuarios                                            |")
			print(" |                                                                            |")
			print(" |   Opcoes:                                                                  |")
			print(" |                                                                            |")
			print(" |   Predio 01                                                                |")
			print(" |   - 12 andares                                                             |")
			print(" |                                                                            |")
			print(" |   Predio 02                                                                |")
			print(" |   - 12 andares                                                             |")
			print(" |                                                                            |")
			print(" ##############################################################################")
			matricula = input(" Matricula: ")
			predio = input(" Predio: ")
			andar = input(" Andar: ")
			tipo_de_acesso = input(" Tipo de acesso: ")

			men = "3#" + matricula + "#" + predio + "#" + andar + "#" + tipo_de_acesso

			client.publish(tpc, str(men))

		elif men_int == 4:
			cls()
			print("\n\n")
			print("                              CADASTRAR PREDIOS                                ")
			print("\n")
			print(" ##############################################################################")
			print(" |                                                                            |")
			print(" |   Cadastrar predios no condominio                                          |")
			print(" |   Informe os dados solicitados                                             |")
			print(" |                                                                            |")
			print(" |                                                                            |")
			print(" ##############################################################################")
			id = input(" ID: ")
			nome = input(" Nome: ")
			numero_de_andares = input(" Numero de andares: ")
			capacidade_de_pessoas_por_andar = input(" Capacidade de pessoas por andar: ")

			men = "4#" + id + "#" + nome + "#" + numero_de_andares + "#" + capacidade_de_pessoas_por_andar

			client.publish(tpc, str(men))

		elif men_int == 1:
			cls()
			print("\n\n")
			print("                              CADASTRAR LOCAL                                  ")
			print("\n")
			print(" ##############################################################################")
			print(" |                                                                            |")
			print(" |   Veja as informações de como preencher                                    |")
			print(" |   ID = um numero                                                           |")
			print(" |   Complexo = UFG                                                           |")
			print(" |   Predio = CA-A, CA-B ou CA-C                                              |")
			print(" |   Andar = um numero de 1 a 3                                               |")
			print(" |   Capacidade = capacidade total de pessoas                                 |")
			print(" |   Ocupantes = pessoas que estão no local                                   |")
			print(" |                                                                            |")
			print(" ##############################################################################")

			id_local = input(" ID: ")
			complexo = input(" Complexo: ")
			predio = input(" Predio: ")
			andar = input(" Andar: ")
			capacidade = input(" Capacidade: ")
			ocupantes = input(" Ocupantes: ")

			men = "5#" + id_local + "#" + complexo + "#" + predio + "#" + andar + "#" + capacidade + "#" + ocupantes

			client.publish(tpc, str(men))

		elif men_int == 6:
			client.publish(tpc, str("6#123#P01#CAT00#A03"))

		else:
			print("Nao existe esta opcao, tente novamente!", "\n")
