import streamlit as st
import pandas as pd
import plotly.express as px

# Carrega os dados dos bairros em um DataFrame
data = pd.read_csv("base.csv")

# Mapeia o nome do tipo de endemia para o nome da coluna correspondente no DataFrame
disease_mapping = {
    "Dengue": "den",
    "Zika": "zik",
    "Chikungunya": "chi"
}

# Escolhe o tipo de endemia a ser visualizado
disease_name = st.sidebar.selectbox("Tipo de Endemia", list(disease_mapping.keys()))

# Obtém o nome da coluna correspondente no DataFrame
disease_column = disease_mapping[disease_name]

# Filtra os dados para o tipo de endemia selecionado
filtered_data = data[data[disease_column] > 0]

# Define as cores personalizadas
color_scale = [(0.0, 'green'), (0.3, 'yellow'), (1.0, 'red')]

# Cria a visualização com Plotly Express
fig = px.scatter_mapbox(filtered_data, lat="lat", lon="lon", color=disease_column, size=disease_column,
                        color_continuous_scale=color_scale, size_max=30, zoom=13,
                        hover_name="bairro", hover_data=[disease_column],
                        text="bairro",  # Define o texto que aparecerá ao passar o mouse sobre a bolha
                        mapbox_style="carto-positron",  # Define o estilo do mapa como carto-positron
                        width=800, height=600,  # Define a largura e altura do mapa
                        center=dict(lat=-7.4931, lon=-38.9867))  # Define o centro do mapa para Brejo Santo, Ceará

# Ajusta as margens para remover o excesso de espaço
fig.update_layout(margin=dict(l=0, t=0, r=0, b=0))

# Define a cor do texto dos nomes dos bairros como preto
fig.update_traces(textfont_color="black")

# Exibe a visualização na interface
st.plotly_chart(fig)
