# Proyecto UCU · Grupo G

Proyecto final del curso **Python para Análisis de Datos**.

**Integrantes:** Camila, Maximiliano y Arthur.

Se cuenta con un dataset proveniente de Kaggle que se obtuvo utilizando la API de Spotify. Se tienen 114.000 registros que corresponden a _tracks_ (pistas de audio que incluyen canciones y rutinas de Stand Up), donde para cada género (_track_genre_) posible se incluyen 1000 pistas.

- **Repositorio:** [Ucu_diploma_python](https://github.com/ArthurMartinezUcu/Ucu_diploma_python)
- **Aplicación Streamlit:** [ucu-grupo-g-2026.streamlit.app](https://ucu-grupo-g-2026.streamlit.app/)
- **Dataset:** [Spotify Tracks Dataset en Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)

## Pregunta de análisis

### ¿Qué atributos de una canción están relacionados con la popularidad?

`popularity` es la variable objetivo y se expresa en una escala de 0 a 100.
El notebook estudia su relación con duración, bailabilidad, energía, volumen, contenido hablado, acústica, instrumentalidad, probabilidad de grabación en vivo, valencia musical y tempo.

## Resultado del procesamiento

El dataset original contiene 114.000 filas y 89.741 identificadores de pista únicos.
Después de la limpieza se obtiene `spotify_processed.csv`, con:

- 88.404 pistas únicas por `track_id`
- 15 columnas
- ningún valor faltante
- ningún identificador de pista duplicado

## Principales observaciones del EDA

- `energy` y `loudness` presentan una correlación positiva fuerte, cercana a `0,76`.
- `energy` y `acousticness` presentan una correlación negativa fuerte, cercana a `-0,75`.
- `loudness` y `acousticness` mantienen una asociación negativa aproximada de `-0,59`.
- `danceability` y `valence` presentan una asociación positiva moderada, cercana a `0,49`.
- Ningún atributo individual muestra una correlación lineal fuerte con `popularity`. La relación de mayor magnitud es la de `instrumentalness`, cercana a `-0,13`.

Estas relaciones describen asociaciones estadísticas y no implican causalidad.

## Limpieza y preparación

El flujo implementado en `notebooks/notebook.ipynb` realiza:

1. Validación de estructura, tipos, nulos y duplicados.
2. Eliminación de filas con valores iguales a cero en `tempo`, `danceability` o `valence`.
3. Identificación de contenido hablado del género `comedy` mediante `speechiness`.
4. Eliminación de columnas identificadoras y descriptivas que no se utilizan en el análisis.
5. Eliminación de registros duplicados por `track_id`.
6. Exclusión de pistas superiores a diez minutos.
7. Análisis univariado y multivariado.
8. Separación de los datos en conjuntos de entrenamiento y prueba.
9. Estandarización de variables continuas y one-hot encoding de `time_signature`.
10. Selección de las diez características principales mediante `f_regression`.

El ranking de características se utiliza como una herramienta exploratoria para comparar la relación de cada variable con `popularity`. Estas asociaciones no implican causalidad ni permiten evaluar por sí solas la capacidad predictiva de un modelo.

## Aplicación Streamlit

`app.py` carga el dataset procesado y permite:

- filtrar por popularidad, duración, energía y contenido explícito;
- consultar métricas que se recalculan después de aplicar los filtros;
- visualizar la distribución de la popularidad;
- comparar correlaciones lineales con popularidad;
- comparar la popularidad con otro atributo seleccionado;
- observar una tendencia lineal orientativa;
- consultar media, mediana, desviación estándar, cuartiles, mínimo, máximo y rango;
- inspeccionar los registros filtrados.

## Estructura

```text
Ucu_diploma_python/
├── app.py
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── README.md
│   └── processed/
│       ├── README.md
│       └── spotify_processed.csv
└── notebooks/
    ├── import_dataset.ipynb
    └── notebook.ipynb
```

El CSV original no se adjunta por su tamaño. Se descarga en `notebooks/import_dataset.ipynb`.
El CSV procesado sí forma parte del repositorio porque la aplicación lo necesita para iniciar.

## Instrucciones para cargar el proyecto y la aplicación de Streamlit
1. Instalar las dependencias desde el archivo `requirements.txt`

```bash
$ pip install -r requirements.txt
```
2. Ejecutar el archivo `app.py` (o acceder mediante el link previamente indicado en este README.)

```bash
$ streamlit run app.py
```