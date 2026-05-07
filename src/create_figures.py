from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


def formato_miles(valor: float, _posicion: int) -> str:
    """Muestra numeros grandes con punto de miles."""
    return f"{valor:,.0f}".replace(",", ".")


def guardar_figura(nombre: str) -> None:
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / nombre, dpi=160, bbox_inches="tight")
    plt.close()


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    resumen_generos = pd.read_csv(PROCESSED_DIR / "resumen_generos_min_1000_juegos.csv")
    juegos = pd.read_csv(PROCESSED_DIR / "juegos_steam_limpio_base.csv")

    top_usuarios = resumen_generos.sort_values("usuarios_estimados_media", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_usuarios["genero"][::-1], top_usuarios["usuarios_estimados_media"][::-1])
    ax.set_title("Top 10 géneros por usuarios estimados medios por juego")
    ax.set_xlabel("Usuarios estimados medios por juego")
    ax.set_ylabel("Género")
    ax.xaxis.set_major_formatter(FuncFormatter(formato_miles))
    guardar_figura("01_usuarios_por_genero.png")

    top_tiempo = resumen_generos.sort_values("tiempo_medio_horas_solo_con_tiempo", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_tiempo["genero"][::-1], top_tiempo["tiempo_medio_horas_solo_con_tiempo"][::-1])
    ax.set_title("Top 10 géneros por tiempo medio de juego")
    ax.set_xlabel("Tiempo medio acumulado por juego (horas)")
    ax.set_ylabel("Género")
    guardar_figura("02_tiempo_por_genero.png")

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

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(resumen_tipo["tipo_juego"], resumen_tipo["usuarios_estimados_media"])
    ax.set_title("Usuarios estimados medios por juego")
    ax.set_xlabel("Tipo de juego")
    ax.set_ylabel("Usuarios estimados medios")
    ax.yaxis.set_major_formatter(FuncFormatter(formato_miles))
    guardar_figura("03_gratis_vs_pago_usuarios.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(resumen_tipo["tipo_juego"], resumen_tipo["tiempo_medio_horas_solo_con_tiempo"])
    ax.set_title("Tiempo medio acumulado por juego")
    ax.set_xlabel("Tipo de juego")
    ax.set_ylabel("Horas medias, solo juegos con tiempo registrado")
    guardar_figura("04_gratis_vs_pago_tiempo.png")

    juegos_con_resenas = juegos[juegos["total_resenas"] >= 50].copy()
    juegos_con_resenas["grupo_valoracion"] = pd.cut(
        juegos_con_resenas["proporcion_positivas"] * 100,
        bins=[-1, 60, 80, 100],
        labels=["Baja (<60%)", "Media (60-80%)", "Alta (>80%)"],
    )
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
    for index, row in resumen_valoracion.iterrows():
        ax.text(
            index,
            row["usuarios_estimados_media"] * 1.02,
            f"{int(row['cantidad_juegos'])} juegos",
            ha="center",
            fontsize=8,
        )
    guardar_figura("05_valoraciones_vs_usuarios.png")

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
    for index, row in resumen_tiempo_valoracion.iterrows():
        ax.text(
            index,
            row["tiempo_medio_horas"] * 1.02,
            f"{int(row['cantidad_juegos'])} juegos",
            ha="center",
            fontsize=8,
        )
    guardar_figura("06_valoraciones_vs_tiempo.png")

    print(f"Figuras guardadas en: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
