<img src ="scr\steam_portada_2.png">
<p align='center'>
<p>


<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>


## Descripción del Proyecto 

Descripción del Proyecto:
El objetivo de este proyecto es emular las funciones de un MLOps Engineer, quien actúa como un híbrido entre Data Engineer y Data Scientist, para la empresa de juegos Steam. El reto empresarial consiste en crear un Producto Mínimo Viable (MVP) que incorporará una API y un modelo de Machine Learning para realizar un análisis de sentimientos basado en los comentarios de los usuarios. Además, ofrecerá un sistema de recomendación de videojuegos para mejorar la experiencia en la plataforma.


<p align='center'><img src ="scr\ia.jpeg">

## Rol: MLOps Engineer

### Contexto

En el rol de un MLOps Engineer en Steam, enfrentamos el desafío de desarrollar un sistema de recomendación de videojuegos desde cero, superando las limitaciones de madurez de los datos disponibles.

## **Datos**

Los conjuntos de datos son los siguientes:

1. **steam_games.json**
   - Ruta: [`datsets/steam_games.json.gz`](datsets/steam_games.json.gz)

2. **user_reviews.json**
   - Ruta: [`datsets/user_reviews.json.gz`](datsets/user_reviews.json.gz)

3. **users_items.json**
   - Ruta: [`datsets/users_items.json.gz`](datsets/users_items.json.gz)

La información detallada sobre el contenido de cada conjunto se encuentra especificada en el diccionario de datos, disponible en el archivo Excel: datsets/Diccionario de Datos STEAM.xlsx

## Objetivo

Desarrollar un sistema de recomendación de juegos utilizando los conjuntos de datos proporcionados. Abordaremos todas las fases clave de Data Engineering desde la preparación de datos (ETL) hasta el análisis exploratorio y la implementación del modelo.


### **1. ETL (Extracción, Transformación y Carga)** <br />

Para el análisis de los archivos creamos el notebook **'1_Transformaciones.ipynb'** el cual tiene el proceso ETL, realizado a los 3 dataframes.

Esta fase inicial se enfoca en la extracción y transformación de los archivos comprimidos **.json.gz'** proporcionados, convirtiéndolos en archivos CSV. Durante este proceso, se realiza la desanidación de las columnas, conservando únicamente aquellas esenciales para el sistema de recomendación y los endpoints propuestos. Además, se implementa el manejo de valores nulos y duplicados, preparándolos para futuros procesos de tratamiento.

El proceso detallado de ETL se puede verificarar en el siguiente notebook: [Proceso de ETL(Extracción, Transformación y Carga)](Notebooks/1_Transformaciones.ipynb).

### **2. Feature Engineering** 

Para este proceso de análisis de sentimiento creamos el notebook **2_Feature_Engineering.ipynb** el cual tiene el proceso Feature Engineering.

Se ha creado la columna 'sentiment_analysis' aplicando análisis de sentimiento a las reseñas de los usuarios mediante la librería NLTK. La asignación de valores es la siguiente: '0' si es una reseña negativa, '1' si es neutral y '2' si es positiva. Esta nueva columna se ha introducido para reemplazar la columna original 'user_reviews.review', facilitando así el trabajo de los modelos de machine learning y el análisis de datos.

Para obtener más detalles sobre este proceso se puede consultar la sección correspondiente en el [Notebook de análisis de sentimiento](Notebooks/2_Feature_Engineering.ipynb)

<p align='center'><img src ="scr\ia_sent.png">

### **3. Tratamiento de Datos y Preparación**

- El proceso de EDA y tratamiento de datos involucró varias etapas clave:

- Filtrado de Datos: Se seleccionaron registros con **playtime_forever** mayor a **0** para asegurar que solo se incluyeran juegos que los usuarios realmente jugaron. Esto refina el conjunto de datos para centrarse en interacciones significativas.

- Análisis de Sentimientos: Se añadió la columna **Sentiment_analysis** basada en reseñas de usuarios, clasificando el sentimiento como positivo (2), neutral (1), o negativo (0), lo que proporciona una dimensión adicional para entender la percepción de los usuarios sobre los juegos.

- Normalización de Fechas: Se transformaron las fechas de publicación (**posted**) a un formato de fecha estandarizado, permitiendo un manejo más fácil de las temporalidades en el análisis.

- Genres: Se conservó la diversidad de géneros listados para cada juego en lugar de reducirlos a un género principal. Esto permite una visión más completa y detallada de las preferencias de género de los usuarios y facilita recomendaciones más precisas al considerar la amplia gama de intereses de los jugadores.

- Ajuste de Precios: Los precios se normalizaron a valores numéricos, incluyendo la conversión de términos como "Free to Play"(entre otras palabras que aludan a contenido gratuito) a **0.00**, lo que asegura una comparación justa y simplifica el análisis de precios.

- Selección Cuidadosa de Columnas: Aunque se priorizó la conservación de información relevante como genres, algunas columnas que no aportaban valor al objetivo del proyecto fueron eliminadas para optimizar el rendimiento de la API y el entrenamiento del modelo.

