"""Genera las figuras finales del informe.

Este script usa los CSV ya procesados por `src/analyze_genres.py`.
No modifica los datos: solo lee tablas limpias y guarda gráficos en `reports/figures/`.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


# Rutas principales del proyecto.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


def formato_miles(valor: float, _posicion: int) -> str:
    """Muestra números grandes con punto de miles: 1000000 -> 1.000.000."""
    return f"{valor:,.0f}".replace(",", ".")


def guardar_figura(nombre: str) -> None:
    """Ajusta, guarda y cierra la figura activa."""
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / nombre, dpi=160, bbox_inches="tight")
    plt.close()


def anadir_etiquetas_juegos(ax: plt.Axes, datos: pd.DataFrame, columna_valor: str) -> None:
    """Añade encima de cada barra cuántos juegos hay en ese grupo."""
    for index, row in datos.iterrows():
        ax.text(
            index,
            row[columna_valor] * 1.02,
            f"{int(row['cantidad_juegos'])} juegos",
            ha="center",
            fontsize=8,
        )


def main() -> None:
    """Crea todas las figuras usadas por el informe final."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Leemos los datos ya limpios. El script no toca el CSV original de Kaggle.
    resumen_generos = pd.read_csv(PROCESSED_DIR / "resumen_generos_min_1000_juegos.csv")
    juegos = pd.read_csv(PROCESSED_DIR / "juegos_steam_limpio_base.csv")

    # Figura 1: géneros con más usuarios estimados medios por juego.
    top_usuarios = resumen_generos.sort_values("usuarios_estimados_media", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_usuarios["genero"][::-1], top_usuarios["usuarios_estimados_media"][::-1])
    ax.set_title("Top 10 géneros por usuarios estimados medios por juego")
    ax.set_xlabel("Usuarios estimados medios por juego")
    ax.set_ylabel("Género")
    ax.xaxis.set_major_formatter(FuncFormatter(formato_miles))
    guardar_figura("01_usuarios_por_genero.png")

    # Figura 2: géneros con mayor tiempo medio, usando solo juegos con tiempo registrado.
    top_tiempo = resumen_generos.sort_values("tiempo_medio_horas_solo_con_tiempo", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_tiempo["genero"][::-1], top_tiempo["tiempo_medio_horas_solo_con_tiempo"][::-1])
    ax.set_title("Top 10 géneros por tiempo medio de juego")
    ax.set_xlabel("Tiempo medio acumulado por juego (horas)")
    ax.set_ylabel("Género")
    guardar_figura("02_tiempo_por_genero.png")

    # Preparamos una variable sencilla para comparar juegos gratis y de pago.
    juegos["tipo_juego"] = juegos["es_gratis"].map({True: "Gratis", False: "Pago"})
    juegos["tiempo_horas_solo_si_registrado"] = juegos["tiempo_medio_horas"].where(
        juegos["tiempo_medio_horas"] > 0
    )
    resumen_tipo = (
        juegos.groupby("tipo_juego", as_index=False)
        .agg(
            usuarios_estimados_media=("usuarios_estimados_aprox", "mean"),
            tiempo_medio_horas_solo_con_tiempo=("tiempo_horas_solo_si_registrado", "mean"),
            proporcion_positivas_media=("proporcion_positivas", "mean"),
        )
        .sort_values("tipo_juego")
    )

    # Figura 3: comparación de usuarios medios entre juegos gratis y de pago.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(resumen_tipo["tipo_juego"], resumen_tipo["usuarios_estimados_media"])
    ax.set_title("Usuarios estimados medios por juego")
    ax.set_xlabel("Tipo de juego")
    ax.set_ylabel("Usuarios estimados medios")
    ax.yaxis.set_major_formatter(FuncFormatter(formato_miles))
    guardar_figura("03_gratis_vs_pago_usuarios.png")

    # Figura 4: comparación de tiempo medio entre juegos gratis y de pago.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(resumen_tipo["tipo_juego"], resumen_tipo["tiempo_medio_horas_solo_con_tiempo"])
    ax.set_title("Tiempo medio acumulado por juego")
    ax.set_xlabel("Tipo de juego")
    ax.set_ylabel("Horas medias, solo juegos con tiempo registrado")
    guardar_figura("04_gratis_vs_pago_tiempo.png")

    # Para valoraciones filtramos juegos con al menos 50 reseñas.
    # Así evitamos que juegos con 1 o 2 reseñas distorsionen el porcentaje positivo.
    juegos_con_resenas = juegos[juegos["total_resenas"] >= 50].copy()
    juegos_con_resenas["grupo_valoracion"] = pd.cut(
        juegos_con_resenas["proporcion_positivas"] * 100,
        bins=[-1, 60, 80, 100],
        labels=["Baja (<60%)", "Media (60-80%)", "Alta (>80%)"],
    )

    # Figura 5: usuarios estimados medios según grupo de valoración.
    resumen_valoracion = (
        juegos_con_resenas.groupby("grupo_valoracion", observed=False)
        .agg(
            usuarios_estimados_media=("usuarios_estimados_aprox", "mean"),
            cantidad_juegos=("id_app", "count"),
        )
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        resumen_valoracion["grupo_valoracion"].astype(str),
        resumen_valoracion["usuarios_estimados_media"],
    )
    ax.set_title("Usuarios estimados medios según valoración del juego")
    ax.set_xlabel("Grupo de valoración positiva")
    ax.set_ylabel("Usuarios estimados medios por juego")
    ax.yaxis.set_major_formatter(FuncFormatter(formato_miles))
    anadir_etiquetas_juegos(ax, resumen_valoracion, "usuarios_estimados_media")
    guardar_figura("05_valoraciones_vs_usuarios.png")

    # Figura 6: tiempo medio según grupo de valoración.
    juegos_con_tiempo = juegos_con_resenas[juegos_con_resenas["tiempo_medio_horas"] > 0].copy()
    resumen_tiempo_valoracion = (
        juegos_con_tiempo.groupby("grupo_valoracion", observed=False)
        .agg(
            tiempo_medio_horas=("tiempo_medio_horas", "mean"),
            cantidad_juegos=("id_app", "count"),
        )
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        resumen_tiempo_valoracion["grupo_valoracion"].astype(str),
        resumen_tiempo_valoracion["tiempo_medio_horas"],
    )
    ax.set_title("Tiempo medio de juego según valoración del juego")
    ax.set_xlabel("Grupo de valoración positiva")
    ax.set_ylabel("Tiempo medio acumulado (horas)")
    anadir_etiquetas_juegos(ax, resumen_tiempo_valoracion, "tiempo_medio_horas")
    guardar_figura("06_valoraciones_vs_tiempo.png")

    print(f"Figuras guardadas en: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
