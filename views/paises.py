
import streamlit as st
import plotly.express as px


def paises(df):

    COR_VERDE = ["#6fbd09"]

    # =========================
    # TÍTULO
    # =========================
    st.markdown(
        "<h2 style='color:#ffffff;'>🌍 Visão Países</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # =========================
    # FILTRO POR PAÍS
    # =========================
    st.sidebar.title("Filtros - Países")

    paises_selecionados = st.sidebar.multiselect(
        "Selecione os países",
        options=df["country"].unique(),
        default=df["country"].unique()
    )

    df_filtrado = df[df["country"].isin(paises_selecionados)]

    # =========================
    #  Restaurantes por país
    # =========================
    restaurantes_pais = (
        df_filtrado.groupby("country")["restaurant_id"]
        .nunique()
        .reset_index(name="qtd_restaurantes")
        .sort_values("qtd_restaurantes", ascending=False)
    )

    fig_rest = px.bar(
        restaurantes_pais,
        x="country",
        y="qtd_restaurantes",
        title="Quantidade de Restaurantes por País",
        color_discrete_sequence=COR_VERDE
    )

    st.plotly_chart(fig_rest, use_container_width=True)

    # =========================
    #  Cidades por país
    # =========================
    cidades_pais = (
        df_filtrado.groupby("country")["city"]
        .nunique()
        .reset_index(name="qtd_cidades")
        .sort_values("qtd_cidades", ascending=False)
    )

    fig_city = px.bar(
        cidades_pais,
        x="country",
        y="qtd_cidades",
        title="Quantidade de Cidades por País",
        color_discrete_sequence=COR_VERDE
    )

    st.plotly_chart(fig_city, use_container_width=True)

    # =========================
    #  Avaliação média
    # =========================
    rating_pais = (
        df_filtrado.groupby("country")["aggregate_rating"]
        .mean()
        .reset_index(name="media_avaliacao")
        .sort_values("media_avaliacao", ascending=False)
    )

    fig_rating = px.bar(
        rating_pais,
        x="country",
        y="media_avaliacao",
        title="Média de Avaliação por País",
        color_discrete_sequence=COR_VERDE
    )

    # =========================
    #  Preço médio para dois
    # =========================
    preco_pais = (
        df_filtrado.groupby("country")["average_cost_for_two"]
        .mean()
        .reset_index(name="preco_medio_dois")
        .sort_values("preco_medio_dois", ascending=False)
    )

    fig_price = px.bar(
        preco_pais,
        x="country",
        y="preco_medio_dois",
        title="Preço Médio de um Prato para Dois por País",
        color_discrete_sequence=COR_VERDE
    )

    # =========================
    # LAYOUT FINAL
    # =========================
    col1, col2 = st.columns(2)

    col1.plotly_chart(fig_rating, use_container_width=True)

    col2.plotly_chart(fig_price, use_container_width=True)
