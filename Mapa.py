import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.colors as colors

# Carrega os dados dos bairros em um DataFrame
data = pd.read_csv("base.csv")

# Mapeia o nome do tipo de endemia para o nome da coluna correspondente no DataFrame
disease_mapping = {
    "Dengue": "DENGUE",
    "Zika": "ZIKA",
    "Chikungunya": "CHIKUNGUNYA"
}

# Escolhe o tipo de endemia a ser visualizado
disease_name = st.sidebar.selectbox("Tipo de vírus", list(disease_mapping.keys()))

# Obtém o nome da coluna correspondente no DataFrame
disease_column = disease_mapping[disease_name]

# Filtra os dados para o tipo de endemia selecionado
filtered_data = data[data[disease_column] > 0]

# Define as cores personalizadas
color_scale = colors.diverging.RdYlGn_r

# Cria a visualização com Plotly Express
fig = px.scatter_mapbox(filtered_data, lat="lat", lon="lon", color=disease_column, size=disease_column,
                        color_continuous_scale=color_scale, size_max=30, zoom=10.8,
                        hover_name="PSF", hover_data=[disease_column],
                        text="PSF",  # Define o texto que aparecerá ao passar o mouse sobre a bolha
                        mapbox_style="carto-positron",  # Define o estilo do mapa como carto-positron
                        width=800, height=600,  # Define a largura e altura do mapa
                        center=dict(lat=-7.5053, lon=-38.9594))  # Define o centro do mapa para Brejo Santo, Ceará

# Ajusta as margens para remover o excesso de espaço
fig.update_layout(margin=dict(l=0, t=0, r=0, b=0))

# Define a cor do texto dos nomes dos bairros como preto
fig.update_traces(textfont_color="black", marker=dict(opacity=0.5)) # Ajusta a opacidade das bolhas

# Adiciona um título acima do mapa com o tamanho da fonte reduzido
st.subheader(f"Mapa de casos de {disease_name} em Brejo Santo-CE (2023)")

# Exibe a visualização na interface
st.plotly_chart(fig)

st.subheader("")

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
