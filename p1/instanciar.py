import sys
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

# ATENÇÃO! PROVISÓRIO
# Adequar o 'clienteADM.py' para salvar no 'Redis' com essa estrutura.
# somente para teste, será usado o clienteADM para inserir os dados

local = {
            "id_local": "1", 
            "complexo": "UFG", 
            "predio": "CA-A",  
            "andar": "1",
            "capacidade": 50,
            "ocupantes": 0
        }
r.hmset("local:" 
        + local ['complexo'] + ":" 
        + local ['predio'] + ":" 
        + local ['andar'],
        local)

user = {
            "id_matricula": "123", 
            "nome": "Jose Silva", 
            "politica": "Administracao",  
            "complexo": "UFG", 
            "predio": "CA-A",
            "andar": "1",
            "ativo": "S"
        }
r.hmset("user:" + user ['id_matricula'], user)

politica = {
            "id_politica": "1", 
            "nome": "Administracao", 
            "acesso_livre": "S",  
            "limitado_por_capacidade": "N"
        }
r.hmset("politica:" + politica ['id_politica'], politica)