- Estos pasos de limpieza y transformación garantizan que el conjunto de datos final sea integral y adecuadamente estructurado para soportar el desarrollo de un sistema de recomendación efectivo y eficiente.

Para obtener más detalles sobre este proceso se puede consultar la sección correspondiente en el [Notebook EDA, Tratamiento de Datos y Preparación](3_EDA.ipynb)

### **4. Preparación de Datos para el Modelo de Recomendación Ítem-Ítem**

Para el desarrollo del modelo de recomendación ítem-ítem, se ha realizado una optimización significativa del conjunto de datos inicial, resultando en un dataset más compacto y enfocado. Esta optimización tiene como objetivo facilitar el entrenamiento del modelo y mejorar la calidad de las recomendaciones generadas.

**Datos Utilizados**

El dataset utilizado ha sido **data_fusionada**, generado en el proceso **EDA**, para este proceso se seleccionó columnas clave:

- `item_id`: Identificador único del juego.
- `app_name`: Nombre del juego.
- `recommend`: Número de recomendaciones positivas que el juego ha recibido.
- `playtime_forever`: Tiempo total de juego acumulado por todos los usuarios, en minutos.
- `genres`: Número total de géneros asociados al juego.

#### Proceso de Optimización

El proceso para optimizar el dataset implicó las siguientes etapas:

1. **Consolidación de Datos**: Se agruparon los datos por `item_id`, sumando las recomendaciones y el tiempo de juego acumulado, y contabilizando el número de géneros para cada juego. Esto permite una representación más simplificada y directa de la popularidad y la diversidad de géneros de cada juego.

2. **Selección de Características Relevantes**: Se enfocó en mantener solo aquellas características que ofrecen valor significativo para el modelo de recomendación, eliminando cualquier dato redundante o no esencial.

3. **Limpieza de Datos**: Se aseguró de que los valores fueran coherentes y manejables, preparando el dataset para un procesamiento eficiente y un análisis detallado.

#### Objetivo del Modelo

El modelo de recomendación ítem-ítem utilizará este dataset optimizado para identificar juegos similares basándose en las características de recomendaciones, tiempo de juego y géneros. Esto permitirá ofrecer a los usuarios recomendaciones personalizadas de juegos que otros usuarios con gustos similares han disfrutado, potenciando así la experiencia de usuario en la plataforma Steam.

Para más detalles sobre la implementación del modelo y el análisis de resultados, consulte el siguiente notebook: [Modelo de Recomendación Ítem-Ítem](Notebooks/4_Optimizacion_df_ml.ipynb).

- **Data generada en este proceso**
   - Ruta: [`Items óptimos para entrenamiento`](datsets/dataML_item_item.csv)

### 4.1. Filtrado de Usuarios para el Entrenamiento del Modelo

A partir del dataset resultante del proceso de EDA, se realizó un paso adicional de filtrado para enfocarnos en usuarios cuyos datos son óptimos para el entrenamiento de nuestro sistema de recomendación. Este enfoque selectivo asegura que el modelo se entrene en un conjunto de datos de alta calidad, que refleje interacciones significativas de usuarios con los juegos.

#### Criterios de Selección

Los usuarios fueron seleccionados basándose en varios criterios clave para determinar su "optimalidad", incluyendo:

- **Interacción Activa**: Usuarios que han mostrado un nivel significativo de interacción con los juegos, como indicado por su tiempo de juego (`playtime_forever`) y la actividad de recomendación.

- **Variedad en Sentimientos**: Preferencia por usuarios que han expresado una gama de sentimientos en sus reseñas (`Sentiment_analysis`), proporcionando una rica diversidad de datos para el análisis de sentimientos.

- **Interacciones**: Un enfoque en usuarios que han dado han interactuado frecuentemente, asegurando que el modelo pueda identificar juegos con alta interacción por parte de los usuarios

#### Proceso de Filtrado

El filtrado se llevó a cabo en el notebook `4_Optimizacion_df_ml.ipynb`, donde se aplicaron los criterios mencionados para reducir el dataset `data_fusionada` a una selección de usuarios aptos. Este proceso involucró:

1. Identificar usuarios con un tiempo de juego acumulado significativo y una actividad diversa de recomendación y análisis de sentimientos.
2. Excluir usuarios con poca o ninguna actividad de recomendación para asegurar que el dataset final refleje solo interacciones significativas.
3. Consolidar los datos filtrados en un nuevo dataset preparado específicamente para el entrenamiento del modelo.

El resultado de este filtrado es un conjunto de datos más manejable y representativo de usuarios activos y comprometidos, ideal para el desarrollo de un sistema de recomendación preciso.

Para más detalles sobre el filtrado y la preparación de datos, consulte el notebook: [Proceso de Filtrado](Notebooks/4_Optimizacion_df_ml.ipynb).

- **Data generada en este proceso**
   - Ruta: [`Users óptimos para entrenamiento`](datsets/dataML_user_item.csv)



## 5. Desarrollo de la API con FastAPI

