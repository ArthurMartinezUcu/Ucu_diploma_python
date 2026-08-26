import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/spotify_processed.csv")

st.set_page_config(page_title="UCU Curso Pyton EDA Dataset de Spotify", page_icon="🎵",layout="wide")

st.title("🎵 UCU Curso Pyton EDA Dataset de Spotify")
st.title("Grupo G - Camila, Maxi, Arthur")
st.write("Exploración de las características musicales y la popularidad de las canciones del dataset de Spotify.")
st.subheader("Dataset")

col1, col2, col3 = st.columns(3)
col1.metric("Canciones", len(df))
col2.metric("Géneros", df["track_genre"].nunique())
col3.metric("Popularidad promedio", round(df["popularity"].mean(), 2))


st.subheader("Filtrar canciones")

generos = sorted(df["track_genre"].dropna().unique())

genero = st.selectbox("Seleccioná un género:", ["Todos"] + generos)

if genero != "Todos":
    df_filtrado = df[df["track_genre"] == genero]
else:
    df_filtrado = df


st.dataframe(
    df_filtrado[
        [
            "track_name",
            "artists",
            "track_genre",
            "popularity",
            "danceability",
            "energy",
            "speechiness"
        ]
    ].head(100),
    use_container_width=True
)

st.subheader("Distribución de popularidad")

fig, ax = plt.subplots()
ax.hist(
    df_filtrado["popularity"],
    bins=20
)

ax.set_xlabel("Popularidad")
ax.set_ylabel("Cantidad de canciones")
ax.set_title("Distribución de popularidad")

st.pyplot(fig)
