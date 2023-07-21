import streamlit as st
import numpy as np
import plotly.graph_objects as go

from data_processing import load_data

data = load_data()

st.title('Setor Energético Brasileiro')
st.text('Escrever algo aqui...')

anos_operacao = np.sort(data['ano_operacao'].unique())
ano_operacao = st.selectbox('Selecione o ano desejado:', anos_operacao)

data = data[data['ano_operacao'] <= ano_operacao]

st.subheader('Gráficos')

# Gráfico de Barras: Subestações por Estado

qtd_subestacoes_estado = data['id'].value_counts()

fig = go.Figure(data=[go.Bar(x=qtd_subestacoes_estado.index, y=qtd_subestacoes_estado.values)])
fig.update_layout(
    title='Qtd de Subestações por Estado',
    xaxis_title='Estado',
    yaxis_title='Qtd Subestações'
)

st.plotly_chart(fig)

# Gráfico de Barras: Subestações por Região

qtd_subestacoes_regiao = data['regiao'].value_counts()

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

st.map(data)