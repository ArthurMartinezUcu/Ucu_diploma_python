from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


RUTA_DATOS = Path(__file__).parent / "data" / "processed" / "spotify_processed.csv"
URL_REPOSITORIO = "https://github.com/ArthurMartinezUcu/Ucu_diploma_python"
URL_DATASET = "https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset"

NOMBRES_VARIABLES = {
    "popularity": "Popularidad",
    "duration_min": "Duración (min)",
    "danceability": "Bailabilidad",
    "energy": "Energía",
    "loudness": "Volumen (dB)",
    "speechiness": "Contenido hablado",
    "acousticness": "Acústica",
    "instrumentalness": "Instrumentalidad",
    "liveness": "En vivo",
    "valence": "Valencia musical",
    "tempo": "Tempo (BPM)",
}

COLUMNAS_ANALISIS = list(NOMBRES_VARIABLES)


@st.cache_data(show_spinner=False)
def cargar_datos(ruta):
    datos = pd.read_csv(ruta)
    datos["duration_min"] = datos["duration_ms"] / 60_000
    datos["explicit_label"] = datos["explicit"].map({0: "No explícita", 1: "Explícita"})
    return datos


def dar_estilo(figura, alto=420):
    figura.update_layout(
        height=alto,
        margin=dict(l=20, r=20, t=55, b=20),
        legend_title_text="",
    )
    return figura


def crear_resumen(datos):
    numericas = datos[COLUMNAS_ANALISIS]
    resumen = pd.DataFrame(
        {
            "Media": numericas.mean(),
            "Mediana": numericas.median(),
            "Desv. estándar": numericas.std(),
            "Q1": numericas.quantile(0.25),
            "Q3": numericas.quantile(0.75),
            "Mínimo": numericas.min(),
            "Máximo": numericas.max(),
            "Rango": numericas.max() - numericas.min(),
        }
    )
    resumen.index = [NOMBRES_VARIABLES[columna] for columna in resumen.index]
    return resumen.round(3)


st.set_page_config(
    page_title="Proyecto UCU · Grupo G",
    page_icon="🎧",
    layout="wide",
)

if not RUTA_DATOS.exists():
    st.error("No se encontró el dataset procesado.")
    st.stop()

datos = cargar_datos(RUTA_DATOS)

with st.sidebar:
    st.header("Filtros")

    rango_popularidad = st.slider(
        "Popularidad",
        int(datos["popularity"].min()),
        int(datos["popularity"].max()),
        (int(datos["popularity"].min()), int(datos["popularity"].max())),
    )
    duracion_minutos = (
        float(np.floor(datos["duration_min"].min() * 10) / 10),
        float(np.ceil(datos["duration_min"].max() * 10) / 10),
    )
    rango_duracion = st.slider(
        "Duración (minutos)",
        duracion_minutos[0],
        duracion_minutos[1],
        duracion_minutos,
        step=0.1,
    )
    rango_energia = st.slider(
        "Energía",
        float(datos["energy"].min()),
        float(datos["energy"].max()),
        (float(datos["energy"].min()), float(datos["energy"].max())),
        step=0.01,
    )
    filtro_explicito = st.multiselect(
        "Contenido explícito",
        ["No explícita", "Explícita"],
        default=["No explícita", "Explícita"],
    )

    st.divider()
    st.link_button("Repositorio en GitHub", URL_REPOSITORIO, width="stretch")
    st.link_button("Dataset original", URL_DATASET, width="stretch")
    st.caption("Proyecto UCU · Maximiliano Friss y Arthur Martinez")

condicion = (
    datos["popularity"].between(*rango_popularidad)
    & datos["duration_min"].between(*rango_duracion)
    & datos["energy"].between(*rango_energia)
    & datos["explicit_label"].isin(filtro_explicito)
)
datos_filtrados = datos.loc[condicion].copy()

st.title("🎧 ¿Qué atributos están relacionados con la popularidad?")
st.write(
    "Análisis exploratorio para observar qué atributos se relacionan con la popularidad. "
    "La aplicación no realiza una predicción, sino que muestra asociaciones y tendencias."
)
st.caption(f"Dataset completo: {len(datos):,} canciones".replace(",", "."))

if datos_filtrados.empty:
    st.warning("El filtro utilizado no trajo datos.")
    st.stop()

columna_1, columna_2, columna_3, columna_4 = st.columns(4)
columna_1.metric(
    "Canciones visibles",
    f"{len(datos_filtrados):,}".replace(",", "."),
    f"{len(datos_filtrados) / len(datos):.1%} del total",
)
columna_2.metric("Popularidad media", f"{datos_filtrados['popularity'].mean():.1f} / 100")
columna_3.metric("Duración mediana", f"{datos_filtrados['duration_min'].median():.1f} min")
columna_4.metric("Bailabilidad media", f"{datos_filtrados['danceability'].mean():.2f}")

pestaña_panorama, pestaña_relaciones, pestaña_datos = st.tabs(
    ["Panorama", "Relaciones", "Datos y resumen"]
)

