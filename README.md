# Análise de Dados e Dashboard de Pokémon

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
## Visão Geral

Este projeto foca na extração, análise e visualização de dados relacionados a Pokémon. Ele busca dados abrangentes de atributos e combates de uma API específica, realiza análise exploratória de dados (EDA), aplica técnicas de clusterização automatizada com otimização de hiperparâmetros, constrói um modelo preditivo simples e apresenta insights chave através de um dashboard interativo feito com Streamlit.

Os objetivos principais são:
1.  **Aquisição de Dados:** Extrair dados de forma confiável da API de Pokémon, lidando com autenticação, paginação e limites de requisições (rate limiting).
2.  **Exploração de Dados:** Entender a distribuição, relações e características dos atributos dos Pokémon e seu desempenho em combate (vitórias).
3.  **Clusterização:** Identificar automaticamente grupos distintos (clusters) de Pokémon com base em seus status, utilizando múltiplos algoritmos e critérios de avaliação.
4.  **Modelagem Preditiva:** Construir um modelo básico de regressão linear para prever as vitórias de um Pokémon com base em sua velocidade e avaliar suas suposições.
5.  **Visualização:** Criar um dashboard interativo para que os usuários explorem os dados dos Pokémon com base no tipo e status de lendário.

## Funcionalidades

* **Extração de Dados da API:**
    * Autentica usando tokens JWT obtidos via endpoint de login.
    * Busca a lista básica de Pokémon (`/pokemon`) com paginação.
    * Busca atributos detalhados para cada Pokémon (`/pokemon/{id}`).
    * Busca a lista de resultados de combate (`/combats`) com paginação.
    * Inclui pausas (`time.sleep`) e lógica de retentativa para lidar com limites da API (erros HTTP 429).
    * Salva os dados brutos em arquivos JSON (`pokemons.json`, `pokemons_atributos.json`, `combats.json`).
* **Análise Exploratória de Dados (EDA):**
    * Carrega os dados brutos JSON em DataFrames do Pandas.
    * Limpeza e pré-processamento de dados: Une os dados de vitórias em combate, trata valores ausentes (preenche `wins` com 0), converte tipos de dados.
    * Cálculo de estatísticas descritivas (`.describe()`).
    * Análise de variáveis categóricas (`.value_counts()` para tipos, status de lendário, geração).
    * Análise de correlação entre variáveis numéricas visualizada com um heatmap do Seaborn.
* **Clusterização Automatizada (`AutoClusterHPO`):**
    * Classe Python customizada implementando clusterização automatizada.
    * Usa `Hyperopt` (algoritmo TPE) para otimização de hiperparâmetros.
    * Testa múltiplos algoritmos de clusterização: KMeans, DBSCAN, Agglomerative Clustering.
    * Otimiza hiperparâmetros (ex: `n_clusters`, `eps`, `min_samples`, `linkage`) com base no algoritmo.
    * Avalia a qualidade do cluster usando uma pontuação combinada de Índices de Validade de Cluster (CVI) baseada na Pontuação de Silhueta (Silhouette Score), Índice Calinski-Harabasz (normalizado) e Índice Davies-Bouldin (inverso normalizado).
    * Lida com o escalonamento de dados usando `StandardScaler`.
    * Gerencia pontos de ruído gerados pelo DBSCAN durante o cálculo do CVI.
    * Identifica o melhor algoritmo geral e a configuração de parâmetros.
* **Modelagem Preditiva:**
    * Treina um modelo simples de Regressão Linear (`scikit-learn`) para prever `wins` com base na `speed` escalonada.
    * Divide os dados em conjuntos de treino e teste.
    * Avalia o desempenho do modelo usando Erro Quadrático Médio (MSE) e Coeficiente de Determinação (R²).
    * Realiza análise de resíduos para verificar as suposições da regressão:
        * Homocedasticidade (Gráfico de Resíduos vs. Valores Previstos, teste de Breusch-Pagan).
        * Normalidade dos Resíduos (Histograma, teste de Shapiro-Wilk).
        * Independência dos Resíduos (Gráfico de Resíduos vs. Ordem, teste de Durbin-Watson).
* **Dashboard Interativo (`Streamlit`):**
    * Aplicação web construída usando Streamlit (`app.py`).
    * Carrega os dados processados de `pokemons_atributos.json`.
    * Filtros na barra lateral (sidebar) para `types` (tipos) e `legendary` (lendário) dos Pokémon.
    * Exibe indicadores chave de desempenho (KPIs) como métricas (médias de status: Speed, HP, Attack, etc.).
    * Visualiza a distribuição das variáveis numéricas usando histogramas Plotly.
    * Mostra gráficos de barras horizontais Plotly para o Top 10 Pokémon com base nos status selecionados (`speed`, `hp`, `attack`, etc.).
    * Exibe um heatmap de correlação interativo Plotly das variáveis numéricas.
    * Trata casos onde os filtros não retornam dados.

## Estrutura do Projeto

