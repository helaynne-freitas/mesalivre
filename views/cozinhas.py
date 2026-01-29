
import streamlit as st
import pandas as pd
import plotly.express as px

def cozinhas(df):

    st.title("🍳 Visão Tipo de Cozinhas")

    # =========================
    # SIDEBAR – FILTROS
    # =========================
    st.sidebar.header("Filtros")

    qtd_restaurantes = st.sidebar.slider(
        "Selecione a quantidade de Restaurantes que deseja visualizar",
        min_value=1,
        max_value=20,
        value=10
    )

    paises = st.sidebar.multiselect(
        "Selecione os Países",
        options=sorted(df["country"].unique()),
        default=sorted(df["country"].unique())
    )

    culinarias = st.sidebar.multiselect(
        "Selecione os Tipos de Culinária",
        options=sorted(df["cuisines"].unique()),
        default=sorted(df["cuisines"].unique())
    )

    # Aplicando filtros
    df_filtro = df[
        (df["country"].isin(paises)) &
        (df["cuisines"].isin(culinarias))
    ]

    # =========================
    # KPIs – Melhores restaurantes por culinária
    # =========================
    st.subheader("Melhores Restaurantes dos Principais Tipos Culinários")

    df_kpi = (
        df_filtro.loc[:, ["restaurant_name", "cuisines", "aggregate_rating"]]
        .sort_values(["cuisines", "aggregate_rating"], ascending=[True, False])
        .drop_duplicates(subset=["cuisines"])
    )

    cols = st.columns(5)
    for col, (_, row) in zip(cols, df_kpi.head(5).iterrows()):
        col.metric(
            label=row["cuisines"],
            value=row["restaurant_name"],
            delta=f'{row["aggregate_rating"]}/5.0'
        )

    st.divider()

    # =========================
    # TABELA – TOP RESTAURANTES
    # =========================
    
    top_restaurantes = (
    df_filtro.loc[:, [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "cuisines",
        "average_cost_for_two",
        "aggregate_rating",
        "votes"
    ]]
    .sort_values("aggregate_rating", ascending=False)
    .head(qtd_restaurantes)
)


    st.dataframe(top_restaurantes, use_container_width=True)

    st.divider()

    # =========================
    # GRÁFICOS – MELHORES E PIORES CULINÁRIAS
    # =========================
    df_cuisine_rating = (
        df_filtro.groupby("cuisines", as_index=False)["aggregate_rating"]
        .mean()
    )

    col1, col2 = st.columns(2)

    # Melhores
    melhores = df_cuisine_rating.sort_values(
        "aggregate_rating", ascending=False
    ).head(10)

    fig_best = px.bar(
        melhores,
        x="cuisines",
        y="aggregate_rating",
        title="Top 10 Culinárias com Maior Avaliação",
        color_discrete_sequence=["#6abd00"]
    )

    col1.plotly_chart(fig_best, use_container_width=True)

    # Piores
    piores = df_cuisine_rating.sort_values(
        "aggregate_rating", ascending=True
    ).head(10)

    fig_worst = px.bar(
        piores,
        x="cuisines",
        y="aggregate_rating",
        title="Culinárias com Menor Avaliação",
        color_discrete_sequence=["#6abd00"]
    )

    col2.plotly_chart(fig_worst, use_container_width=True)
