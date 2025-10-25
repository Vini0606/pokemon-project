import requests
import json
import time

base_url = "http://ec2-52-67-119-247.sa-east-1.compute.amazonaws.com:8000"

# --- ETAPA 1: LOGIN ---
# (Usando as credenciais do seu etl.py)
login_endpoint = "/login"
login_url = base_url + login_endpoint
login_payload = {
    "username": "kaizen-poke",
    "password": "4w9f@D39fkkO"
}
# Cabeçalhos para o login
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'accept': 'application/json'
}

try:
    print("Tentando fazer login em:", login_url)
    response_login = requests.post(login_url, headers=headers, json=login_payload)
    response_login.raise_for_status() 

    # --- ETAPA 2: RECEBER E GUARDAR O JWT ---
    token_data = response_login.json()
    access_token = token_data['access_token']
    token_type = token_data.get('token_type', 'Bearer') 
    print(f"Login bem-sucedido! Token ({token_type}) obtido.")

    # --- Prepara os cabeçalhos de DADOS para todas as etapas seguintes ---
    data_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'accept': 'application/json',
        'Authorization': f'{token_type} {access_token}'
    }

    # --- ETAPA 3: BUSCAR A LISTA BASE (POKEMON) ---
    print("\nIniciando a extração da LISTA BASE de Pokémons...")
    dados_endpoint = "/pokemon"
    dados_url = base_url + dados_endpoint
    lista_pokemons_basica = [] 
    pagina_atual = 1
    per_page_pokemon = 50 # Conforme seu script

    for i in range(1000):
        params = {'page': pagina_atual, 'per_page': per_page_pokemon}
        try:
            print(f"Buscando Pokémons - Página: {pagina_atual}...")
            response_dados = requests.get(dados_url, headers=data_headers, params=params)
            response_dados.raise_for_status() 
        except requests.exceptions.HTTPError as errh:
            if errh.response.status_code == 429:
                print(f" -> Erro 429 (Pokémons). Pausando por 5 segundos...")
                time.sleep(5) 
                continue 
            else:
                raise errh 
        
        dados_da_pagina = response_dados.json()

        # Correção baseada na estrutura da imagem (image_970b68.png)
        if 'pokemons' not in dados_da_pagina or not dados_da_pagina['pokemons']:
            print("Página vazia (sem pokémons). Extração da lista base concluída.")
            break 
        
        lista_pokemons_basica.extend(dados_da_pagina['pokemons'])
        print(f" -> {len(dados_da_pagina['pokemons'])} itens. Total Pokémons: {len(lista_pokemons_basica)}")
        
        pagina_atual += 1
        time.sleep(1) 

    # --- ETAPA 4: SALVAR A LISTA BASE (POKEMON) ---
    nome_arquivo_base = r"data\\raw\\pokemons.json"
    print(f"\nSalvando os {len(lista_pokemons_basica)} itens básicos em {nome_arquivo_base}...")
    with open(nome_arquivo_base, 'w', encoding='utf-8') as f:
        json.dump(lista_pokemons_basica, f, indent=2, ensure_ascii=False)
    print(f"Lista base salva com sucesso.")

    # --- ETAPA 5: BUSCAR DETALHES DE CADA POKÉMON ---
    print(f"\nIniciando a extração de DETALHES para {len(lista_pokemons_basica)} Pokémons...")
    lista_pokemons_detalhada = [] 
    for i, item_basico in enumerate(lista_pokemons_basica):
        try:
            pokemon_id = item_basico['id']
        except KeyError:
            print(f"Erro: Item {item_basico} não contém 'id'. Pulando.")
            continue 
        except TypeError:
            print(f"Erro: Item {item_basico} formato inesperado. Pulando.")
            continue

        detalhe_url = f"{base_url}/pokemon/{pokemon_id}"
        while True:
            try:
                print(f"Buscando detalhes... ID: {pokemon_id} ({i+1}/{len(lista_pokemons_basica)})")
                response_detalhe = requests.get(detalhe_url, headers=data_headers)
                response_detalhe.raise_for_status()
                lista_pokemons_detalhada.append(response_detalhe.json())
                time.sleep(1) # Pausa entre cada ID
                break 
            except requests.exceptions.HTTPError as errh:
                if errh.response.status_code == 429:
                    print(f" -> Erro 429 no ID {pokemon_id}. Pausando 5s...")
                    time.sleep(5)
                    continue 
                else:
                    print(f"Erro HTTP {errh.response.status_code} ao buscar ID {pokemon_id}. Pulando.")
                    break
            except requests.exceptions.RequestException as err:
                print(f"Erro de Conexão no ID {pokemon_id}: {err}. Pulando.")
                break 

    # --- ETAPA 6: SALVAR OS DADOS DETALHADOS (POKEMON) ---
    nome_arquivo_detalhado = r"data\\raw\\pokemons_atributos.json"
    print(f"\nSalvando todos os {len(lista_pokemons_detalhada)} itens detalhados em {nome_arquivo_detalhado}...")
    with open(nome_arquivo_detalhado, 'w', encoding='utf-8') as f:
        json.dump(lista_pokemons_detalhada, f, indent=2, ensure_ascii=False)
    print(f"Dados detalhados salvos com sucesso!")

    # --- NOVA ETAPA 7: BUSCAR A LISTA DE COMBATES (PAGINAÇÃO) ---
    print("\nIniciando a extração da LISTA DE COMBATES...")
    
    combats_endpoint = "/combats"
    combats_url = base_url + combats_endpoint
    
    lista_combats = [] # Lista para guardar os dados de combates
    pagina_atual = 1
    per_page_combats = 10 # Conforme seu novo 'curl'

    for i in range(1000):
        params = {
            'page': pagina_atual,
            'per_page': per_page_combats
        }

        try:
            print(f"Buscando Combates - Página: {pagina_atual}...")
            response_combats = requests.get(combats_url, headers=data_headers, params=params)
            response_combats.raise_for_status() 
        
        except requests.exceptions.HTTPError as errh:
            if errh.response.status_code == 429:
                print(f" -> Erro 429 (Combates). Pausando por 5 segundos...")
                time.sleep(5) 
                continue 
            else:
                raise errh 
        
        dados_da_pagina = response_combats.json()

        # Assumindo que a API /combats segue o mesmo padrão da /pokemon
        # (retornando um objeto com uma chave 'combats')
        if 'combats' not in dados_da_pagina or not dados_da_pagina['combats']:
            print("Página vazia (sem combates). Extração de combates concluída.")
            break 
        
        lista_combats.extend(dados_da_pagina['combats'])
        print(f" -> {len(dados_da_pagina['combats'])} itens. Total Combates: {len(lista_combats)}")
        
        pagina_atual += 1
        time.sleep(1) # Pausa de 1s entre cada PÁGINA de combates

    # --- NOVA ETAPA 8: SALVAR OS DADOS DE COMBATES ---
    
    nome_arquivo_combats = r"data\\raw\\combats.json"
    print(f"\nSalvando todos os {len(lista_combats)} combates em {nome_arquivo_combats}...")
    
    with open(nome_arquivo_combats, 'w', encoding='utf-8') as f:
        json.dump(lista_combats, f, indent=2, ensure_ascii=False)

    print(f"Dados de combates salvos com sucesso!")

# Captura de erros fatais
except requests.exceptions.HTTPError as errh:
    print(f"Erro HTTP Fatal: {errh}")
except requests.exceptions.RequestException as err:
    print(f"Erro de Conexão: {err}")
except KeyError:
    print("Erro: Não foi possível encontrar 'access_token' na resposta do login.")
    print("Resposta recebida do servidor:", response_login.text)