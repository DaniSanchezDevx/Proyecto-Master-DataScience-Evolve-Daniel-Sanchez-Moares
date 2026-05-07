# Steam Games 2025

Proyecto de análisis de datos sobre videojuegos publicados en Steam.

El objetivo es estudiar qué géneros tienen más usuarios estimados por juego, cuáles presentan mayor tiempo medio de juego y si las valoraciones positivas están relacionadas con la popularidad.

Proyecto académico desarrollado durante el Master en Data Science de Evolve.

## Objetivos

La pregunta inicial del proyecto fue:

> ¿Qué géneros tienen más usuarios estimados por juego y cuáles tienen mayor tiempo medio de juego?

Después, el análisis se amplió con dos preguntas más:

- ¿Existen diferencias entre juegos gratuitos y juegos de pago?
- ¿Existe relación entre valoraciones positivas, usuarios estimados y tiempo medio de juego?

## Tecnologías utilizadas

- Python
- pandas
- matplotlib
- Jupyter Notebook
- PowerShell
- HTML y Markdown para el informe final

## Dataset

Dataset utilizado: **Steam Games dataset 2025**, descargado de Kaggle.

Archivo original esperado:

```text
data/raw/games_march2025_full.csv
```

El dataset contiene aproximadamente 95.000 juegos y 47 columnas.

El archivo original no se incluye en el repositorio porque es demasiado pesado para GitHub. Para reproducir el proyecto, hay que descargarlo desde Kaggle y colocarlo en `data/raw/` con el nombre indicado.

## Estructura del proyecto

```text
Steam_Games_2025/
|-- data/
|   |-- raw/
|   |   |-- README.md
|   |   `-- games_march2025_full.csv
|   `-- processed/
|       |-- juegos_steam_limpio_base.csv
|       |-- resumen_generos.csv
|       `-- resumen_generos_min_1000_juegos.csv
|-- notebooks/
|   |-- 01_analisis_generos.ipynb
|   |-- 02_gratis_vs_pago.ipynb
|   |-- 03_valoraciones_popularidad.ipynb
|   `-- *_ejecutado.ipynb
|-- reports/
|   |-- informe_final.md
|   |-- informe_final.html
|   |-- presentacion_resumen.md
|   |-- publicacion_devto.md
|   |-- linkedin_article.md
|   |-- linkedin_post.md
|   |-- checklist_publicacion_evolve.md
|   |-- entrega/
|   `-- figures/
|-- scripts/
|   `-- run_all.ps1
|-- src/
|   |-- analyze_genres.py
|   `-- create_figures.py
|-- requirements.txt
`-- README.md
```

## Instalación

Desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Cómo reproducir el análisis

Ejecutar todo el proyecto:

```powershell
.\scripts\run_all.ps1
```

Este comando:

- ejecuta el script de limpieza;
- genera las figuras del informe;
- ejecuta los tres notebooks;
- genera copias ejecutadas de los notebooks.

## Notebooks

- `notebooks/01_analisis_generos.ipynb`: análisis por géneros.
- `notebooks/02_gratis_vs_pago.ipynb`: comparación entre juegos gratuitos y juegos de pago.
- `notebooks/03_valoraciones_popularidad.ipynb`: relación entre valoraciones, usuarios y tiempo medio.

Las versiones terminadas aparecen como `*_ejecutado.ipynb`.

## Informes y entregables

- `reports/informe_final.md`
- `reports/informe_final.html`
- `reports/presentacion_resumen.md`
- `reports/entrega/Analisis_Steam_2025_Generos_Usuarios_Valoraciones.pdf`

También se incluyen borradores para la publicación del proyecto:

- `reports/publicacion_devto.md`
- `reports/medium_hashnode.md`
- `reports/linkedin_article.md`
- `reports/linkedin_post.md`
- `reports/checklist_publicacion_evolve.md`

## Resultados principales

### Géneros con más usuarios estimados medios por juego

| Género | Usuarios estimados medios por juego |
|---|---:|
| Multijugador masivo | 486.198 |
| Gratis | 233.896 |
| Acción | 157.349 |
| RPG | 150.048 |
| Estrategia | 114.714 |

### Géneros con mayor tiempo medio de juego

| Género | Tiempo medio |
|---|---:|
| Simulación | 37,47 horas |
| Multijugador masivo | 32,42 horas |
| Casual | 28,32 horas |
| Aventura | 23,99 horas |
| Acción | 18,92 horas |

### Juegos gratis vs juegos de pago

| Tipo de juego | Usuarios medios | Tiempo medio | Valoraciones positivas |
|---|---:|---:|---:|
| Gratis | 134.488 | 14,37 horas | 75% |
| Pago | 85.688 | 22,49 horas | 75% |

## Conclusiones

Los géneros con más usuarios estimados por juego no son siempre los mismos que presentan mayor tiempo medio de juego. Esto indica que popularidad y retención no miden exactamente lo mismo.

Los juegos gratuitos tienen más usuarios estimados medios, pero los juegos de pago presentan mayor tiempo medio de juego. Una posible interpretación es que los juegos gratis reducen la barrera de entrada, mientras que los juegos de pago pueden implicar mayor compromiso por parte del jugador.

Las valoraciones positivas no muestran una relación fuerte con los usuarios estimados ni con el tiempo medio de juego. En cambio, el número de reseñas sí está más relacionado con la popularidad estimada.

## Notas metodológicas

`estimated_owners` no es un número exacto, sino un rango. Para analizarlo se usa el punto medio del rango como aproximación.

`usuarios_estimados_total` no representa usuarios únicos. Es una suma acumulada de juegos y puede inflar mucho los resultados. Por eso, para comparar géneros se usa principalmente `usuarios_estimados_media`.

Un mismo juego puede pertenecer a varios géneros. Al agrupar por género, un juego puede contar en más de una categoría.

`average_playtime_forever` está en minutos en el dataset original. En el análisis se convierte a horas.

Muchos juegos tienen tiempo medio igual a 0. Por eso se analiza también el tiempo medio solo entre juegos con tiempo registrado mayor que 0.

Para las valoraciones se filtran juegos con al menos 50 reseñas, porque con muy pocas reseñas el porcentaje positivo puede ser poco representativo.

Correlación no implica causalidad.

## Publicación

La guía de publicación de Evolve pide presentar el proyecto en varias plataformas. Este repositorio ya incluye borradores para:

- README de GitHub.
- Artículo técnico en Dev.to.
- Artículo adaptado para Medium o Hashnode.
- Artículo adaptado para LinkedIn.
- Post breve para LinkedIn.
- Checklist final de publicación.

Nombre recomendado para el repositorio:

```text
Proyecto-Master-DataScience-Evolve-TuNombre
```
