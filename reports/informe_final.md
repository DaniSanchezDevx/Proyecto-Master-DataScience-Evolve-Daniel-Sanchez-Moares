# Informe final: Steam Games 2025

## 1. Introducción

Este proyecto analiza un dataset de videojuegos de Steam de marzo de 2025. El objetivo principal es explorar qué características se relacionan con la popularidad, el tiempo de juego y la valoración de los videojuegos.

El análisis se ha dividido en tres bloques:

1. Análisis por géneros.
2. Comparación entre juegos gratuitos y juegos de pago.
3. Relación entre valoraciones positivas, usuarios estimados y tiempo medio de juego.

## 2. Objetivos

Las preguntas principales del proyecto son:

- ¿Qué géneros tienen más usuarios estimados medios por juego?
- ¿Qué géneros tienen mayor tiempo medio de juego?
- ¿Existen diferencias entre juegos gratuitos y juegos de pago?
- ¿Existe relación entre las valoraciones positivas, los usuarios estimados y el tiempo medio de juego?

## 3. Dataset

El archivo original utilizado es:

`data/raw/games_march2025_full.csv`

El dataset contiene información sobre juegos de Steam, incluyendo:

- nombre del juego;
- fecha de lanzamiento;
- géneros;
- precio;
- usuarios estimados;
- tiempo medio de juego;
- valoraciones positivas y negativas;
- plataformas disponibles;
- desarrolladores y publicadores.

## 4. Limpieza y transformación de datos

El archivo original contiene columnas que necesitan transformación antes de poder analizarlas correctamente.

Las principales transformaciones realizadas han sido:

- Conversión de `genres` de texto a listas reales de géneros.
- Traducción de géneros principales al castellano.
- Conversión de `estimated_owners` de rango a valor numérico aproximado usando el punto medio.
- Conversión del tiempo medio de juego de minutos a horas.
- Creación de `total_resenas`, sumando reseñas positivas y negativas.
- Creación de `proporcion_positivas`, dividiendo reseñas positivas entre total de reseñas.
- Creación de `es_gratis`, para separar juegos gratuitos y juegos de pago.
- Agrupación por género para obtener métricas resumidas.

Los archivos procesados principales son:

- `data/processed/juegos_steam_limpio_base.csv`
- `data/processed/resumen_generos.csv`
- `data/processed/resumen_generos_min_1000_juegos.csv`

## 5. Análisis por géneros

Notebook relacionado:

`notebooks/01_analisis_generos.ipynb`

### 5.1 Usuarios estimados medios por juego

Para analizar qué géneros tienen más usuarios, se ha utilizado `usuarios_estimados_media`, no `usuarios_estimados_total`.

Esto es importante porque `usuarios_estimados_total` suma todos los juegos de un género y puede generar cifras muy infladas. En cambio, `usuarios_estimados_media` responde mejor a la pregunta:

> ¿Cuántos usuarios estimados tiene de media un juego de este género?

Filtrando géneros con al menos 1000 juegos, los géneros con más usuarios estimados medios por juego son:

| Género | Usuarios estimados medios por juego | Cantidad de juegos |
|---|---:|---:|
| Multijugador masivo | 486.198 | 2.129 |
| Gratis | 233.896 | 8.873 |
| Acción | 157.349 | 36.894 |
| RPG | 150.048 | 16.350 |
| Estrategia | 114.714 | 17.380 |

![Top 10 géneros por usuarios estimados medios por juego](figures/01_usuarios_por_genero.png)

### 5.2 Tiempo medio de juego por género

El dataset contiene muchos juegos con tiempo medio igual a 0. Por eso, para analizar el tiempo de juego se ha usado principalmente la columna:

`tiempo_medio_horas_solo_con_tiempo`

Esta columna calcula la media solo sobre juegos con tiempo registrado mayor que 0.

Los géneros con mayor tiempo medio de juego son:

| Género | Tiempo medio en horas | Juegos con tiempo registrado |
|---|---:|---:|
| Simulación | 37,47 | 1.929 |
| Multijugador masivo | 32,42 | 303 |
| Casual | 28,32 | 2.498 |
| Aventura | 23,99 | 3.381 |
| Acción | 18,92 | 3.647 |

![Top 10 géneros por tiempo medio de juego](figures/02_tiempo_por_genero.png)

### 5.3 Interpretación

Los géneros con más usuarios medios por juego no son necesariamente los géneros con mayor tiempo medio.

Multijugador masivo destaca por usuarios medios por juego, mientras que Simulación destaca por tiempo medio acumulado. Esto sugiere que popularidad y tiempo de juego no miden exactamente lo mismo.

## 6. Juegos gratuitos vs juegos de pago

Notebook relacionado:

