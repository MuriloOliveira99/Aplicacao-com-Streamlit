from logging import exception
from turtle import color
from unicodedata import decimal
import streamlit as st
import pandas as pd
from matplotlib.pyplot import axis, title, xlabel, ylabel
import plotly.express as px


# Configurando a página
st.set_page_config(
    page_title = 'Análise - GÁS',
    page_icon = ':bar_chart:',
    layout = 'centered'
)

# Inserindo um título na página
st.title(':fuelpump: ANÁLISE - GÁS')
st.header('Valor')

# Importando a base de dados .CSV
df = pd.read_csv('glp-2021-02.csv', 
                  delimiter=";", 
                  decimal=",", 
                  nrows=3000, 
                  usecols=['Regiao - Sigla', 'Estado - Sigla', 'Municipio', 'Bairro', 'Valor de Venda', 'Bandeira']
)

# Renomeando o nome da coluna para realizar a query
#df.columns = df.columns.str.replace(' ', '')
df.rename(
    columns={'Regiao - Sigla': 'Regiao', 
             'Estado - Sigla': 'Estado'
            }, inplace=True          
)

# Exibindo o DataFrame
st.sidebar.subheader('Filtros')

# Criando o SIDEBAR e FILTRANDO
filtro_regiao = st.sidebar.multiselect(
    label="Regiao: ",
    options=df['Regiao'].unique(),
    default=df['Regiao'].unique()
)

filtro_bandeira = st.sidebar.multiselect(
    label='Bandeira: ',
    options=df['Bandeira'].unique(),
    default=df['Bandeira'].unique()
)

filtro_estado = st.sidebar.multiselect(
    label='Estado: ',
    options=df['Estado'].unique(),
    default=df['Estado'].unique()
)

# QUERY PARA FILTRAR BANDEIRA, REGIÃO E ESTADo
df_filtrado = df.query(f'Bandeira == @filtro_bandeira and Regiao == @filtro_regiao and Estado == @filtro_estado')

# Criando colunas para exibir as operações sum, mean, median e max
esquerda, subcentro, centro, direita = st.columns(4)

try:
    # Operações
    soma_valor_venda = int(df_filtrado['Valor de Venda'].sum())
    media_valor_venda = int(df_filtrado['Valor de Venda'].mean())
    mediana_valor_venda = int(df_filtrado['Valor de Venda'].median())
    maior_valor_venda = int(df_filtrado['Valor de Venda'].max())
except:
    soma_valor_venda = 0
    media_valor_venda = 0
    mediana_valor_venda = 0
    maior_valor_venda = 0

with esquerda:
    st.subheader(':moneybag:Média:')
    st.subheader(f'R$ {media_valor_venda:.2f}')

with subcentro:
    st.subheader('➕Soma:')
    st.subheader(f'R$ {soma_valor_venda:.2f}')

with centro:
    st.subheader(':chart:Mediana:')
    st.subheader(f'R$ {mediana_valor_venda:.2f}')

with direita:
    st.subheader(':arrow_up_small:Maior:')
    st.subheader(f'R$ {maior_valor_venda:.2f}')


################## CRIANDO OS GRÁFICOS #####################

#Bandeira e valor de venda
grafico_bandeira_valor_venda = px.bar(
    df_filtrado[['Bandeira', 'Valor de Venda']],
    x='Valor de Venda',
    y='Bandeira',
    title="Bandeira e Valor de Venda",
    color="Bandeira"
)
st.plotly_chart(grafico_bandeira_valor_venda)

# Estado e Valor de Venda
grafico_estado_valor_venda = px.bar(
    df_filtrado[['Estado', 'Valor de Venda']],
    x='Valor de Venda',
    y='Estado',
    title="Estado e Valor de Venda",
    color="Estado"
)
st.plotly_chart(grafico_estado_valor_venda)

# Regiao e Valor de Venda
grafico_regiao_valor_venda = px.bar(
    df_filtrado[['Regiao', 'Valor de Venda']],
    x='Valor de Venda',
    y='Regiao',
    title="Regiao e Valor de Venda",
    color="Regiao"
)
st.plotly_chart(grafico_regiao_valor_venda)

st.dataframe(df_filtrado) 


