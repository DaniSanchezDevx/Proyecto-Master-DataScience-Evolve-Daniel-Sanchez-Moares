# Borrador para Medium o Hashnode

## Lo que aprendí analizando datos de Steam 2025

Este proyecto nace de una pregunta sencilla: **¿qué géneros de Steam tienen más usuarios y más tiempo medio de juego?**

Para responderla trabajé con el dataset **Steam Games dataset 2025**, descargado de Kaggle. El conjunto de datos incluye información sobre juegos, géneros, precios, reseñas, usuarios estimados y tiempo medio de juego.

Durante el proceso limpié y transformé los datos con Python y pandas. Una de las partes más importantes fue convertir variables que no venían directamente listas para analizar. Por ejemplo, `estimated_owners` aparece como un rango, así que usé el punto medio como estimación. También convertí el tiempo medio de minutos a horas para que los resultados fueran más fáciles de entender.

El aprendizaje más importante fue metodológico. Al principio parecía que algunos géneros tenían miles de millones de usuarios, pero eso ocurría porque se estaban sumando usuarios de muchos juegos y un mismo juego puede pertenecer a varios géneros. Para evitar esa lectura inflada, decidí usar **usuarios estimados medios por juego** como métrica principal.

Los resultados muestran que géneros como **Multijugador masivo**, **Gratis**, **Acción**, **RPG** y **Estrategia** destacan por usuarios estimados medios. En cambio, si miramos tiempo medio de juego, aparecen con fuerza **Simulación**, **Multijugador masivo**, **Casual**, **Aventura** y **Acción**.

También comparé juegos gratuitos y juegos de pago. Los juegos gratis tienen más usuarios estimados medios, mientras que los de pago presentan mayor tiempo medio de juego.

Por último, analicé si las valoraciones positivas estaban relacionadas con la popularidad o el tiempo de juego. La conclusión fue que no hay una relación fuerte entre esas variables. Tener buenas valoraciones no implica necesariamente tener muchos usuarios ni muchas horas jugadas.

Este proyecto me ayudó a entender que en análisis de datos no solo importa calcular, sino justificar qué se calcula y por qué.

Proyecto académico desarrollado durante el Master en Data Science de Evolve.

Repositorio: https://github.com/DaniSanchezDevx/Proyecto-Master-DataScience-Evolve-Daniel-Sanchez-Moares