`notebooks/02_gratis_vs_pago.ipynb`

En este bloque se comparan juegos gratuitos y juegos de pago en usuarios estimados, tiempo de juego y valoraciones.

| Tipo de juego | Cantidad de juegos | Usuarios estimados medios | Tiempo medio en horas | Valoraciones positivas medias | Precio medio |
|---|---:|---:|---:|---:|---:|
| Gratis | 19.420 | 134.488 | 14,37 | 75% | 0,00 |
| Pago | 75.528 | 85.688 | 22,49 | 75% | 8,69 |

![Usuarios estimados medios: gratis vs pago](figures/03_gratis_vs_pago_usuarios.png)

![Tiempo medio: gratis vs pago](figures/04_gratis_vs_pago_tiempo.png)

### Interpretación

Los juegos gratuitos tienen más usuarios estimados de media por juego. Esto puede explicarse porque no tienen barrera de entrada económica.

Sin embargo, los juegos de pago presentan mayor tiempo medio de juego entre los juegos con tiempo registrado. Esto puede indicar que los usuarios que pagan por un juego tienden a dedicarle más tiempo, aunque sería necesario un análisis más profundo para confirmarlo.

Las valoraciones positivas medias son muy similares entre ambos grupos.

## 7. Valoraciones, usuarios y tiempo de juego

Notebook relacionado:

`notebooks/03_valoraciones_popularidad.ipynb`

En este bloque se analiza si existe relación entre:

- usuarios estimados;
- tiempo medio de juego;
- proporción de valoraciones positivas;
- total de reseñas.

Para evitar resultados poco fiables, se filtran juegos con al menos 50 reseñas.

### 7.1 Correlaciones principales

| Variables | Correlación |
|---|---:|
| Usuarios estimados vs valoraciones positivas | 0,029 |
| Tiempo medio vs valoraciones positivas | 0,005 |
| Usuarios estimados vs total de reseñas | 0,700 |

![Usuarios estimados medios según valoración del juego](figures/05_valoraciones_vs_usuarios.png)

![Tiempo medio de juego según valoración del juego](figures/06_valoraciones_vs_tiempo.png)

### Interpretación

Las valoraciones positivas apenas tienen relación lineal con los usuarios estimados o el tiempo medio de juego.

En cambio, usuarios estimados y total de reseñas sí tienen una relación clara. Esto es esperable: los juegos con más usuarios tienden a acumular más reseñas.

Para que la relación sea más fácil de interpretar, los gráficos dividen los juegos en tres grupos: valoración baja, media y alta. Después comparan cuántos usuarios estimados y cuántas horas medias tiene cada grupo.

Una conclusión importante es que popularidad, tiempo de juego y satisfacción son dimensiones distintas. Un juego puede tener muchos usuarios sin tener necesariamente mejores valoraciones.

## 8. Limitaciones del análisis

Este proyecto tiene varias limitaciones importantes:

- `estimated_owners` no es una cifra exacta, sino un rango.
- Se usa el punto medio del rango como aproximación.
- `usuarios_estimados_total` no representa usuarios únicos.
- Un mismo usuario puede jugar a varios juegos.
- Un mismo juego puede pertenecer a varios géneros.
- Muchos juegos tienen tiempo medio igual a 0.
- Las valoraciones pueden ser poco fiables en juegos con pocas reseñas.
- Correlación no implica causalidad.

Estas limitaciones no invalidan el análisis, pero deben tenerse en cuenta al interpretar los resultados.

## 9. Conclusiones generales

Las principales conclusiones del proyecto son:

- Multijugador masivo es el género con más usuarios estimados medios por juego entre los géneros con al menos 1000 juegos.
- Simulación es el género con mayor tiempo medio de juego entre los géneros principales.
- Los juegos gratuitos tienen más usuarios estimados medios que los juegos de pago.
- Los juegos de pago tienen mayor tiempo medio de juego entre los juegos con tiempo registrado.
- Las valoraciones positivas no muestran una relación fuerte con usuarios estimados ni con tiempo medio.
- Los usuarios estimados y el total de reseñas sí están claramente relacionados.

En conjunto, el análisis muestra que no existe una única forma de medir el éxito de un videojuego. Un género o juego puede destacar por usuarios, por tiempo de juego o por valoraciones, y estas dimensiones no siempre coinciden.

## 10. Próximos pasos

Posibles ampliaciones del proyecto:

- Analizar la evolución por año de lanzamiento.
- Comparar géneros dentro de juegos gratuitos y de pago.
- Crear un modelo predictivo sencillo para estimar si un juego tendrá alta valoración.
- Analizar etiquetas (`tags`) además de géneros.
- Estudiar diferencias entre plataformas: Windows, Mac y Linux.
