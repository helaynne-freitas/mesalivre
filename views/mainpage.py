
import streamlit as st
import folium
from streamlit_folium import folium_static


def mainpage(df):

    # =========================
    # TOPO
    # =========================
    st.markdown(
        """
        <h2 style="color:#8fdd10;">
            🍜 O Melhor lugar para encontrar seu mais novo restaurante favorito!
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # =========================
    # KPIs
    # =========================
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Restaurantes Cadastrados", df["restaurant_id"].nunique())
    col2.metric("Países Cadastrados", df["country"].nunique())
    col3.metric("Cidades Cadastradas", df["city"].nunique())
    col4.metric("Avaliações Feitas na Plataforma", df["votes"].sum())
    col5.metric("Tipos de Culinárias Oferecidas", df["cuisines"].nunique())

    st.markdown("---")

    # =========================
    # FILTRO POR PAÍS
    # =========================
    st.sidebar.title("Filtros")

    paises = st.sidebar.multiselect(
        "Selecione os países",
        options=df["country"].unique(),
        default=df["country"].unique()
    )

    df_filtrado = df[df["country"].isin(paises)]

    # =========================
    # DOWNLOAD
    # =========================
    st.sidebar.download_button(
        label="📥 Baixar dados tratados",
        data=df_filtrado.to_csv(index=False),
        file_name="dados_tratados.csv",
        mime="text/csv"
    )

    # =========================
    # MAPA MUNDIAL (ESCURÃO 🌑)
    # =========================
    st.markdown("### 🌍 Restaurantes pelo mundo")

    mapa = folium.Map(
        location=[0, 0],
        zoom_start=2,
        tiles="CartoDB dark_matter"
    )

    for _, row in df_filtrado.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            fill=True,
            fill_opacity=0.7
        ).add_to(mapa)

    folium_static(mapa, width=1200, height=500)

