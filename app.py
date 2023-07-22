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

st.title('Sistema Elétrico de Transmissão')

# Texto de várias linhas
texto_multilinhas1 = """
## Projeto Final

Projeto de conclusão da disciplina Análise e Visualização de Dados da pós-graduação em Engenharia e Análise de Dados 2023.01 do CESAR , consiste na construção de dashboards e insigths sobre um tema definido pela equipe do projeto

### Equipe

- Felipe Augusto Marques de Alcântra
- Renato de Castro Lopes

### Tema

O sistema elétrico de transmissão brasileiro refere-se à rede de alta tensão que permite a transferência de energia elétrica em larga escala , das usinas de geração até chegar nos centros de distribuição e grandes consumidores de todo o país,
sendo o mesmo uma infraestrutura complexa e vital para o desenvolvimento econômico do país.

O sistema de transmissão brasileiro é composto de usinas de geração, das linhas de transmissão e das subestações de energia, no presente projeto nos debruçamos sobre
as linhas de transmissão e subestações que compoem as instalaçoes estrategicas segundo definições da ONS (Operador Nacional do Sistema Eletrico)

Em função da sua complexidade, o sistema de transmissão tem um orgão de coordenação e controle chamado SIN (sistema integrado nacional) 

Devido a sua importancia estrategica para a economia do Brasil e qualidade de vida da sua população, o sistema de transmissão brasileiro apresenta 
diversos requisitos de redundância definidos pela ONS e coordenados e controlados pelo SIN, no caso em que uma subestação ou linha de transmissão fique inoperante devido à algum problema ou ocorrencia por exemplo, a energia eletrica pode utilizar uma outra rota para 
a mesma flua dos pontos de geração até os consumidores


### A Problematica

Os estados do norte , historicamente estão mais isolados do restante do país no que tange o sistema de transmissão brasileiro, não tendo muitas rotas
de linhas de transmissão, sendo portanto menos resiliente à falhas do que as outras regiões do país, sendo a região atingida pelo pior apagão do pais desde 1990


https://www1.folha.uol.com.br/cotidiano/2010/02/692476-blecaute-atinge-oito-capitais-das-regioes-norte-e-nordeste.shtml

https://g1.globo.com/ap/amapa/noticia/2021/11/03/apagao-no-amapa-completa-1-ano-e-expos-fragilidades-no-acesso-a-energia-eletrica-no-estado.ghtml

https://g1.globo.com/rr/roraima/noticia/2023/04/15/apagao-deixa-boa-vista-e-municipios-do-interior-sem-energia.ghtml

https://pt.wikipedia.org/wiki/Lista_de_blecautes_no_Brasil






"""

st.write(texto_multilinhas1)




# Texto de várias linhas
texto_multilinhas2 = """



### Dataset

Para construção deste dashboard foram utilizados duas fontes de dados:

- **Banco de dados publico da Empresa de Pesquisa Energética (arquivos csv e shapefile):**\n
https://gisepeprd2.epe.gov.br/WebMapEPE/

- **Mapa do Brasil (arquivo Json) :** \n
https://www.kaggle.com/datasets/thiagobodruk/brazil-geojson?resource=download




### Tratamento dos Dados

Dos arquivos escolhidos apenas o csv com os dados das subestações necessitou de um tratamento, sendo necessario a troca de simbolos nas strings do mesmo
e ajuste na tipagem de valores que deveriam ser numericos mas estavam como string

```python

subestacoes = pd.read_csv('./data/subestacoes-base-existentes.csv')
subestacoes = subestacoes.fillna('')
subestacoes['Nome'] = subestacoes['Nome'].str.replace('SE ', '')
subestacoes['ano_operacao'] = subestacoes['Ano de entrada em operação']
subestacoes['ano_operacao'] = subestacoes['ano_operacao'].str.replace('-','0')
subestacoes['ano_operacao'] = subestacoes['ano_operacao'].str.replace(' ','0')
subestacoes['ano_operacao'] = subestacoes['ano_operacao'].astype(int)


```

"""

st.write(texto_multilinhas2)

st.subheader('Gráficos interativos')



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

st.write("__Mapa com as subestações:__")
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
st.write("**Mapa com as subestações e as linhas de transmissão:**")


folium_static(mapa)

# Texto de várias linhas
texto_multilinhas3 = """



### Insigths

Ajustando os filtros dos gráficos interativos, foi possivel visualizar que o sistema de transmissão da região norte do brasil
tem um baixissimo numero de linhas de transmissão e muitas vezes é inexistente rotas alternativas de linhas de transmissão, sendo
portanto mais vulnerável à ocorrencia de falhas

Também foi possivel verificar que Roraima é o unico estado não interligado ao SIN,tornando sua situação bastante critica
como foi o caso durante o apagão ocorrido em 2023

Para minimizar a indisponibilidade de energia eletrica na região norte é necessario a construção de 
mais linhas de transmissão e subestações na região,algo que está ocorrendo nas ultimas decadas, mas 
num ritmo bem menor do que no restante do país.

O planejamento para o crescimento do sistema de transmissão brasileiro não é uma tarefa facil, há 
muitos fatores associados na escolha das regiões para construção de novas linhas de transmissão e subestações
grupos como o EPE ,OSN e SIN estão constatemente analisando as necessidades energeticas do brasil e vulnerabilidades
no sistema de transmissão para traçar as estrategias para o desenvolvimento do país

Devido aos ultimos apagões na região norte, acreditamos que o EPE,ONS e SIN deveriam reajustar seus planejamentos 
dando um enfoque maior no desenvolvimento do sistema de transmissão da região norte. 


"""

st.write(texto_multilinhas3)