En este proyecto, se ha desarrollado una API utilizando FastAPI para exponer los datos y funcionalidades del sistema de recomendación y análisis de datos para la plataforma de juegos Steam. La API proporciona endpoints accesibles que permiten realizar consultas específicas relacionadas con desarrolladores, usuarios, géneros de juegos, y sistemas de recomendación.

### Endpoints Disponibles

A continuación, se describen los endpoints implementados y el propósito de cada uno:

- **`/developer/{developer_name}`**: Devuelve estadísticas sobre los juegos desarrollados por el desarrollador especificado, incluyendo la cantidad de juegos y el porcentaje de contenido gratuito por año.

- **`/userdata/{user_id}`**: Proporciona un resumen de la actividad de un usuario específico, incluyendo el total de dinero gastado, el porcentaje de recomendaciones positivas y la cantidad de ítems adquiridos.

- **`/UserForGenre/{genre}`**: Identifica al usuario que ha acumulado más horas jugadas para un género específico, además de ofrecer un desglose de las horas jugadas por año de lanzamiento.

- **`/best_developer_year/{year}`**: Determina el top 3 de desarrolladores con juegos más recomendados por usuarios para el año especificado.

- **`/developer_reviews_analysis/{developer_name}`**: Analiza las reseñas de juegos de un desarrollador específico, devolviendo el número de reseñas negativas y positivas.

- **`/recomendacion_juego/{item_id}`**: Genera una lista de 5 juegos recomendados similares al juego especificado.

- **`/recomendacion_usuario/{user_id}`**: Recomienda una lista de 5 juegos a un usuario específico, basado en las preferencias de usuarios similares.

### Cómo Consumir la API

Para consumir la API, los usuarios pueden realizar solicitudes HTTP GET a los endpoints proporcionados. Aquí hay un ejemplo de cómo realizar una solicitud a uno de los endpoints:

curl -X 'GET'
'http://127.0.0.1:8000/developer/Valve'
-H 'accept: application/json'

Este comando `curl` consulta el endpoint `/developer/{developer_name}` para obtener estadísticas de los juegos desarrollados por "Valve".

### Documentación de la API

La API cuenta con documentación automática generada por FastAPI, accesible visitando `/docs` o `/redoc` en el navegador después de iniciar la aplicación. Esta documentación proporciona una descripción detallada de cada endpoint, los parámetros esperados y los modelos de respuesta.

### Ejecución Local de la API

Para ejecutar la API localmente, se puede utilizar el siguiente comando desde el directorio raíz del proyecto:

**shell**

uvicorn main:app --reload

## Deployment en Render

El sistema de recomendación y análisis de datos de Steam ha sido desplegado en Render, lo que permite un acceso fácil y rápido a la API desde cualquier lugar. Render ofrece una plataforma de despliegue sencilla y poderosa, ideal para aplicaciones como la nuestra que requieren disponibilidad constante y tiempos de respuesta rápidos.

### Acceso a la API

La API puede ser accedida a través de la siguiente URL: [https://render.com](https://pi-ml-steam-czmx.onrender.com/docs)

[![Link Render](https://ibb.co/RgyzCZx)](https://pi-ml-steam-czmx.onrender.com/docs)

[![Link_Render](src/ia.jpeg)](https://pi-ml-steam-czmx.onrender.com/docs)


Esta URL sirve como punto de entrada para todas las solicitudes a los endpoints descritos anteriormente.

### Documentación Interactiva

Gracias a la integración de documentación de FastAPI, los usuarios pueden explorar interactivamente la API, probar los endpoints y ver las respuestas en tiempo real visitando `/docs` o `/redoc` en la URL proporcionada.

### Pasos para el Despliegue

El proceso de despliegue en Render es directo y se gestionó a través de los siguientes pasos:

1. **Creación de una Aplicación Web en Render**: Se configuró una nueva aplicación web en el dashboard de Render, especificando el repositorio de GitHub que contiene el código fuente.

2. **Configuración del Entorno**: Se configuraron las variables de entorno necesarias y se seleccionó el entorno de ejecución adecuado para la aplicación.

3. **Despliegue Automático**: Gracias a la integración continua de Render con GitHub, cada push al repositorio desencadena un nuevo despliegue, asegurando que la versión más reciente de la API esté siempre disponible.

4. **Monitoreo y Logs**: Render proporciona herramientas para monitorear el rendimiento de la aplicación y acceder a logs en tiempo real, facilitando la detección y corrección de cualquier problema.

## Conclusión

Este proyecto demuestra la capacidad de integrar operaciones de Machine Learning con desarrollo de software para crear y desplegar una API robusta y escalable para sistemas de recomendación. A través de la limpieza y preparación de datos, desarrollo de modelos de ML, y la implementación de una API con FastAPI, hemos establecido un sistema que mejora significativamente la experiencia de los usuarios en la plataforma Steam. Continuaremos mejorando y expandiendo la API para incluir más funcionalidades y mantener la precisión de las recomendaciones.

Esperamos que este proyecto sirva como un recurso valioso para aquellos interesados en MLOps, desarrollo de APIs, y sistemas de recomendación.




