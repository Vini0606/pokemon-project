import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- Configuração da Página ---
# Usar o layout 'wide' para aproveitar melhor o espaço da tela
st.set_page_config(layout="wide", page_title="Dashboard de Análise")

@st.cache_data
def carregar_dados():
    """Gera um DataFrame fictício para o dashboard."""
    df_atributos = pd.read_json(r'data\\raw\\pokemons_atributos.json')

    df_combats = pd.read_json(r'data\\raw\\combats.json')

    df_combats_winners = df_combats['winner'].value_counts().reset_index().rename(
    columns={'winner': 'id', 'index': 'pokemon_id', 'count':'wins'}
    ).sort_values(by='wins', ascending=False)
    
    df_atributos = pd.merge(
    df_atributos,
    df_combats_winners,
    on='id',  # Coluna com mesmo nome em ambos
    how='left'
    )
    
    return df_atributos

#df_original = carregar_dados()

df_atributos = carregar_dados()

# --- Barra Lateral (Sidebar) com Filtros ---
st.sidebar.header("Filtros do Dashboard")

# Filtro 1: Seletor de Região (Selectbox para seleção única) # <-- MUDANÇA
tipos_disponiveis = df_atributos['types'].unique()
tipo_selecionado = st.sidebar.selectbox( # <-- MUDANÇA
    'Selecione o Tipo de Pokémon', # <-- MUDANÇA
    options=tipos_disponiveis,
    index=0 # Define a primeira região da lista como padrão
)

# Filtro 1: Seletor de Região (Selectbox para seleção única) # <-- MUDANÇA
opcoes_legendary = df_atributos['legendary'].unique()
legendary_selecionado = st.sidebar.selectbox( # <-- MUDANÇA
    'Selecione o Tipo de Pokémon', # <-- MUDANÇA
    options=opcoes_legendary,
    index=0 # Define a primeira região da lista como padrão
)

# --- Filtragem dos Dados ---
# Aplicar filtros ao DataFrame
df_filtrado = df_atributos[
    (df_atributos['types'] == tipo_selecionado) & # <-- MUDANÇA
    (df_atributos['legendary'] <= legendary_selecionado)
]

# Verificar se o dataframe filtrado está vazio
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados. Por favor, ajuste suas seleções.")
    st.stop()

# --- Layout do Dashboard ---
st.title("Dashboard de Análise de Dados de Pokemons")

# --- Seção 1: 6 Cards (KPIs) ---
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    st.metric(label="Speed (Média)", value=f"{df_filtrado['speed'].mean():.2f}")
with col2:
    st.metric(label="Hp (Média)", value=f"{df_filtrado['hp'].mean():.2f}")
with col3:
    st.metric(label="Attack (Média)", value=f"{df_filtrado['attack'].mean():.2f}")
with col4:
    st.metric(label="Defense (Média)", value=f"{df_filtrado['defense'].mean():.2f}")
with col5:
    st.metric(label="Sp_attack (Média)", value=f"{df_filtrado['sp_attack'].mean():.2f}")
with col6:
    st.metric(label="Sp_defense (Média)", value=f"{df_filtrado['sp_defense'].mean():.2f}")
with col7:
    st.metric(label="Wins (Média)", value=f"{df_filtrado['wins'].mean():.2f}")


st.divider()

# --- Seção 2: 6 Histogramas ---
st.header("Distribuição das Variáveis Numéricas")
col1, col2, col3 = st.columns(3)
col4, col5, col6, col7 = st.columns(4)
cols_num = ['speed', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'wins']
cols_layout = [col1, col2, col3, col4, col5, col6, col7]

for i, col_name in enumerate(cols_num):
    with cols_layout[i]:
        fig = px.histogram(
            df_filtrado, 
            x=col_name, 
            title=f'Distribuição de {col_name}',
            nbins=30
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Seção 3: 6 Gráficos de Barras ---
st.header("Análises Categoriais")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

# Gráfico 1: Contagem de Categoria_A
with col1:
    df_count = df_filtrado[['name', 'speed']].sort_values(by='speed', ascending=False).head(10).reset_index(drop=True)
    fig = px.bar(df_count, x='speed', y='name', title='Maior Speed por Nome', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

# Gráfico 2: Contagem de Categoria_B
with col2:
    df_count = df_filtrado[['name', 'hp']].sort_values(by='hp', ascending=False).head(10).reset_index(drop=True)
    fig = px.bar(df_count, x='hp', y='name', title='Maior Hp por Nome', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

# Gráfico 3: Contagem de Região
with col3:
    df_count = df_filtrado[['name', 'attack']].sort_values(by='attack', ascending=False).head(10).reset_index(drop=True)
    fig = px.bar(df_count, x='attack', y='name', title='Maior Attack por Nome', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

# Gráfico 4: Média de Num_1 por Região
with col4:
    df_count = df_filtrado[['name', 'defense']].sort_values(by='defense', ascending=False).head(10).reset_index(drop=True)
    fig = px.bar(df_count, x='defense', y='name', title='Maior Defense por Nome', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

# Gráfico 5: Soma de Num_2 por Categoria_A
with col5:
    df_count = df_filtrado[['name', 'sp_attack']].sort_values(by='sp_attack', ascending=False).head(10).reset_index(drop=True)
    fig = px.bar(df_count, x='sp_attack', y='name', title='Maior Sp_attack por Nome', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

# Gráfico 6: Média de Num_3 por Categoria_B
with col6:
    df_count = df_filtrado[['name', 'sp_defense']].sort_values(by='sp_defense', ascending=False).head(10).reset_index(drop=True)
    fig = px.bar(df_count, x='sp_defense', y='name', title='Maior Sp_defense por Nome', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Seção 4: Matriz de Correlação ---
st.header("Matriz de Correlação")

# Selecionar apenas colunas numéricas para correlação
df_corr = df_filtrado[cols_num].corr()

# Usar Plotly Express para criar o heatmap
fig_corr = px.imshow(
    df_corr,
    text_auto=True,  # Adiciona os valores numéricos nas células
    aspect="auto",
    color_continuous_scale='RdBu_r', # Escala de cor (Vermelho-Azul)
    zmin=-1, # Fixar a escala de -1
    zmax=1   # a +1
)
fig_corr.update_layout(title="Correlação entre Variáveis Numéricas")
st.plotly_chart(fig_corr, use_container_width=True)