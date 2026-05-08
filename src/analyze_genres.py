"""Limpieza y transformación principal del dataset de Steam.

Este archivo es el primer paso del proyecto:

1. lee el CSV original de Kaggle;
2. selecciona las columnas necesarias;
3. crea variables más fáciles de analizar;
4. genera los CSV limpios que usan los notebooks y las figuras.

No se modifican los datos originales de `data/raw/`.
"""

# Permite usar anotaciones de tipos modernas sin problemas de compatibilidad.
# En este script se usa, por ejemplo, en funciones que devuelven list[str] o float | None.
from __future__ import annotations

# ast sirve para convertir textos con forma de estructura de Python en objetos reales.
# Lo usamos para pasar de "['Action', 'RPG']" a ['Action', 'RPG'].
import ast

# re permite trabajar con expresiones regulares.
# Lo usamos para extraer numeros de textos como "100000 - 200000".
import re

# Path permite trabajar con rutas de archivos de forma mas clara y segura.
from pathlib import Path

# pandas es la libreria principal para leer, limpiar, transformar y agrupar datos en tablas.
import pandas as pd


# Rutas principales del proyecto.
# Usamos Path para que el script funcione aunque cambie la carpeta desde la que se ejecuta.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "games_march2025_full.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Diccionario para traducir los generos originales de Steam al castellano.
# Dejamos en ingles los terminos que se suelen usar asi en castellano, como Indie, RPG o Gore.
GENRE_TRANSLATIONS = {
    "Action": "Accion",
    "Adventure": "Aventura",
    "Free To Play": "Gratis",
    "Strategy": "Estrategia",
    "Simulation": "Simulacion",
    "Massively Multiplayer": "Multijugador masivo",
    "Early Access": "Acceso anticipado",
    "Sports": "Deportes",
    "Racing": "Carreras",
    "Utilities": "Utilidades",
    "Design & Illustration": "Diseno e ilustracion",
    "Animation & Modeling": "Animacion y modelado",
    "Photo Editing": "Edicion fotografica",
    "Video Production": "Produccion de video",
    "Education": "Educacion",
    "Violent": "Violento",
    "Game Development": "Desarrollo de videojuegos",
    "Audio Production": "Produccion de audio",
    "Software Training": "Formacion en software",
    "Web Publishing": "Publicacion web",
    "Nudity": "Desnudez",
    "Sexual Content": "Contenido sexual",
    "Movie": "Pelicula",
    "Accounting": "Contabilidad",
    "360 Video": "Video 360",
    "Episodic": "Episodico",
    "Documentary": "Documental",
    "Short": "Cortometraje",
    "Tutorial": "Tutorial",
}


def parse_list(value: object) -> list[str]:
    """Convierte textos con forma de lista en listas reales de Python."""
    # Algunos valores pueden venir vacios o como NaN. En ese caso devolvemos una lista vacia.
    if pd.isna(value):
        return []

    try:
        # En el CSV, columnas como genres vienen como texto: "['Action', 'RPG']".
        # literal_eval permite convertir ese texto en una lista real de forma segura.
        parsed = ast.literal_eval(str(value))
    except (SyntaxError, ValueError):
        # Si el texto no se puede convertir, lo tratamos como dato no utilizable.
        return []

    if isinstance(parsed, list):
        # Limpiamos espacios y eliminamos elementos vacios.
        return [str(item).strip() for item in parsed if str(item).strip()]

    return []


def translate_genres(genres: list[str]) -> list[str]:
    """Traduce una lista de generos al castellano cuando existe traduccion."""
    return [GENRE_TRANSLATIONS.get(genre, genre) for genre in genres]


def owners_midpoint(value: object) -> float | None:
    """Convierte rangos como '100000 - 200000' en su punto medio aproximado."""
    # Si no hay dato, dejamos el valor como None.
    if pd.isna(value):
        return None

    # Extraemos todos los numeros que aparezcan en el texto.
    numbers = [int(match) for match in re.findall(r"\d+", str(value))]

    # Si hay dos numeros, asumimos que son el minimo y el maximo del rango.
    if len(numbers) == 2:
        return sum(numbers) / 2

    # Si solo hay un numero, usamos ese numero como aproximacion.
    if len(numbers) == 1:
        return float(numbers[0])

    return None


