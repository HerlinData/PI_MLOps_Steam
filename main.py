from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Optional
from Functions import *

app = FastAPI()

@app.get("/developer/{developer_name}", 
         description="""<html><body><h1>INSTRUCCIONES</h1>
         <h3>INSTRUCCIONES
1. Haga clic en "Try it out".
2. Ingrese el Developer en el cuadro de abajo.
3. Observe la cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.
4. Sugerencia de developer: Edge of Reality, Standing Stone Games, Valve, TaleWorlds Entertainment.
5. Para cambiar de Developer, copie y pegue de las sugerencias y presione Execute nuevamente.</h3></body></html>""", 
         tags=["Developer Stats"])
async def get_developer_stats(developer_name: str):
    result = developer(developer_name)
    return JSONResponse(content=result)

@app.get("/userdata/{user_id}", 
         description="""<html><body><h1>INSTRUCCIONES</h1>
<h3>1. Haga clic en "Try it out".
<br>2. Ingrese el usuario en el cuadro de abajo.
<br>3. Observe la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
<br>4. Sugerencia de usuarios: 76561198031799936, Imposs1bru, -SEVEN-, SwaRIsLoveSwarIsLife.
<br>5. Para cambiar de usuario, copie y pegue de las sugerencias y presione Execute nuevamente.</h3></body></html>""", 
         tags=["User Data"])
async def get_user_data(user_id: str):
    result = userdata(user_id)
    return JSONResponse(content=result)

@app.get("/UserForGenre/{genre}", 
         description="""<html><body style="background-color: #000000;"><h1 style="color: ffff00;">INSTRUCCIONES</h1>
<h3 style="color: ffff00; font-family: 'Trebuchet MS';">
1. Haga clic en "Try it out".
<br>2. Ingrese el género en el cuadro de abajo.
<br>3. Se devuelve el usuario que acumula más horas jugadas para el género especificado y una lista de la acumulación de horas jugadas por año de lanzamiento.
<br>4. Sugerencia de géneros: Action, RPG, Adventure, Education.
<br>5. Para cambiar de género, copie y pegue de las sugerencias y presione Execute nuevamente.</h3></body></html>""", 
         tags=["User For Genre"])
async def get_user_for_genre(genre: str):
    result = UserForGenre(genre)
    return JSONResponse(content=result)

@app.get("/best_developer_year/{year}", 
         description="""<html><body style="background-color: #000000;"><h1 style="color: ffff00;">INSTRUCCIONES</h1><h3 style="color: ffff00; font-family: 'Trebuchet MS';">
1. Haga clic en "Try it out".
<br>2. Ingrese el año en el cuadro de abajo.
<br>3. Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
<br>4. Sugerencia de años: 1993, 2000, 2010, 2015.
<br>5. Para cambiar el año, simplemente ingrese otro año y presione Execute nuevamente.</h3></body></html>""", 
         tags=["Best Developer Year"])
async def get_best_developer(year: int):
    result = best_developer_year(year)
    return JSONResponse(content=result)

@app.get("/developer_reviews_analysis/{developer_name}", 
         description="""<html><body style="background-color: #000000;"><h1 style="color: ffff00;">INSTRUCCIONES</h1><h3 style="color: ffff00; font-family: 'Trebuchet MS';">
1. Haga clic en "Try it out".
<br>2. Ingrese el nombre del desarrollador en el cuadro de abajo.
<br>3. Se devuelve un análisis de las reseñas de los juegos del desarrollador especificado, categorizando las reseñas en positivas o negativas.
<br>4. Sugerencia de desarrolladores: Valve, Edge of Reality, Ubisoft - San Francisco, Ronimo Games.
<br>5. Para cambiar de desarrollador, copie y pegue de las sugerencias y presione Execute nuevamente.</h3></body></html>""", 
         tags=["Developer Reviews Analysis"])
async def get_developer_reviews(developer_name: str):
    result = developer_reviews_analysis(developer_name)
    return JSONResponse(content=result)

@app.get("/recomendacion_juego/{item_id}", 
         description="""<html><body><h1>INSTRUCCIONES</h1>
<h3>1. Haga clic en "Try it out".
<br>2. Ingrese el ID del juego en el cuadro de abajo.
<br>3. Se consulta por ID del juego y devuelve una lista de recomendaciones para el mismo basadas en otros productos similares.
<br>4. Sugerencia de juegos: 70, 2400, 4000, 13230.
<br>5. Para cambiar de IDs de juego, copie y pegue de las sugerencias y presione Execute nuevamente.</h3></body></html>""", 
         tags=["Recomendación Juego"])
async def get_recomendacion_juego(item_id: int):
    result = recomendacion_juego(item_id)
    return JSONResponse(content=result)

@app.get("/recomendacion_usuario/{user_id}", 
         description="""<html><body><h1>INSTRUCCIONES</h1>
<h3>1. Haga clic en "Try it out".
<br>2. Ingrese el ID del usuario en el cuadro de abajo.
<br>3. Consulta realizada por medio del ID del usuario y retorna un conjunto de sugerencias personalizadas. 
Estas recomendaciones se basan en la afinidad con productos similares.
<br>4. Sugerencia de usuarios: Deus_VuIt, SwaRIsLoveSwarIsLife, 76561198031799936, MMR_Assasin.
<br>5. Para cambiar de usuario, copie y pegue de las sugerencias y presione Execute nuevamente.</h3></body></html>""", 
         tags=["Recomendación Usuario"])
async def get_recomendacion_usuario(user_id: str):
    result = recomendacion_usuario(user_id)
    return JSONResponse(content=result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

