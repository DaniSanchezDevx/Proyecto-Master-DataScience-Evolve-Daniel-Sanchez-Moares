# Borrador de artículo para LinkedIn

## Análisis de Steam 2025: qué géneros tienen más usuarios y más tiempo de juego

En este proyecto he analizado un dataset de juegos de Steam con el objetivo de estudiar la popularidad, la retención y la satisfacción de los usuarios.

La pregunta inicial era: **¿qué géneros tienen más usuarios estimados por juego y cuáles tienen mayor tiempo medio de juego?** A partir de ahí, el análisis se amplió para comparar juegos gratuitos y de pago, y para estudiar si las valoraciones positivas tienen relación con el número de usuarios o el tiempo medio de juego.

El dataset utilizado fue Steam Games dataset 2025, descargado de Kaggle. Contiene información sobre géneros, precios, reseñas, usuarios estimados y tiempo medio de juego. Durante la limpieza de datos fue necesario transformar variables como `estimated_owners`, que aparece como rango, y `average_playtime_forever`, que viene expresada en minutos.

Una decisión metodológica importante fue usar usuarios estimados medios por juego, no usuarios acumulados por género. Esto es clave porque un mismo juego puede aparecer en varios géneros, y sumar todos los usuarios por género puede dar cifras infladas.

Entre los géneros con al menos 1.000 juegos, los que presentan más usuarios estimados medios por juego son Multijugador masivo, Gratis, Acción, RPG y Estrategia. En cambio, los géneros con mayor tiempo medio de juego son Simulación, Multijugador masivo, Casual, Aventura y Acción.

También observé una diferencia interesante entre juegos gratuitos y juegos de pago: los gratuitos tienen más usuarios estimados medios, mientras que los de pago muestran mayor tiempo medio de juego.

Por último, al analizar valoraciones positivas, usuarios estimados y tiempo medio, no aparece una relación fuerte entre tener mejores valoraciones y tener más usuarios o más tiempo de juego. Esto refuerza una idea importante: el éxito de un videojuego no se puede medir con una única métrica.

Este proyecto académico fue desarrollado durante el Master en Data Science de Evolve.

Repositorio: `AÑADIR_ENLACE_REPOSITORIO`
