

import streamlit as st
import pandas as pd
from cleaning import dataframe

from views.mainpage import mainpage
from views.paises import paises
from views.cidades import cidades
from views.cozinhas import cozinhas

st.set_page_config(
    page_title="Mesa Livre Dashboard",
    layout="wide"
)

df = pd.read_csv("data.csv")
df = dataframe(df)

# MENU MANUAL
st.sidebar.image("assets/logo.png", use_container_width=True)
pagina = st.sidebar.radio(
    "Escolha uma página",
    ["Main Page", "Países", "Cidades", "Culinária"]
)

# ROTEAMENTO
if pagina == "Main Page":
    mainpage(df)

elif pagina == "Países":
    paises(df)

elif pagina == "Cidades":
    cidades(df)

elif pagina == "Culinária":
    cozinhas(df)
