import streamlit as st
import plotly.express as px


def cidades(df):

    # =========================
    # CORES POR PAÍS (EDITÁVEL)
    # =========================
    CORES_PAISES = {
        "Brazil": "#1CAC1C",
        "India": "#F7B911",
        "United States of America": "#7A39F3",
        "England": "#2D30F5",
        "Australia": "#AE13D4",
        "Canada": "#0099FF",
        "South Africa": "#74CF0C",
        "Qatar": "#5560F7",
        "Turkey": "#0ADCE3",
        "Indonesia": "#E95325",
        "Philippines": "#0038A8",
        "Sri Lanka": "#8D153A",
        "United Arab Emirates": "#00732F",
        "Singapure": "#EF3340",
        "New Zeland": "#969393",
    }

    # =========================
    # TÍTULO
    # =========================
    st.markdown(
        "<h2 style='color:#ffffff;'>🌆 Visão Cidades</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # =========================
    # FILTRO SIDEBAR - PAÍSES
    # =========================
    st.sidebar.title("Filtros - Cidades")

    paises = sorted(df["country"].unique())

    paises_selecionados = st.sidebar.multiselect(
    "Selecione os países:",
    options=paises,
    default=paises
)

    # Aplica filtro
    df = df[df["country"].isin(paises_selecionados)]

    # =========================
    # MAPA DE CORES
    # =========================
    color_map = CORES_PAISES

    # =========================
    # 1️⃣ Top 10 cidades com mais restaurantes
    # =========================
    top_rest = (
        df.groupby(["country", "city"])["restaurant_id"]
        .nunique()
        .reset_index(name="qtd_restaurantes")
        .sort_values("qtd_restaurantes", ascending=False)
        .head(10)
    )

    fig1 = px.bar(
        top_rest,
        x="city",
        y="qtd_restaurantes",
        color="country",
        title="Top 10 Cidades com Mais Restaurantes",
        color_discrete_map=color_map
    )

    # =========================
    # 2️⃣ Top 7 cidades (avaliação > 4)
    # =========================
    rating_maior_4 = (
        df.groupby(["country", "city"])
        .agg(
            media=("aggregate_rating", "mean"),
            qtd=("restaurant_id", "nunique")
        )
        .reset_index()
    )

    top_rating_alto = (
        rating_maior_4[rating_maior_4["media"] > 4]
        .sort_values("media", ascending=False)
        .head(7)
    )

    fig2 = px.bar(
        top_rating_alto,
        x="city",
        y="media",
        color="country",
        title="Top 7 Cidades com Média maior que 4",
        color_discrete_map=color_map
    )

    # =========================
    # 3️⃣ cidades (avaliação <= 2.5)
    # =========================
    top_rating_baixo = (
        rating_maior_4[rating_maior_4["media"] <= 2.5]
        .sort_values("media")
        .head(7)
    )

    fig3 = px.bar(
        top_rating_baixo,
        x="city",
        y="media",
        color="country",
        title="Cidades com Média menor que 2.5",
        color_discrete_map=color_map
    )

    # =========================
    # 4️⃣ Top 10 cidades com mais culinárias distintas
    # =========================
    top_cuisines = (
        df.groupby(["country", "city"])["cuisines"]
        .nunique()
        .reset_index(name="qtd_culinarias")
        .sort_values("qtd_culinarias", ascending=False)
        .head(10)
    )

    fig4 = px.bar(
        top_cuisines,
        x="city",
        y="qtd_culinarias",
        color="country",
        title="Top 10 Cidades com Mais Tipos de Culinária",
        color_discrete_map=color_map
    )

    # =========================
    # LAYOUT FINAL
    # =========================

    # Linha 1
    st.plotly_chart(fig1, use_container_width=True)

    # Linha 2
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig2, use_container_width=True)
    col2.plotly_chart(fig3, use_container_width=True)

    # Linha 3
    st.plotly_chart(fig4, use_container_width=True)