with pestaña_panorama:
    st.subheader("Resumen general")
    columna_histograma, columna_correlacion = st.columns([1.35, 1])

    with columna_histograma:
        histograma = px.histogram(
            datos_filtrados,
            x="popularity",
            nbins=30,
            color_discrete_sequence=["#18a957"],
            labels={"popularity": "Popularidad", "count": "Canciones"},
            title="Distribución de la popularidad",
        )
        histograma.add_vline(
            x=datos_filtrados["popularity"].median(),
            line_dash="dash",
            annotation_text="Mediana",
        )
        st.plotly_chart(dar_estilo(histograma), width="stretch")

    with columna_correlacion:
        correlaciones = (
            datos_filtrados[COLUMNAS_ANALISIS]
            .corr()["popularity"]
            .drop("popularity")
            .dropna()
            .sort_values()
        )

        if correlaciones.empty:
            st.info("No hay correlación.")
        else:
            tabla_correlaciones = correlaciones.rename_axis("variable").reset_index(name="correlación")
            tabla_correlaciones["variable"] = tabla_correlaciones["variable"].map(NOMBRES_VARIABLES)
            tabla_correlaciones["dirección"] = np.where(
                tabla_correlaciones["correlación"] >= 0, "Positiva", "Negativa"
            )
            grafico_correlaciones = px.bar(
                tabla_correlaciones,
                x="correlación",
                y="variable",
                orientation="h",
                color="dirección",
                color_discrete_map={"Positiva": "#18a957", "Negativa": "#f28b66"},
                title="Correlación con popularidad",
            )
            st.plotly_chart(dar_estilo(grafico_correlaciones), width="stretch")

    if correlaciones.empty:
        variable_destacada = "No disponible"
        valor_correlacion = "No hay correlaciones."
    else:
        variable_mayor_correlacion = correlaciones.abs().idxmax()
        variable_destacada = NOMBRES_VARIABLES[variable_mayor_correlacion]
        valor_correlacion = f"{correlaciones[variable_mayor_correlacion]:+.3f}"

    resultado_1, resultado_2, resultado_3 = st.columns(3)
    resultado_1.metric("Mayor asociación", variable_destacada, valor_correlacion)
    resultado_2.metric(
        "Popularidad igual o mayor a 70",
        f"{(datos_filtrados['popularity'] >= 70).mean():.1%}",
    )
    resultado_3.metric("Contenido explícito", f"{datos_filtrados['explicit'].mean():.1%}")
    st.caption("Las correlaciones muestran asociación, no causalidad.")

with pestaña_relaciones:
    st.subheader("Explorador de relaciones")

    selector_1, selector_2 = st.columns(2)
    selector_1.text_input(
        "Eje vertical",
        "Popularidad",
        disabled=True,
    )
    columnas_para_comparar = [
        columna for columna in COLUMNAS_ANALISIS if columna != "popularity"
    ]
    variable_x = selector_2.selectbox(
        "Eje horizontal",
        columnas_para_comparar,
        index=columnas_para_comparar.index("energy"),
        format_func=NOMBRES_VARIABLES.get,
    )
    variable_y = "popularity"

    muestra = datos_filtrados.sample(min(len(datos_filtrados), 6_000), random_state=15)
    dispersion = px.scatter(
        muestra,
        x=variable_x,
        y=variable_y,
        opacity=0.5,
        labels={
            variable_x: NOMBRES_VARIABLES[variable_x],
            variable_y: NOMBRES_VARIABLES[variable_y],
        },
        title=f"{NOMBRES_VARIABLES[variable_y]} vs. {NOMBRES_VARIABLES[variable_x]}",
    )

    if muestra[variable_x].nunique() > 1:
        pendiente, ordenada = np.polyfit(muestra[variable_x], muestra[variable_y], 1)
        valores_x = np.linspace(muestra[variable_x].min(), muestra[variable_x].max(), 100)
        dispersion.add_scatter(
            x=valores_x,
            y=pendiente * valores_x + ordenada,
            mode="lines",
            name="Tendencia",
            line=dict(color="black", dash="dash"),
        )

    st.plotly_chart(dar_estilo(dispersion, 560), width="stretch")

with pestaña_datos:
    st.subheader("Resumen descriptivo")
    st.info("La popularidad cambia con el tiempo y también depende de información que no tenemos, "
        "como promoción, playlists o seguidores del artista.")
    st.dataframe(crear_resumen(datos_filtrados), width="stretch")

    st.subheader("Explorar registros")
    nombres_columnas = {
        "track_id": "ID de canción",
        "explicit_label": "Contenido",
        "time_signature": "Compás",
    }
    columnas_visibles = st.multiselect(
        "Columnas visibles",
        [
            "track_id",
            *COLUMNAS_ANALISIS,
            "explicit_label",
            "time_signature",
        ],
        default=[
            "track_id",
            "popularity",
            "duration_min",
            "danceability",
            "energy",
            "valence",
            "tempo",
        ],
        format_func=lambda valor: NOMBRES_VARIABLES.get(valor, nombres_columnas.get(valor, valor)),
    )

    if columnas_visibles:
        st.dataframe(datos_filtrados[columnas_visibles].head(500), width="stretch", hide_index=True)
    else:
        st.info("Seleccione al menos una columna.")

st.caption(f"[Dataset original]({URL_DATASET}) · [Código fuente]({URL_REPOSITORIO}) · Proyecto UCU")
