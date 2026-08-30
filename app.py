from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


DATA_PATH = Path(__file__).resolve().parent / "data" / "processed" / "spotify_processed.csv"

VARIABLE_LABELS = {
    "popularity": "Popularidad",
    "duration_min": "Duración (min)",
    "danceability": "Bailabilidad",
    "energy": "Energía",
    "loudness": "Volumen (dB)",
    "speechiness": "Contenido hablado",
    "acousticness": "Acústica",
    "instrumentalness": "Instrumentalidad",
    "liveness": "En vivo",
    "valence": "Valencia",
    "tempo": "Tempo (BPM)",
}

ANALYSIS_COLUMNS = list(VARIABLE_LABELS)
SUMMARY_COLUMNS = list(VARIABLE_LABELS)


@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    data["duration_min"] = data["duration_ms"] / 60_000
    data["explicit_label"] = data["explicit"].map({0: "No explícita", 1: "Explícita"})
    data["mode_label"] = data["mode"].map({0: "Menor", 1: "Mayor"})
    return data


def plot_style(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=16, r=16, t=54, b=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        font=dict(family="Inter, ui-sans-serif, system-ui", color="#17211b"),
        title_font=dict(size=17, color="#17211b"),
        legend_title_text="",
        hoverlabel=dict(bgcolor="#17211b", font_color="#ffffff"),
    )
    fig.update_xaxes(gridcolor="#edf1ee", zeroline=False)
    fig.update_yaxes(gridcolor="#edf1ee", zeroline=False)
    return fig


def summary_table(data: pd.DataFrame) -> pd.DataFrame:
    numeric = data[SUMMARY_COLUMNS]
    summary = pd.DataFrame(
        {
            "Media": numeric.mean(),
            "Mediana": numeric.median(),
            "Desv. estándar": numeric.std(),
            "Q1": numeric.quantile(0.25),
            "Q3": numeric.quantile(0.75),
            "Mínimo": numeric.min(),
            "Máximo": numeric.max(),
            "Rango": numeric.max() - numeric.min(),
        }
    )
    summary.index = [VARIABLE_LABELS[column] for column in summary.index]
    return summary.round(3)


