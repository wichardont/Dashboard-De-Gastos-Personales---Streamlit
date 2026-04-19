# Dashboard de Gastos Personales

Aplicación web desarrollada con Streamlit para gestionar y visualizar gastos personales.

## Funcionalidades

- Registro de gastos
- Visualización de métricas
- Gráficos interactivos
- Persistencia en CSV

## Tecnologías

- Python
- Streamlit
- Pandas
- Plotly

## Cómo ejecutar

pip install -r requirements.txt  
streamlit run app.py

# v1.2 (BUG FIX)

Bugs arreglados:

 - La gráfica de barras mostraba la hora del registro a pesar de que el usuario no la añadía
 - La gráfica de pie, en ocasiones, no mostraba correctamente la división de todas las categorías

Extras:

 - Se mejoró la organización del código separandolo en varios archivos, cada uno con una función específica
 - Se separó la visualización del dataframe en una pestaña propia
 - Si alguien lee esto, como dato curioso, me apareció un error mientras hacia esta versión en la parte de las graficas, estuve media hora buscando cómo solucionarlo, lo logré pero a medias, me fui a comer, regresé y se había arreglado solo (lol)

# v1.3 (FEATURES UPDATE)
 - Se añadio una opción para filtrar los datos de los gráficos tanto por fecha como por categoría

# v1.3.2 (MINOR UPDATE)
 - Se movieron los filtros a la pestaña de los gráficos