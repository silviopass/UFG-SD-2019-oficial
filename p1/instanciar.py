#!/usr/bin/python
# -- coding: utf-8 --
import sys
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

# ATENÇÃO! PROVISÓRIO
# Adequar o 'cliente_adm.py' para salvar no 'Redis' com essa estrutura.

# instanciando local
local = {"id_local": "1", "complexo": "UFG", "predio": "CA-A", "andar": "1", "capacidade": 10, "ocupantes": 0}
r.hmset("local:"+local['complexo']+":"+local['predio']+":"+local['andar'],local)
local = {"id_local": "2", "complexo": "UFG", "predio": "CA-A", "andar": "2", "capacidade": 10, "ocupantes": 0}
r.hmset("local:"+local['complexo']+":"+local['predio']+":"+local['andar'],local)
local = {"id_local": "3", "complexo": "UFG", "predio": "CA-A", "andar": "3", "capacidade": 10, "ocupantes": 0}
r.hmset("local:"+local['complexo']+":"+local['predio']+":"+local['andar'],local)
local = {"id_local": "4", "complexo": "UFG", "predio": "CA-B", "andar": "1", "capacidade": 10, "ocupantes": 0}
r.hmset("local:"+local['complexo']+":"+local['predio']+":"+local['andar'],local)
local = {"id_local": "5", "complexo": "UFG", "predio": "CA-B", "andar": "2", "capacidade": 10, "ocupantes": 0}
r.hmset("local:"+local['complexo']+":"+local['predio']+":"+local['andar'],local)
local = {"id_local": "6", "complexo": "UFG", "predio": "CA-B", "andar": "3", "capacidade": 10, "ocupantes": 0}
r.hmset("local:"+local['complexo']+":"+local['predio']+":"+local['andar'],local)
local = {"id_local": "7", "complexo": "UFG", "predio": "CA-C", "andar": "1", "capacidade": 10, "ocupantes": 0}
r.hmset("local:"+local['complexo']+":"+local['predio']+":"+local['andar'],local)
local = {"id_local": "8", "complexo": "UFG", "predio": "CA-C", "andar": "2", "capacidade": 10, "ocupantes": 0}
r.hmset("local:"+local['complexo']+":"+local['predio']+":"+local['andar'],local)
local = {"id_local": "9", "complexo": "UFG", "predio": "CA-C", "andar": "3", "capacidade": 10, "ocupantes": 0}
r.hmset("local:"+local['complexo']+":"+local['predio']+":"+local['andar'],local)

# instanciando usuários
user = {"id_matricula": "101", "nome": "Jose Silva", "politica": "1", "complexo": "UFG", "predio": "CA-A", "andar": "1", "ativo": "S"}
r.hmset("user:" + user ['id_matricula'], user)
user = {"id_matricula": "102", "nome": "Maria Rodrigues",  "politica": "3", "complexo": "UFG", "predio": "CA-C", "andar": "2", "ativo": "S"}
r.hmset("user:" + user ['id_matricula'], user)
user = {"id_matricula": "103", "nome": "Joana Ferreira",  "politica": "2", "complexo": "UFG", "predio": "CA-C", "andar": "2", "ativo": "S"}
r.hmset("user:" + user ['id_matricula'], user)
user = {"id_matricula": "104", "nome": "Carlos Mendes Siqueira",  "politica": "3", "complexo": "UFG", "predio": "CA-C", "andar": "3", "ativo": "S"}
r.hmset("user:" + user ['id_matricula'], user)
user = {"id_matricula": "105", "nome": "Pedro Joaquim", "politica": "1",  "complexo": "UFG", "predio": "CA-B", "andar": "1", "ativo": "N"}
r.hmset("user:" + user ['id_matricula'], user)
user = {"id_matricula": "106",  "nome": "Severino Mendes", "politica": "3", "complexo": "UFG",  "predio": "CA-B", "andar": "2", "ativo": "S"}
r.hmset("user:" + user ['id_matricula'], user)
user = {"id_matricula": "107",  "nome": "Rosana Pereira Costa", "politica": "3", "complexo": "UFG",  "predio": "CA-A", "andar": "2", "ativo": "S"}
r.hmset("user:" + user ['id_matricula'], user)
user = {"id_matricula": "108",  "nome": "Joao Rocha", "politica": "3", "complexo": "UFG",  "predio": "CA-C", "andar": "1", "ativo": "S"}
r.hmset("user:" + user ['id_matricula'], user)
user = {"id_matricula": "109",  "nome": "Eduardo Costa", "politica": "3", "complexo": "UFG",  "predio": "CA-C", "andar": "1", "ativo": "S"}
r.hmset("user:" + user ['id_matricula'], user)
user = {"id_matricula": "110",  "nome": "Roberta Teixeira", "politica": "3", "complexo": "UFG",  "predio": "CA-C", "andar": "1", "ativo": "S"}
r.hmset("user:" + user ['id_matricula'], user)

# instanciando políticas
politica = {"id_politica": "1","nome": "Administração","acesso_livre": "S","limitado_por_capacidade":"N"}
r.hmset("politica:" + politica ['id_politica'], politica)
politica = {"id_politica": "2", "nome": "Condômino", "acesso_livre": "N", "limitado_por_capacidade": "N"}
r.hmset("politica:" + politica ['id_politica'], politica)
politica = {"id_politica": "3", "nome": "Visitante", "acesso_livre": "N","limitado_por_capacidade": "S"}
r.hmset("politica:" + politica ['id_politica'], politica)
