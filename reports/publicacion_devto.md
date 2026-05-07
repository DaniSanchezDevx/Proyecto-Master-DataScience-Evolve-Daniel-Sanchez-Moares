# Borrador para Dev.to

## Análisis de Steam 2025: géneros, usuarios y valoraciones

Steam es una de las plataformas más importantes de distribución de videojuegos para PC. Por eso, analizar sus datos puede ayudar a entender qué tipos de juegos consiguen más usuarios, cuáles retienen mejor a los jugadores y si las valoraciones positivas están relacionadas con la popularidad.

Este proyecto parte del dataset **Steam Games dataset 2025**, descargado de Kaggle. El archivo original contiene cerca de 95.000 juegos y diferentes variables sobre precio, géneros, reseñas, usuarios estimados y tiempo medio de juego. El objetivo principal fue responder a una pregunta sencilla: **¿qué géneros tienen más usuarios estimados por juego y cuáles tienen mayor tiempo medio de juego?**

El primer paso fue limpiar y transformar los datos. Algunas columnas necesitaban tratamiento especial. Por ejemplo, `estimated_owners` no contiene un número exacto de usuarios, sino rangos como `100000 - 200000`. Para poder trabajar con esta variable, se calculó el punto medio del rango. También se convirtió `average_playtime_forever`, que venía en minutos, a horas.

Otra decisión importante fue no usar la suma total de usuarios por género como métrica principal. Un mismo juego puede pertenecer a varios géneros, así que sumar todos los usuarios por género puede inflar mucho los resultados. Para comparar géneros de forma más justa, se usó principalmente la media de usuarios estimados por juego.

Los resultados muestran que, entre los géneros con al menos 1.000 juegos, **Multijugador masivo** es el género con más usuarios estimados medios por juego, con aproximadamente 486.198 usuarios. Le siguen **Gratis**, **Acción**, **RPG** y **Estrategia**. En cambio, si se analiza el tiempo medio de juego, destacan **Simulación**, **Multijugador masivo**, **Casual**, **Aventura** y **Acción**.

También se compararon juegos gratuitos y juegos de pago. Los juegos gratuitos tienen más usuarios estimados medios por juego, pero los juegos de pago presentan mayor tiempo medio de juego. Esto sugiere que los juegos gratis consiguen más alcance inicial, mientras que los de pago pueden retener más tiempo a quienes los compran.

Además de los resultados numéricos, el proyecto me sirvió para practicar una parte muy importante del análisis de datos: explicar las decisiones tomadas. No basta con generar gráficos; también hay que entender qué significa cada variable, qué limitaciones tiene y qué conclusiones se pueden defender. En este caso, fue especialmente importante separar usuarios acumulados de usuarios medios por juego, porque esa diferencia cambia por completo la lectura del proyecto.

Por último, se estudió la relación entre valoraciones positivas, usuarios estimados y tiempo medio de juego. Para evitar resultados poco fiables, se filtraron juegos con al menos 50 reseñas. El análisis mostró que las valoraciones positivas no tienen una relación fuerte con el número de usuarios ni con el tiempo medio de juego. Sin embargo, sí aparece una relación mucho más clara entre número de reseñas y usuarios estimados.

La principal conclusión es que el éxito de un juego no depende de una sola métrica. Popularidad, retención y satisfacción miden aspectos distintos. Un juego puede tener muchos usuarios, pero no necesariamente mucho tiempo de juego; también puede tener buenas valoraciones sin ser masivo.

Este proyecto académico fue desarrollado durante el Master en Data Science de Evolve.

Repositorio de GitHub: `AÑADIR_ENLACE_AL_REPOSITORIO`

Tags sugeridos: `python`, `datascience`, `pandas`, `jupyter`, `steam`