```
pokemon-dashboard-project/
│
├── .gitignore               # Especifica arquivos não rastreados que o Git deve ignorar.
├── README.md                # Este arquivo: explica o projeto.
├── requirements.txt         # Lista as dependências Python necessárias para rodar o projeto.
│
├── data/
│   └── raw/
│       └── .gitkeep         # Placeholder para garantir que o Git rastreie o diretório vazio. Arquivos JSON brutos são salvos aqui pelo script de extração, mas são ignorados pelo gitignore.
│
├── notebooks/
│   └── exploratory_analysis.ipynb  # Jupyter notebook contendo os passos de EDA, clusterização e modelagem.
│
├── scripts/
│   ├── extract_data.py      # Script Python para extrair dados da API.
│   └── AutoClusterHPO.py    # Classe Python para clusterização automatizada com otimização de hiperparâmetros.
│
└── src/
    └── app.py               # Script Python para a aplicação de dashboard Streamlit.
```

## Configuração e Instalação

Siga estes passos para configurar o ambiente do projeto:

1.  **Clonar o Repositório:**
    ```bash
    git clone [https://github.com/](https://github.com/)<seu-usuario>/pokemon-dashboard-project.git
    cd pokemon-dashboard-project
    ```

2.  **Criar e Ativar um Ambiente Virtual:**
    (Recomendado para evitar conflitos com outros projetos)
    ```bash
    # Usando venv (biblioteca padrão)
    python -m venv venv
    ```
    * No Windows: `.\venv\Scripts\activate`
    * No macOS/Linux: `source venv/bin/activate`

3.  **Instalar Dependências:**
    Certifique-se de que seu ambiente virtual está ativado, então instale as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

## Bibliotecas Chave Utilizadas

O arquivo `requirements.txt` deve conter:

```
requests
pandas
numpy
streamlit
plotly
seaborn
matplotlib
scikit-learn
hyperopt
scipy
```

## Uso

Siga este fluxo de trabalho para executar os componentes do projeto:

1.  **Extrair Dados da API:**
    Execute o script de extração. Ele fará login na API, buscará todos os atributos de Pokémon e dados de combate, e os salvará como arquivos JSON no diretório `data/raw/`.
    ```bash
    python scripts/extract_data.py
    ```
    *Observação: Este script atualmente tem as credenciais da API fixas no código (hardcoded). Para produção ou compartilhamento, considere usar variáveis de ambiente ou um arquivo de configuração.*

2.  **Executar o Dashboard Interativo:**
    Assim que a extração de dados estiver completa (você terá `pokemons_atributos.json` e `combats.json` em `data/raw/`), inicie a aplicação Streamlit:
    ```bash
    streamlit run src/app.py
    ```
    Isso abrirá o dashboard no seu navegador. Use os filtros da barra lateral para explorar os dados.

3.  **(Opcional) Explorar o Notebook de Análise:**
    Para ver os passos detalhados do processo de EDA, clusterização e modelagem, execute o Jupyter notebook:
    ```bash
    jupyter notebook notebooks/exploratory_analysis.ipynb
    ```
    Certifique-se de executar as células sequencialmente, pois células posteriores dependem de objetos criados anteriormente.

## Dados

* **Fonte:** Os dados são extraídos de uma API específica hospedada em `http://ec2-52-67-119-247.sa-east-1.compute.amazonaws.com:8000`. O acesso requer autenticação via endpoint `/login`.
* **Endpoints Utilizados:**
    * `/login`: Para obter um token de autenticação JWT.
    * `/pokemon`: Para buscar a lista de Pokémon (paginada).
    * `/pokemon/{id}`: Para buscar atributos detalhados de um Pokémon específico.
    * `/combats`: Para buscar resultados de combate (paginados).
* **Arquivos Gerados (`data/raw/` - *Não commitados no Git*):**
    * `pokemons.json`: Lista básica de Pokémon com seus IDs (arquivo intermediário).
    * `pokemons_atributos.json`: Atributos detalhados para cada Pokémon.
    * `combats.json`: Lista de resultados de combate, incluindo o ID do vencedor.

## Análise e Modelagem (`exploratory_analysis.ipynb`)

O notebook realiza as seguintes análises chave:

* **Carregamento e Preparação dos Dados:** Lê os arquivos JSON, une os dados de `wins` (vitórias) do `combats.json` ao DataFrame de atributos, trata `wins` ausentes preenchendo com 0 e define tipos de dados apropriados.
* **Análise Descritiva:** Calcula estatísticas resumidas para variáveis numéricas e examina a contagem de valores para variáveis categóricas (`types`, `legendary`, `generation`).
* **Análise de Correlação:** Computa e visualiza a matriz de correlação para atributos numéricos usando um heatmap. `wins` mostra correlação positiva moderada com vários status, notavelmente `speed` (~0.55).
* **Clusterização Automatizada:**
    * Aplica a classe `AutoClusterHPO` às variáveis `hp`, `attack`, `defense`, `sp_attack`, `sp_defense`, `speed`, `generation` e `wins`.
    * **Resultado:** Agglomerative Clustering com `n_clusters=3` e `linkage='single'` foi considerado o melhor, alcançando uma pontuação CVI combinada de ~0.513.
    * **Interpretação dos Clusters:**
        * Cluster 0: A grande maioria dos Pokémon (796/799).
        * Cluster 1: Shuckle (ID 231) - Defense/Sp. Defense extremamente altas, HP/Attack/Speed muito baixos.
        * Cluster 2: Chansey (ID 122) & Blissey (ID 262) - HP extremamente alto, Attack/Defense muito baixos.
