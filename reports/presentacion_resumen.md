# Presentación resumen: Steam Games 2025

## 1. Título

**Steam Games 2025: análisis de géneros, precio, usuarios y valoraciones**

## 2. Idea del proyecto

El objetivo del proyecto es analizar un dataset de videojuegos de Steam para entender qué factores se relacionan con la popularidad, el tiempo de juego y las valoraciones de los usuarios.

La pregunta inicial fue:

> ¿Qué géneros tienen más usuarios estimados o más tiempo medio de juego?

Después el análisis se amplió con dos preguntas más:

- ¿Existen diferencias entre juegos gratuitos y juegos de pago?
- ¿Existe relación entre valoraciones positivas, usuarios estimados y tiempo de juego?

## 3. Dataset

El dataset utilizado es **Steam Games dataset 2025**, descargado de Kaggle.

El archivo original contiene aproximadamente 95.000 juegos y 47 columnas.

Algunas columnas importantes son:

- `genres`
- `price`
- `estimated_owners`
- `average_playtime_forever`
- `positive`
- `negative`

## 4. Limpieza y transformación

Antes de analizar los datos fue necesario limpiarlos y transformarlos.

Las transformaciones principales fueron:

- Convertir `genres`, que venía como texto, en listas reales de géneros.
- Traducir los géneros principales al castellano.
- Convertir `estimated_owners`, que venía como rango, en un valor aproximado usando el punto medio.
- Convertir el tiempo medio de juego de minutos a horas.
- Crear `total_resenas`, sumando reseñas positivas y negativas.
- Crear `proporcion_positivas`, para medir el porcentaje de valoraciones positivas.
- Crear `es_gratis`, para distinguir juegos gratuitos y juegos de pago.

## 5. Análisis 1: géneros

Para analizar los géneros se usó la media de usuarios estimados por juego.

No se usó el total acumulado como métrica principal porque sumaba todos los juegos de un género y podía generar cifras enormes que no representaban usuarios únicos.

### Resultado: usuarios estimados medios por juego

Entre los géneros con al menos 1000 juegos, los que tienen más usuarios estimados medios por juego son:

1. Multijugador masivo: 486.198
2. Gratis: 233.896
3. Acción: 157.349
4. RPG: 150.048
5. Estrategia: 114.714

### Resultado: tiempo medio de juego

Para el tiempo medio se usaron solo juegos con tiempo registrado mayor que 0, porque muchos juegos tenían tiempo igual a 0.

Los géneros con mayor tiempo medio son:

1. Simulación: 37,47 horas
2. Multijugador masivo: 32,42 horas
3. Casual: 28,32 horas
4. Aventura: 23,99 horas
5. Acción: 18,92 horas

### Interpretación

Los géneros con más usuarios medios por juego no son necesariamente los que tienen más tiempo medio de juego.

Esto indica que popularidad y tiempo de juego son dimensiones diferentes.

## 6. Análisis 2: juegos gratis vs juegos de pago

Se compararon juegos gratuitos y juegos de pago.

| Tipo de juego | Usuarios medios | Tiempo medio | Valoraciones positivas |
|---|---:|---:|---:|
| Gratis | 134.488 | 14,37 horas | 75% |
| Pago | 85.688 | 22,49 horas | 75% |

### Interpretación

Los juegos gratuitos tienen más usuarios estimados medios por juego.

Esto puede tener sentido porque no tienen barrera de entrada económica.

Sin embargo, los juegos de pago tienen mayor tiempo medio de juego entre los juegos con tiempo registrado.

Las valoraciones positivas medias son prácticamente iguales en ambos grupos.

## 7. Análisis 3: valoraciones, usuarios y tiempo

Se analizó si las valoraciones positivas se relacionan con:

- usuarios estimados;
- tiempo medio de juego;
- total de reseñas.

Para evitar conclusiones poco fiables, se filtraron juegos con al menos 50 reseñas.

### Correlaciones principales

| Variables | Correlación |
|---|---:|
| Usuarios estimados vs valoraciones positivas | 0,029 |
| Tiempo medio vs valoraciones positivas | 0,005 |
| Usuarios estimados vs total de reseñas | 0,700 |

### Interpretación

Las valoraciones positivas apenas tienen relación lineal con usuarios estimados o tiempo medio.

En cambio, usuarios estimados y total de reseñas sí están claramente relacionados.

Esto tiene sentido: los juegos con más usuarios suelen acumular más reseñas.

## 8. Limitaciones

El análisis tiene varias limitaciones:

- `estimated_owners` no es una cifra exacta, sino un rango.
- Los usuarios estimados no representan usuarios únicos.
- Un juego puede pertenecer a varios géneros.
- Muchos juegos tienen tiempo medio igual a 0.
- Las valoraciones son poco fiables cuando hay pocas reseñas.
- Correlación no implica causalidad.

## 9. Conclusión final

La conclusión principal es que el éxito de un videojuego no se puede medir con una sola variable.

Un juego o género puede destacar por:

- tener muchos usuarios;
- generar muchas horas de juego;
- recibir buenas valoraciones;
- acumular muchas reseñas.

Pero estas dimensiones no siempre coinciden.

En este dataset, Multijugador masivo destaca por usuarios medios por juego, Simulación destaca por tiempo medio, y las valoraciones positivas no parecen depender directamente ni del número de usuarios ni del tiempo de juego.

## 10. Frase de cierre

> El análisis muestra que popularidad, retención y satisfacción son conceptos relacionados, pero no equivalentes. Por eso es importante estudiar varias métricas antes de concluir que un juego o género tiene más éxito.
