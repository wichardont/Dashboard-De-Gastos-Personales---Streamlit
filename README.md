# Dashboard de Gastos Personales

Aplicación web desarrollada con Streamlit para gestionar y visualizar gastos personales.

## Funcionalidades

- Registro de gastos
- Visualización de métricas
- Gráficos interactivos
- Persistencia en CSV (En las primeras versiones)
- Online a partir de la versión v3.0

## Tecnologías

- Python
- Streamlit
- Pandas
- Plotly
- Docker

## Cómo ejecutar localmente

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

# v2.0 (UX UPDATE)
 - Se añadió un sistema de autenticación (Login y Registro)
 - Se modificó el flujo para que se mostraran solo los datos del usuario que hizo login con su respectiva cuenta
 - Se cambió la base de datos csv por una .db con SQLite
 - Se añadió un sistema para modificar y/o eliminar registros de la base de datos

# v3.0 (DOCKERIZED APP)
 - Se dockerizó la aplicación para después añadirla a un entorno de producción
 - Se hicieron algunos cambios en db.py, ui.py y app.py para poder cambiar la base de datos
 a una online

# v4.0 (UX UPDATE / BUG FIX)
 - Se cambió la forma de navegar entre las secciones de la aplicación (ahora se usan botones)
 - Se añadió funcionalidad para ingresar una categoría personalizada
 - Se corrigió un bug que hacia que el gasto se registrara doble
 - Se corrigió un bug en el que al dar clic muchas veces seguidas en el botón de editar, salia
 un error de streamlit en la pantalla
 - Se mejoró lo más posible la velocidad de carga de la app

# v5.0 (POO)
 - Se modificó prácticamente todo el backend, la estructura de las carpetas y archivos
 para mejorar la organización del código
 - Se cambió el proyecto a un paradigma orientado a objetos para poder hacerlo más escalable

# Puede visitar la aplición en https://dashboard-de-gastos-personales-streamlit.onrender.com/