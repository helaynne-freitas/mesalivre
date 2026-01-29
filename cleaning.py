
import pandas as pd
import inflection

df = pd.read_csv("data.csv")

print(df.head)
df.info()

print(df.columns)

# -----------------------------
# DICIONÁRIOS (REGRAS DE NEGÓCIO)
# -----------------------------

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

# -----------------------------
# FUNÇÕES AUXILIARES
# -----------------------------

def country_name(country_code):
    return COUNTRIES.get(country_code, "Unknown")


def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


def color_name(color_code):
    return COLORS.get(color_code, "unknown")


def rename_columns(dataframe):
    df = dataframe.copy()

    df.columns = (
        df.columns
        .str.title()
        .str.replace(" ", "")
        .map(inflection.underscore)
    )

    return df


# -----------------------------
# FUNÇÃO PRINCIPAL DE LIMPEZA
# -----------------------------

def dataframe(df):
    df = df.copy()

    # 1. Renomear colunas
    df = rename_columns(df)

    # 2. Criar nome do país
    df["country"] = df["country_code"].apply(country_name)

    # 3. Criar tipo de preço
    df["price_type"] = df["price_range"].apply(create_price_type)

    # 4. Criar nome da cor do rating
    df["rating_color_name"] = df["rating_color"].apply(color_name)

    # 5. Ajustar cuisines (primeiro tipo)
    df["cuisines"] = df["cuisines"].fillna("Unknown")
    df["cuisines"] = df["cuisines"].apply(lambda x: x.split(",")[0])

    # 6. Converter flags 0/1 para boolean
    flag_cols = [
        "has_table_booking",
        "has_online_delivery",
        "is_delivering_now",
        "switch_to_order_menu",
    ]

    for col in flag_cols:
        df[col] = df[col].astype(bool)

    # 7. Garantir tipos corretos
    df["aggregate_rating"] = df["aggregate_rating"].astype(float)
    df["votes"] = df["votes"].astype(int)

    return df