def main() -> None:
    # Creamos la carpeta de datos procesados si todavia no existe.
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Seleccionamos solo las columnas necesarias para este primer analisis.
    # Asi evitamos cargar columnas muy pesadas como descripciones largas, imagenes o URLs.
    columns = [
        "appid",
        "name",
        "release_date",
        "genres",
        "estimated_owners",
        "average_playtime_forever",
        "positive",
        "negative",
        "price",
    ]

    # Leemos el CSV original desde data/raw.
    # low_memory=False ayuda a que pandas infiera mejor los tipos en archivos grandes.
    df = pd.read_csv(RAW_PATH, usecols=columns, low_memory=False)

    # Convertimos genres de texto a lista real y despues traducimos los generos al castellano.
    df["lista_generos"] = df["genres"].apply(parse_list).apply(translate_genres)

    # Convertimos estimated_owners, que viene como rango, en un numero aproximado.
    df["usuarios_estimados_aprox"] = df["estimated_owners"].apply(owners_midpoint)

    # Convertimos la fecha a formato datetime. Los errores se convierten en NaT.
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    # Extraemos el ano de lanzamiento para futuros analisis.
    df["ano_lanzamiento"] = df["release_date"].dt.year

    # Creamos variables nuevas que pueden ser utiles para el analisis.
    df["total_resenas"] = df["positive"] + df["negative"]
    df["proporcion_positivas"] = df["positive"] / df["total_resenas"].where(df["total_resenas"] > 0)
    df["es_gratis"] = df["price"].eq(0)
    # Steam guarda average_playtime_forever en minutos.
    # Creamos una version en horas para que sea mas facil de interpretar en el analisis.
    df["tiempo_medio_horas"] = df["average_playtime_forever"] / 60

    # Guardamos una version limpia base con las columnas que nos interesan.
    clean_games = df[
        [
            "appid",
            "name",
            "ano_lanzamiento",
            "lista_generos",
            "estimated_owners",
            "usuarios_estimados_aprox",
            "average_playtime_forever",
            "tiempo_medio_horas",
            "positive",
            "negative",
            "total_resenas",
            "proporcion_positivas",
            "price",
            "es_gratis",
        ]
    ].rename(
        columns={
            "appid": "id_app",
            "name": "nombre",
            "estimated_owners": "usuarios_estimados_rango",
            "average_playtime_forever": "tiempo_medio_minutos",
            "positive": "resenas_positivas",
            "negative": "resenas_negativas",
            "price": "precio",
        }
    ).copy()

    clean_games.to_csv(PROCESSED_DIR / "juegos_steam_limpio_base.csv", index=False)

    # Un juego puede tener varios generos.
    # explode crea una fila por cada genero, manteniendo el resto de datos del juego.
    generos = clean_games.explode("lista_generos")

    # Renombramos la columna para que el resumen final sea mas claro.
    generos = generos.rename(columns={"lista_generos": "genero"})

    # Quitamos filas sin genero o sin usuarios estimados, porque no aportan a esta pregunta.
    generos = generos[generos["genero"].notna() & generos["usuarios_estimados_aprox"].notna()]

    # Agrupamos por genero para calcular metricas agregadas.
    # Mantenemos dos lecturas del tiempo:
    # - tiempo medio incluyendo ceros: muestra el promedio bruto del dataset.
    # - tiempo medio solo con tiempo registrado: evita que los muchos ceros hundan la media.
    resumen_generos = (
        generos.groupby("genero", as_index=False)
        .agg(
            cantidad_juegos=("id_app", "count"),
            usuarios_estimados_total=("usuarios_estimados_aprox", "sum"),
            usuarios_estimados_media=("usuarios_estimados_aprox", "mean"),
            usuarios_estimados_mediana=("usuarios_estimados_aprox", "median"),
            tiempo_medio_horas_todos=("tiempo_medio_horas", "mean"),
            juegos_con_tiempo_registrado=("tiempo_medio_minutos", lambda values: values.gt(0).sum()),
            proporcion_positivas_media=("proporcion_positivas", "mean"),
            total_resenas=("total_resenas", "sum"),
        )
        .sort_values("usuarios_estimados_total", ascending=False)
    )

    generos_con_tiempo = generos[generos["tiempo_medio_minutos"] > 0]
    resumen_tiempo_registrado = (
        generos_con_tiempo.groupby("genero", as_index=False)
        .agg(
            tiempo_medio_horas_solo_con_tiempo=("tiempo_medio_horas", "mean"),
            tiempo_mediano_horas_solo_con_tiempo=("tiempo_medio_horas", "median"),
        )
    )

    resumen_generos = resumen_generos.merge(resumen_tiempo_registrado, on="genero", how="left")
    resumen_generos["porcentaje_juegos_con_tiempo"] = (
        resumen_generos["juegos_con_tiempo_registrado"] / resumen_generos["cantidad_juegos"] * 100
    )

    # Redondeamos columnas numericas para que los CSV finales sean mas faciles de leer.
    resumen_generos["usuarios_estimados_total"] = resumen_generos["usuarios_estimados_total"].round(0).astype("int64")
    resumen_generos["usuarios_estimados_media"] = resumen_generos["usuarios_estimados_media"].round(0).astype("int64")
    resumen_generos["usuarios_estimados_mediana"] = resumen_generos["usuarios_estimados_mediana"].round(0).astype("int64")
    resumen_generos["usuarios_estimados_media_millones"] = (resumen_generos["usuarios_estimados_media"] / 1_000_000).round(3)
    resumen_generos["usuarios_estimados_mediana_millones"] = (
        resumen_generos["usuarios_estimados_mediana"] / 1_000_000
    ).round(3)
    resumen_generos["tiempo_medio_horas_todos"] = resumen_generos["tiempo_medio_horas_todos"].round(2)
    resumen_generos["tiempo_medio_horas_solo_con_tiempo"] = resumen_generos[
        "tiempo_medio_horas_solo_con_tiempo"
    ].round(2)
    resumen_generos["tiempo_mediano_horas_solo_con_tiempo"] = resumen_generos[
        "tiempo_mediano_horas_solo_con_tiempo"
    ].round(2)
    resumen_generos["porcentaje_juegos_con_tiempo"] = resumen_generos["porcentaje_juegos_con_tiempo"].round(2)
    resumen_generos["proporcion_positivas_media"] = resumen_generos["proporcion_positivas_media"].round(4)

    # Guardamos el resumen completo por genero.
    resumen_generos.to_csv(PROCESSED_DIR / "resumen_generos.csv", index=False)

    # Creamos una version filtrada para evitar conclusiones poco fiables con generos pequenos.
    # Por ejemplo, un genero con 20 juegos puede tener una media muy alta por pocos casos extremos.
    resumen_generos_filtrado = resumen_generos[resumen_generos["cantidad_juegos"] >= 1000].copy()
    resumen_generos_filtrado.to_csv(PROCESSED_DIR / "resumen_generos_min_1000_juegos.csv", index=False)

    # Mostramos en consola los principales resultados del analisis.
    print("\nTop 10 generos por usuarios estimados medios por juego, filtrando generos con al menos 1000 juegos:")
    print(
        resumen_generos_filtrado.sort_values("usuarios_estimados_media", ascending=False)[
            [
                "genero",
                "cantidad_juegos",
                "usuarios_estimados_media",
                "usuarios_estimados_mediana",
                "usuarios_estimados_total",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\nTop 10 generos por tiempo medio de juego, solo juegos con tiempo registrado:")
    print(
        resumen_generos.sort_values("tiempo_medio_horas_solo_con_tiempo", ascending=False)[
            [
                "genero",
                "cantidad_juegos",
                "juegos_con_tiempo_registrado",
                "tiempo_medio_horas_solo_con_tiempo",
                "usuarios_estimados_total",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nTop 10 generos por tiempo medio de juego, solo juegos con tiempo registrado "
        "y filtrando generos con al menos 1000 juegos:"
    )
    print(
        resumen_generos_filtrado.sort_values("tiempo_medio_horas_solo_con_tiempo", ascending=False)[
            [
                "genero",
                "cantidad_juegos",
                "juegos_con_tiempo_registrado",
                "tiempo_medio_horas_solo_con_tiempo",
                "usuarios_estimados_total",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    # Este bloque hace que main() se ejecute solo cuando lanzamos este archivo directamente.
    main()