* **Modelagem Preditiva (Wins vs. Speed):**
    * Um modelo simples de Regressão Linear é treinado usando `speed` escalonada para prever `wins`.
    * **Desempenho:** Atinge um R² de aproximadamente 0.63 no conjunto de teste, indicando que a velocidade explica cerca de 63% da variância nas vitórias neste modelo simples. O MSE é ~20.89.
    * **Verificação das Suposições:**
        * *Homocedasticidade:* O gráfico de resíduos mostra padrões potenciais, e o teste de Breusch-Pagan resulta em um p-valor muito pequeno (< 0.001), sugerindo **heterocedasticidade** (a variância dos erros não é constante).
        * *Normalidade dos Resíduos:* O histograma é assimétrico, e o teste de Shapiro-Wilk resulta em um p-valor muito pequeno (< 0.001), indicando que **os resíduos não são normalmente distribuídos**.
        * *Independência dos Resíduos:* A estatística de Durbin-Watson é ~1.91, próxima de 2, sugerindo **ausência de autocorrelação significativa** entre os resíduos.
    * *Conclusão:* Embora a velocidade seja um preditor significativo, o modelo linear simples viola algumas suposições chave, sugerindo que um modelo mais complexo ou transformação de dados pode ser necessário para melhores previsões e inferências.

## Dashboard (`app.py`)

A aplicação Streamlit (`src/app.py`) fornece uma interface interativa para explorar os dados dos Pokémon:

* **Carregamento de Dados:** Carrega o arquivo final `pokemons_atributos.json` após a união com as contagens de vitórias. Usa `@st.cache_data` para eficiência.
* **Filtragem:** Permite aos usuários selecionar um `type` (tipo) específico de Pokémon e o status `legendary` (lendário) através de widgets na barra lateral (`st.selectbox`).
* **Métricas KPI:** Exibe valores médios para todos os status primários (HP, Attack, Defense, Sp. Attack, Sp. Defense, Speed, Wins) para o subconjunto filtrado de Pokémon.
* **Distribuições:** Mostra histogramas para cada status numérico, permitindo aos usuários ver a dispersão dos valores para o grupo selecionado.
* **Melhores Desempenhos:** Apresenta gráficos de barras horizontais destacando o Top 10 Pokémon dentro do grupo filtrado para cada status individual.
* **Correlação:** Inclui um heatmap de correlação interativo para os status numéricos dos Pokémon filtrados.

## Melhorias Potenciais e Trabalhos Futuros

* **Gerenciamento de Credenciais:** Mover o nome de usuário/senha da API fixos no código de `extract_data.py` para variáveis de ambiente ou um arquivo de configuração seguro (`.env`).
* **Tratamento de Erros:** Implementar tratamento de erros mais específico no script de extração (ex: para erros de decodificação JSON, problemas de rede além do 429).
* **Modelagem Avançada:**
    * Explorar transformações (ex: log) para `wins` ou preditores para melhor atender às suposições da regressão.
    * Incluir mais variáveis (ex: `types`, `legendary`, termos de interação) no modelo preditivo.
    * Tentar diferentes tipos de modelos (ex: Regressão de Poisson para dados de contagem, Gradient Boosting).
* **Melhorias na Clusterização:**
    * Analisar o impacto de diferentes métodos de escalonamento de variáveis.
    * Realizar uma interpretação mais profunda do Cluster 0.
    * Visualizar clusters usando técnicas de redução de dimensionalidade (PCA, t-SNE).
* **Funcionalidades do Dashboard:**
    * Adicionar mais tipos de visualização (gráficos de dispersão, box plots).
    * Permitir comparação entre diferentes grupos filtrados.
    * Incorporar resultados da clusterização no dashboard.
    * Fazer deploy do dashboard (ex: usando Streamlit Community Cloud).
* **Qualidade do Código:** Adicionar testes unitários, especialmente para a classe `AutoClusterHPO` e funções de processamento de dados.
* **Containerização:** Criar um `Dockerfile` para containerizar a aplicação para facilitar o deploy e a reprodutibilidade.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar um pull request ou abrir uma issue se encontrar bugs ou tiver sugestões de melhorias.
*(Você pode adicionar diretrizes de contribuição mais específicas, se necessário)*

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
*(Ajuste se escolher uma licença diferente)*

## Contato

Vinicius [Seu Sobrenome] - [Seu Email ou Link do Perfil GitHub]
*(Opcional: Adicione seus detalhes de contato)*