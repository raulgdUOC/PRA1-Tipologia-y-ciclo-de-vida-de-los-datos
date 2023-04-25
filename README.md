# Practica 1: ¿Cómo podemos capturar los datos de la web? 
## Description

Este módulo realiza un raspado de información referente a las obras que estan reflejadas en IMDb 
con un género determinado.

## Estructura del dataset

La información que se obtiene una vez ejecutado el programa de la forma indicada es la siguiente:

| NameContent | ReleseYear | Certificate | TimeContent | AllGenres | RatingImdb | RatingMetacritic | Casting | Directors | Writers |
|-------------|------------|-------------|-------------|-----------|------------|------------------|---------|-----------|---------|
| ...         | ...        | ...         | ...         | ...       | ...        | ...              | ...     | ...       | ...     |

Donde:
- NameContent: Nombre de la obra.
- ReleseYear: Año de lanzamiento.
- Certificate: A que publico está dirigido.
- TimeContent: Duración de la obra.
- AllGenres: Todos los géneros de la obra.
- RatingImdb: Puntuación en IMDb.
- RatingMetacritic: Punctuation en Metracritic.
- Casting: Reparto de la obra.
- Directors: Directores de la obra.
- Writers: Escritores de la obra.

## Uso del programa
1. `cd ./ PRA1-Tipologia-y-ciclo-de-vida-de-los-datos`
2. `pip install -r requirements.txt`
3. `python3 -m main type_='movie', genre='comedy'`

Este ejemplo es para extraer las 10000 primeras películas de comedia que aparecen en IMDb.

## Publicación en Zenodo
El dataset ha sido publicado en Zenodo con DOI [10.5281/zenodo.7860478](https://doi.org/10.5281/zenodo.7860478).



[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7860478.svg)](https://doi.org/10.5281/zenodo.7860478)

