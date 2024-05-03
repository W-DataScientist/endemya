import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.colors as colors
import plotly.graph_objects as go

# Carrega os dados dos bairros em um DataFrame
data = pd.read_csv("base.csv")

# Mapeia o nome do tipo de virus para o nome da coluna correspondente no DataFrame
disease_mapping = {
    "Dengue": "DENGUE",
    "Chikungunya": "CHIKUNGUNYA",
    "Zika": "ZIKA"
}

# Escolhe o tipo de endemia a ser visualizado
disease_name = st.sidebar.selectbox("Tipo de vírus", list(disease_mapping.keys()))

# Obtém o nome da coluna correspondente no DataFrame
disease_column = disease_mapping[disease_name]

# Filtra os dados para o tipo de virus selecionado
filtered_data = data[data[disease_column] > 0]

# Define as cores personalizadas
color_scale = colors.diverging.RdYlGn_r

# Cria a visualização com Plotly Express
fig_map = px.scatter_mapbox(filtered_data, lat="lat", lon="lon", color=disease_column, size=disease_column,
                        color_continuous_scale=color_scale, size_max=30, zoom=10.8,
                        hover_name="PSF", hover_data=[disease_column],
                        text="PSF",  # Define o texto que aparecerá ao passar o mouse sobre a bolha
                        mapbox_style="carto-positron",  # Define o estilo do mapa como carto-positron
                        width=800, height=600,  # Define a largura e altura do mapa
                        center=dict(lat=-7.5053, lon=-38.9594))  # Define o centro do mapa para Brejo Santo, Ceará

# Ajusta as margens para remover o excesso de espaço
fig_map.update_layout(margin=dict(l=0, t=0, r=0, b=0))

# Define a cor do texto dos nomes dos bairros como preto
fig_map.update_traces(textfont_color="black", marker=dict(opacity=0.5)) # Ajusta a opacidade das bolhas

# Adiciona um título acima do mapa com o tamanho da fonte reduzido
st.subheader(f"Mapa de casos de {disease_name} em Brejo Santo-CE (2023)")

# Exibe a visualização na interface
st.plotly_chart(fig_map)

# Linha separadora
st.markdown("---")

# Criar o gráfico de barras na tela principal
st.subheader(f"Números de casos de {disease_name} por PSF (2023)")

# Ordenar os dados por quantidade do tipo de endemia
sorted_data = filtered_data.sort_values(by=disease_column, ascending=True)  # Agora ordenado de forma descendente

# Criar o gráfico de barras na tela principal
fig_bar = px.bar(sorted_data, x=disease_column, y="PSF", orientation='h', text=disease_column, color=disease_column, color_continuous_scale=color_scale)  # Adicionando o texto com o número de casos

# Remover os rótulos do eixo x
fig_bar.update_xaxes(title=None, showticklabels=False)

# Definir o formato dos números na barra para um padrão de tamanho e orientação horizontal
fig_bar.update_traces(texttemplate='%{text:.0f}', textposition='outside')

# Ajustar o tamanho do gráfico de barras
fig_bar.update_layout(width=795, height=500)

# Exibir o gráfico de barras na tela principal
st.plotly_chart(fig_bar)

# Linha separadora
st.markdown("---")

# Restante do conteúdo

# Definir o título do aplicativo
st.subheader("Casos de Dengue, Chikungunya e Zika ao longo de 2023")

# Criar um gráfico de linhas
fig = go.Figure()

# Adicionar linhas para cada doença
fig.add_trace(go.Scatter(x=data['MES'], y=data['DENGUE-2023'], mode='lines+markers', name='Dengue', line=dict(color='#FF5733')))
fig.add_trace(go.Scatter(x=data['MES'], y=data['CHIKUNGUNYA-2023'], mode='lines+markers', name='Chikungunya', line=dict(color='#F9DC5C')))
fig.add_trace(go.Scatter(x=data['MES'], y=data['ZIKA-2023'], mode='lines+markers', name='Zika', line=dict(color='#65C271')))

# Atualizar o layout do gráfico
fig.update_layout(xaxis_title='Mês', yaxis_title='Número de casos', 
                  legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                  xaxis=dict(tickangle=90))

# Exibir o gráfico
st.plotly_chart(fig)

# Info
st.markdown("1- Dados sujeitos a alterações, visto que ainda existem casos aguardando resultado laboratorial de sorologias.")
st.markdown("2- Quanto ao número de casos de Dengue, nota-se uma tendência decrescente, tendo como parâmetro o Mês de março, onde foi registrado o maior número de casos. Entretanto observa-se tambem uma transmissão sustentavel durante todo o ano com casos confirmados por laboratório.")
st.markdown("3- Quanto ao número de casos de Chikungunya, nota-se uma tendência decrescente durante todo o ano de 2023, sendo o Mês de Janeiro o de maior incidência. Quanto a positividade, apresenta-se em baixa visto que no ano anterior(2022) prevaleceu um ano epidemico para Chikungunya.")
st.markdown("4- TODOS OS CASOS DE ZIKA NOTIFICADOS FORAM DESCARTADOS POR EXAME LABORATORIAL")
st.markdown("**FONTE:** SINANNET_SMS_BREJO SANTO - ATUALIZAÇÃO 30/01/2024")
