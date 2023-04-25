# Practica 1: ¿Cómo podemos capturar los datos de la web? 
# Autores
- Juan Luis Andión Tápiz | mail: [jandion@uoc.edu](jandion@uoc.edu)
- Raúl García Díaz | mail: [raulgd@uoc.edu](raulgd@uoc.edu)

## Description
Asignatura: M2.851 / Fecha 25-04-2023

Este módulo realiza un raspado de información referente a las obras que estan reflejadas en IMDb 
con un género determinado.

URL del sitio elegido: https://www.imdb.com

## Descripción del repositorio
- `memoria.pdf`: Documento con una descripccion mas detallada del proyecto.
- `/src/main.py`: Archivo que ejecuta todo el proyecto.
- `/src/imdbClassDataSet.py`: Archivo que se encarga de generear el dataset.
- `/src/load_proxy.py`: Módulo que contiene las herramientas necesarias para cargar los proxys.
- `/src/requirements.txt`: Lista de paquetes utilizados (python 3.10).
- `dataset/IMDb_data.csv`: Dataset extraído con los parámetros `type_=movie` y `genre=comedy`.

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
1. `cd ./ PRA1-Tipologia-y-ciclo-de-vida-de-los-datos/src`
2. `pip install -r requirements.txt`
3. `python3 -m main type_='movie', genre='comedy'`

Este ejemplo es para extraer las 10000 primeras películas de comedia que aparecen en IMDb.

## Publicación en Zenodo
El dataset ha sido publicado en Zenodo con DOI [10.5281/zenodo.7860478](https://doi.org/10.5281/zenodo.7860478).



[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7860478.svg)](https://doi.org/10.5281/zenodo.7860478)