st.set_page_config(
    page_title="Spotify Audio Lab · UCU",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --ink: #17211b;
            --muted: #657269;
            --line: #dfe7e1;
            --surface: #ffffff;
            --accent: #18a957;
            --accent-soft: #dff5e8;
        }
        .stApp {
            background:
                radial-gradient(circle at 78% 2%, rgba(29, 185, 84, 0.12), transparent 25rem),
                #f5f7f5;
            color: var(--ink);
        }
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stSidebar"] {
            background: #111914;
            border-right: 1px solid #2b372f;
        }
        [data-testid="stSidebar"] * { color: #eef6f0; }
        [data-testid="stSidebar"] [data-baseweb="slider"] div[role="slider"] {
            background: #1ed760;
        }
        .block-container {
            max-width: 1440px;
            padding-top: 2.1rem;
            padding-bottom: 3rem;
        }
        .hero {
            padding: 1.45rem 1.55rem 1.55rem;
            margin-bottom: 1.15rem;
            border: 1px solid var(--line);
            border-radius: 22px;
            background: rgba(255, 255, 255, 0.86);
            box-shadow: 0 18px 55px rgba(25, 48, 34, 0.07);
        }
        .eyebrow {
            color: var(--accent);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.13em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }
        .hero h1 {
            color: var(--ink);
            font-size: clamp(2rem, 4vw, 3.65rem);
            line-height: 0.98;
            letter-spacing: -0.055em;
            margin: 0;
        }
        .hero-copy {
            color: var(--muted);
            max-width: 760px;
            font-size: 1.02rem;
            line-height: 1.55;
            margin: 0.8rem 0 0;
        }
        .hero-meta {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            margin-top: 1rem;
            padding: 0.34rem 0.62rem;
            border-radius: 999px;
            background: var(--accent-soft);
            color: #087538;
            font-size: 0.8rem;
            font-weight: 700;
        }
        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 0.95rem 1rem;
            box-shadow: 0 8px 25px rgba(25, 48, 34, 0.045);
        }
        [data-testid="stMetricLabel"] { color: var(--muted); }
        [data-testid="stMetricValue"] {
            color: var(--ink);
            font-weight: 750;
            letter-spacing: -0.035em;
        }
        [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 17px;
            overflow: hidden;
            background: var(--surface);
        }
        .insight {
            min-height: 116px;
            padding: 1rem 1.05rem;
            border: 1px solid var(--line);
            border-radius: 16px;
            background: var(--surface);
        }
        .insight-label {
            color: var(--muted);
            font-size: 0.76rem;
            font-weight: 750;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .insight-value {
            color: var(--ink);
            font-size: 1.18rem;
            font-weight: 760;
            line-height: 1.25;
            margin-top: 0.42rem;
        }
        .insight-note {
            color: var(--muted);
            font-size: 0.82rem;
            margin-top: 0.25rem;
        }
        .section-note { color: var(--muted); margin-top: -0.45rem; }
        .stTabs [data-baseweb="tab-list"] { gap: 0.35rem; }
        .stTabs [data-baseweb="tab"] {
            border-radius: 999px;
            padding: 0.35rem 0.85rem;
        }
        .stTabs [aria-selected="true"] { background: var(--accent-soft); }
        @media (max-width: 720px) {
            .block-container { padding-top: 1rem; }
            .hero { padding: 1.1rem; border-radius: 18px; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if not DATA_PATH.exists():
    st.error("No se encontró el dataset procesado. Ejecutá primero el notebook de preparación.")
    st.stop()

df = load_data(DATA_PATH)

with st.sidebar:
    st.markdown("## Sala de control")
    st.caption("Ajustá los filtros y todo el análisis se actualizará al instante.")

    popularity_range = st.slider(
        "Popularidad",
        min_value=int(df["popularity"].min()),
        max_value=int(df["popularity"].max()),
        value=(int(df["popularity"].min()), int(df["popularity"].max())),
        help="Índice de Spotify entre 0 y 100.",
    )
    duration_bounds = (
        float(np.floor(df["duration_min"].min() * 10) / 10),
        float(np.ceil(df["duration_min"].max() * 10) / 10),
    )
    duration_range = st.slider(
        "Duración (minutos)",
        min_value=duration_bounds[0],
        max_value=duration_bounds[1],
        value=duration_bounds,
        step=0.1,
    )
    energy_range = st.slider(
        "Energía",
        min_value=float(df["energy"].min()),
        max_value=float(df["energy"].max()),
        value=(float(df["energy"].min()), float(df["energy"].max())),
        step=0.01,
    )
    explicit_filter = st.multiselect(
        "Contenido explícito",
        options=["No explícita", "Explícita"],
        default=["No explícita", "Explícita"],
    )
    mode_filter = st.multiselect(
        "Modo tonal",
        options=["Mayor", "Menor"],
        default=["Mayor", "Menor"],
    )
    signature_filter = st.multiselect(
        "Compás detectado",
        options=sorted(df["time_signature"].unique().tolist()),
        default=sorted(df["time_signature"].unique().tolist()),
        format_func=lambda value: f"{int(value)}/4" if value in {3, 4, 5} else f"Código {int(value)}",
    )
    st.divider()
    st.caption("Proyecto UCU · Camila, Maxi y Arthur")

mask = (
    df["popularity"].between(*popularity_range)
    & df["duration_min"].between(*duration_range)
    & df["energy"].between(*energy_range)
    & df["explicit_label"].isin(explicit_filter)
    & df["mode_label"].isin(mode_filter)
    & df["time_signature"].isin(signature_filter)
)
filtered = df.loc[mask].copy()

st.markdown(
    f"""
    <section class="hero">
        <div class="eyebrow">Spotify Audio Lab · UCU</div>
        <h1>¿Qué hace popular<br>una canción?</h1>
        <p class="hero-copy">
            Una lectura interactiva de los atributos sonoros de Spotify. Explorá cómo cambian
            la popularidad, la energía y el carácter musical en <strong>{len(filtered):,}</strong> pistas filtradas.
        </p>
        <div class="hero-meta">● Datos listos · {len(df):,} pistas analizadas</div>
    </section>
    """.replace(",", "."),
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("No hay canciones para esta combinación de filtros. Ampliá alguno de los rangos.")
    st.stop()

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Pistas visibles", f"{len(filtered):,}".replace(",", "."), f"{len(filtered) / len(df):.1%} del total")
metric_2.metric("Popularidad media", f"{filtered['popularity'].mean():.1f} / 100")
metric_3.metric("Duración mediana", f"{filtered['duration_min'].median():.1f} min")
metric_4.metric("Bailabilidad media", f"{filtered['danceability'].mean():.2f}")

tab_overview, tab_relationships, tab_data = st.tabs(
    ["Panorama", "Relaciones", "Datos y resumen"]
)

with tab_overview:
    st.subheader("La muestra, de un vistazo")
    st.markdown(
        '<p class="section-note">Distribución del objetivo y variables con mayor asociación lineal.</p>',
        unsafe_allow_html=True,
    )

    chart_col, corr_col = st.columns([1.35, 1])
    with chart_col:
        bins = st.slider("Detalle del histograma", 10, 60, 28, 2)
        histogram = px.histogram(
            filtered,
            x="popularity",
            nbins=bins,
            color_discrete_sequence=["#18a957"],
            labels={"popularity": "Popularidad", "count": "Pistas"},
            title="Distribución de popularidad",
        )
        histogram.update_traces(
            marker_line_color="#ffffff",
            marker_line_width=0.7,
            hovertemplate="Popularidad: %{x}<br>Pistas: %{y}<extra></extra>",
        )
        histogram.add_vline(
            x=filtered["popularity"].median(),
            line_dash="dash",
            line_color="#17211b",
            annotation_text="Mediana",
            annotation_position="top right",
        )
        st.plotly_chart(plot_style(histogram), width="stretch")

    with corr_col:
        correlations = (
            filtered[ANALYSIS_COLUMNS]
            .corr(numeric_only=True)["popularity"]
            .drop("popularity")
            .dropna()
            .sort_values()
        )
        if correlations.empty:
            st.info("Se necesita variación en popularidad para calcular correlaciones.")
        else:
            corr_frame = correlations.rename_axis("variable").reset_index(name="correlación")
            corr_frame["variable"] = corr_frame["variable"].map(VARIABLE_LABELS)
            corr_frame["dirección"] = np.where(corr_frame["correlación"] >= 0, "Positiva", "Negativa")
            corr_chart = px.bar(
                corr_frame,
                x="correlación",
                y="variable",
                orientation="h",
                color="dirección",
                color_discrete_map={"Positiva": "#18a957", "Negativa": "#f28b66"},
                title="Correlación con popularidad",
                labels={"correlación": "Correlación", "variable": ""},
            )
            corr_chart.update_traces(hovertemplate="%{y}: %{x:.3f}<extra></extra>")
            st.plotly_chart(plot_style(corr_chart), width="stretch")

    if correlations.empty:
        strongest_name = "No disponible"
        strongest_note = "Ampliá el rango de popularidad para comparar."
    else:
        strongest = correlations.abs().idxmax()
        strongest_name = VARIABLE_LABELS[strongest]
        strongest_note = f"Correlación {correlations[strongest]:+.3f}; asociación, no causalidad."
    explicit_share = filtered["explicit"].mean()
    high_popularity_share = (filtered["popularity"] >= 70).mean()
    insight_1, insight_2, insight_3 = st.columns(3)
    insight_1.markdown(
        f'<div class="insight"><div class="insight-label">Señal más fuerte</div><div class="insight-value">{strongest_name}</div><div class="insight-note">{strongest_note}</div></div>',
        unsafe_allow_html=True,
    )
    insight_2.markdown(
        f'<div class="insight"><div class="insight-label">Alta popularidad</div><div class="insight-value">{high_popularity_share:.1%} de la muestra</div><div class="insight-note">Pistas con popularidad igual o superior a 70.</div></div>',
        unsafe_allow_html=True,
    )
    insight_3.markdown(
        f'<div class="insight"><div class="insight-label">Contenido explícito</div><div class="insight-value">{explicit_share:.1%} de la muestra</div><div class="insight-note">Proporción dentro de los filtros actuales.</div></div>',
        unsafe_allow_html=True,
    )

with tab_relationships:
    st.subheader("Explorador de relaciones")
    st.markdown(
        '<p class="section-note">Elegí dos atributos y compará hasta 6.000 pistas, con una tendencia lineal orientativa.</p>',
        unsafe_allow_html=True,
    )
    selector_1, selector_2, selector_3 = st.columns([1, 1, 1])
    x_variable = selector_1.selectbox(
        "Eje horizontal",
        ANALYSIS_COLUMNS,
        index=ANALYSIS_COLUMNS.index("energy"),
        format_func=VARIABLE_LABELS.get,
    )
    y_variable = selector_2.selectbox(
        "Eje vertical",
        ANALYSIS_COLUMNS,
        index=ANALYSIS_COLUMNS.index("popularity"),
        format_func=VARIABLE_LABELS.get,
    )
    color_variable = selector_3.selectbox(
        "Agrupar por",
        ["explicit_label", "mode_label"],
        format_func=lambda value: "Contenido explícito" if value == "explicit_label" else "Modo tonal",
    )

    plot_data = filtered.sample(min(len(filtered), 6_000), random_state=15)
    scatter = px.scatter(
        plot_data,
        x=x_variable,
        y=y_variable,
        color=color_variable,
        color_discrete_sequence=["#18a957", "#7467f0"],
        opacity=0.48,
        labels={
            x_variable: VARIABLE_LABELS[x_variable],
            y_variable: VARIABLE_LABELS[y_variable],
            "explicit_label": "Contenido",
            "mode_label": "Modo",
        },
        title=f"{VARIABLE_LABELS[y_variable]} vs. {VARIABLE_LABELS[x_variable]}",
        hover_data={"track_id": True, "duration_min": ":.2f", "popularity": True},
    )
    if x_variable != y_variable and plot_data[x_variable].nunique() > 1:
        slope, intercept = np.polyfit(plot_data[x_variable], plot_data[y_variable], 1)
        trend_x = np.linspace(plot_data[x_variable].min(), plot_data[x_variable].max(), 100)
        scatter.add_trace(
            go.Scatter(
                x=trend_x,
                y=slope * trend_x + intercept,
                mode="lines",
                name="Tendencia",
                line=dict(color="#17211b", width=2, dash="dash"),
                hoverinfo="skip",
            )
        )
    scatter.update_traces(marker=dict(size=7), selector=dict(mode="markers"))
    st.plotly_chart(plot_style(scatter, height=560), width="stretch")

with tab_data:
    st.subheader("Resumen descriptivo")
    st.markdown(
        '<p class="section-note">Todas las métricas corresponden únicamente a la selección visible.</p>',
        unsafe_allow_html=True,
    )
    st.dataframe(
        summary_table(filtered),
        width="stretch",
        column_config={
            column: st.column_config.NumberColumn(column, format="%.3f")
            for column in ["Media", "Mediana", "Desv. estándar", "Q1", "Q3", "Mínimo", "Máximo", "Rango"]
        },
    )

    st.subheader("Explorar registros")
    default_columns = [
        "track_id",
        "popularity",
        "duration_min",
        "danceability",
        "energy",
        "valence",
        "tempo",
    ]
    visible_columns = st.multiselect(
        "Columnas visibles",
        options=["track_id", *ANALYSIS_COLUMNS, "explicit_label", "mode_label", "time_signature"],
        default=default_columns,
        format_func=lambda value: VARIABLE_LABELS.get(
            value,
            {
                "track_id": "ID de pista",
                "explicit_label": "Contenido",
                "mode_label": "Modo",
                "time_signature": "Compás",
            }.get(value, value),
        ),
    )
    if visible_columns:
        st.dataframe(filtered[visible_columns].head(500), width="stretch", hide_index=True)
    else:
        st.info("Seleccioná al menos una columna para ver la tabla.")

    export_data = filtered.drop(columns=["explicit_label", "mode_label"]).to_csv(index=False).encode("utf-8")
    st.download_button(
        "Descargar selección en CSV",
        data=export_data,
        file_name="spotify_seleccion.csv",
        mime="text/csv",
        width="stretch",
    )

st.caption(
    "Fuente: Spotify Tracks Dataset · La correlación describe asociación estadística y no implica causalidad."
)
