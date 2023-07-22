import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

from data_processing import load_data

subestacoes, linhas = load_data()

# Filtros

st.sidebar.title('Filtros')
anos_operacao = np.sort(pd.concat([subestacoes['ano_operacao'],linhas['Ano_Opera']], axis=0))
ano_inicial, ano_final = st.sidebar.select_slider(
    'Selecione a faixa temporal de interesse:',
    options=anos_operacao,
    value=(anos_operacao[0], anos_operacao[-1])
    )

regioes = subestacoes['regiao'].unique()
regiao = st.sidebar.multiselect('Selecione a Região Geográfica:', regioes, default=regioes)

subestacoes = subestacoes[(subestacoes['ano_operacao'] >= ano_inicial) & (subestacoes['ano_operacao'] <= ano_final) & (subestacoes['regiao'].isin(regiao))]
linhas = linhas[(linhas['Ano_Opera'] >= ano_inicial) & (linhas['Ano_Opera'] <= ano_final)]

st.title('Setor Energético Brasileiro')

# Texto de várias linhas
texto_multilinhas = """
## Projeto Final

Projeto de conclusão da disciplina Análise e Visualização de Dados da pós-graduação em Engenharia e Análise de Dados 2023.01 do CESAR , consiste na construção de dashboards e insigths sobre um tema, neste caso o tema escolhido foi o setor energético brasileiro

### Grupo

- Felipe Augusto
- Renato de Castro Lopes

### Dataset

Para construção deste dashboard foram utilizados duas fontes de dados:

- **Banco de dados publico da Empresa de Pesquisa Energética (arquivos csv e shapefile):**\n
https://gisepeprd2.epe.gov.br/WebMapEPE/

- **Mapa do Brasil (arquivo Json) :** \n
https://www.kaggle.com/datasets/thiagobodruk/brazil-geojson?resource=download


"""

st.write(texto_multilinhas)


st.subheader('Gráficos')

# Gráfico de Barras: Subestações por Estado

qtd_subestacoes_estado = subestacoes['id'].value_counts()

fig = go.Figure(data=[go.Bar(x=qtd_subestacoes_estado.index, y=qtd_subestacoes_estado.values)])
fig.update_layout(
    title='Qtd de Subestações por Estado',
    xaxis_title='Estado',
    yaxis_title='Qtd Subestações'
)

st.plotly_chart(fig)

# Gráfico de Barras: Subestações por Região

qtd_subestacoes_regiao = subestacoes['regiao'].value_counts()

fig = go.Figure(go.Bar(
    x=qtd_subestacoes_regiao.values,
    y=qtd_subestacoes_regiao.index,
    orientation='h'
))

fig.update_layout(
    title='Qtd Subestações por Região',
    xaxis_title='Qtd Subestações',
    yaxis_title='Região',
)

st.plotly_chart(fig)

# Mapa de Dispersão Geográfico: Distribuição das Subestações

st.write("Mapa com as subestações:")
st.map(subestacoes)


# Criar o mapa
latitude, longitude = -15.7801, -47.9292
mapa = folium.Map(location=[latitude, longitude], zoom_start=4)

# Adicionar os objetos LineString ao mapa
for _, linha in linhas.iterrows():
    linha_geojson = linha['geometry'].__geo_interface__
    folium.GeoJson(linha_geojson).add_to(mapa)

for _, ponto in subestacoes.iterrows():
    folium.Circle(
        location=[ponto['lat'], ponto['lon']],
        radius=10000,  # Define o raio do círculo (em metros)
        popup=ponto['Nome'],
        color='red',  # Define a cor do círculo
        fill=True,
        fill_color='red',  # Define a cor de preenchimento do círculo
        fill_opacity=0.7
    ).add_to(mapa)

# Exibir o mapa no Streamlit
st.write("Mapa com as subestações e as linhas de transmissão:")
folium_static(mapa)








