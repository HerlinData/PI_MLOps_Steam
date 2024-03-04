import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

def developer(desarrollador):
    
    devv = pd.read_csv('data_fusionada.csv')
    data_filtrada = devv[devv['developer'] == desarrollador]
    por_año = data_filtrada.groupby('release_date')
    
    resultado = {}
    
    for año, grupo in por_año:
        total_items = len(grupo)
        items_gratis = len(grupo[grupo['price'] == 0])
        porcentaje_gratis = (items_gratis / total_items) * 100 if total_items > 0 else 0
        resultado[año] = {'Cantidad de Items': total_items, 'Contenido Free': f"{porcentaje_gratis:.0f}%"}
        
    return resultado

def userdata(user_id):

    udata = pd.read_csv('data_fusionada.csv')
    data_filtrada = udata[udata['user_id'] == user_id]
    dinero_gastado = data_filtrada['price'].sum()
    
    if len(data_filtrada) > 0:
        porcentaje_recomendacion = (data_filtrada['recommend'].sum() / len(data_filtrada)) * 100
    else:
        porcentaje_recomendacion = 0  
    
    cantidad_items = len(data_filtrada)
    
    resultado = {
        "Usuario": user_id,
        "Dinero gastado": f"{dinero_gastado} USD",
        "% de recomendación": f"{porcentaje_recomendacion:.0f}%",
        "Cantidad de ítems": cantidad_items
    }
    
    return resultado

def UserForGenre(genero):

    ufg = pd.read_csv('data_fusionada.csv')
    data_filtrada = ufg[ufg['genres'].str.contains(genero, case=False, na=False)].copy()
    data_filtrada['playtime_hours'] = data_filtrada['playtime_forever'] / 60

    usuario_max_horas = data_filtrada.groupby('user_id')['playtime_hours'].sum().idxmax()
    horas_por_año = data_filtrada.groupby('release_date')['playtime_hours'].sum().reset_index()
    
    horas_por_año.sort_values(by='release_date', inplace=True)
    horas_list_formatted = [{"Año": row['release_date'], "Horas": round(row['playtime_hours'], 2)} for index, row in horas_por_año.iterrows()]

    resultado = {
        "Usuario con más horas jugadas para Género": genero + " : " + usuario_max_horas,
        "Horas jugadas": horas_list_formatted
    }
    
    return resultado

def best_developer_year(año):
    
    bdy = pd.read_csv('data_fusionada.csv')
    filtered_data = bdy[(bdy['release_date'] == año) & (bdy['recommend'] == True) & (bdy['Sentiment_analysis'] > 0)]
    developer_counts = filtered_data.groupby('developer').size().reset_index(name='counts')
    sorted_developers = developer_counts.sort_values(by='counts', ascending=False).head(3)
    
    result = [{"Puesto 1": sorted_developers.iloc[0]['developer']}, 
              {"Puesto 2": sorted_developers.iloc[1]['developer']}, 
              {"Puesto 3": sorted_developers.iloc[2]['developer']}]
    
    return result

def developer_reviews_analysis(desarrolladora):
    
    dra = pd.read_csv('data_fusionada.csv')
    data_filtrada = dra[dra['developer'] == desarrolladora]
    
    negative_reviews = len(data_filtrada[data_filtrada['Sentiment_analysis'] == 0])
    neutral_reviews = len(data_filtrada[data_filtrada['Sentiment_analysis'] == 1])
    positive_reviews = len(data_filtrada[data_filtrada['Sentiment_analysis'] == 2])
    resultado = {desarrolladora: {"Negative": negative_reviews, "Positive": positive_reviews}}
    
    return resultado


def recomendacion_juego(id_producto):

    df = pd.read_csv("data_fusionada.csv")
    
    columnas = ['app_name', 'item_id', 'genres']
    df = df[columnas]
    
    # Filtrar las filas que no deseamos
    df = df[df['genres'] != 'Pendiente de clasificación']
    
    df_dummies = pd.get_dummies(df, columns=['genres'], prefix="")
    df_agrupado = df_dummies.groupby(['item_id', 'app_name'], as_index=False).sum()
    
    # Calcular la similitud del coseno basada en las variables dummy
    similitudes = cosine_similarity(df_agrupado.iloc[:, 2:])
    
    try:
        idx = df_agrupado.index[df_agrupado['item_id'] == id_producto].tolist()[0]
        similarity_scores = list(enumerate(similitudes[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        indices_similares = [i[0] for i in similarity_scores[1:6]]
        
        # Obtener los nombres de los 5 juegos recomendados
        juegos_recomendados = df_agrupado.iloc[indices_similares]['app_name']
        
        return juegos_recomendados.to_list()
    except IndexError:
        return "El juego con el ID especificado no existe en la base de datos."
    
# def recomendacion_usuario(user_id):
    
#     columnas = ['user_id', 'item_id', 'recommend', 'app_name']
#     df = pd.read_csv('data_fusionada.csv', usecols=columnas)
#     top_n = 5
    
#     df['interaction'] = df['recommend'].astype(int)
    
#     matriz_utilidad = df.pivot_table(index='user_id', columns='item_id', values='interaction', fill_value=0)
#     similitudes = cosine_similarity(matriz_utilidad)
#     similitudes_df = pd.DataFrame(similitudes, index=matriz_utilidad.index, columns=matriz_utilidad.index)
    
#     if user_id not in similitudes_df.index:
#         return "El ID de usuario proporcionado no existe en la base de datos."
    
#     usuarios_similares = similitudes_df[user_id].sort_values(ascending=False)[1:11]
    
#     juegos_recomendados = set()
#     for usuario_similar in usuarios_similares.index:
#         juegos_usuario_similar = set(matriz_utilidad.columns[(matriz_utilidad.loc[usuario_similar] > 0)])
#         juegos_usuario = set(matriz_utilidad.columns[(matriz_utilidad.loc[user_id] > 0)])
#         juegos_recomendados.update(juegos_usuario_similar.difference(juegos_usuario))
    
#     juegos_recomendados = list(juegos_recomendados)[:top_n]
    
#     nombres_juegos = df[df['item_id'].isin(juegos_recomendados)]['app_name'].drop_duplicates().tolist()
    
#     return nombres_juegos


def recomendacion_usuario(user_id):
    # Carga de datos con las columnas necesarias
    columnas = ['user_id', 'item_id', 'recommend', 'app_name', 'Sentiment_analysis']
    df = pd.read_csv('usuarios_filtrados.csv', usecols=columnas)
    top_n = 5
    # Convertir Sentiment_analysis de bool a int para optimizar
    df['Sentiment_analysis'] = df['Sentiment_analysis'].astype(int)
    
    # Filtrar por Sentiment_analysis para incluir solo negativos (0) y positivos (1), y usar copy()
    df_filtrado = df[df['Sentiment_analysis'].isin([0, 1])].copy()
    
    # Convertir 'recommend' a enteros
    df_filtrado['interaction'] = df_filtrado['recommend'].astype(int)
    
    # Crear la matriz de utilidad
    matriz_utilidad = df_filtrado.pivot_table(index='user_id', columns='item_id', values='interaction', fill_value=0)
    
    # Calcular la similitud de coseno entre usuarios
    similitudes = cosine_similarity(matriz_utilidad)
    similitudes_df = pd.DataFrame(similitudes, index=matriz_utilidad.index, columns=matriz_utilidad.index)
    
    if user_id not in similitudes_df.index:
        return "El ID de usuario proporcionado no existe en la base de datos."
    
    # Encontrar usuarios similares
    usuarios_similares = similitudes_df[user_id].sort_values(ascending=False)[1:11]
    
    # Recopilar recomendaciones
    juegos_recomendados = set()
    for usuario_similar in usuarios_similares.index:
        juegos_usuario_similar = set(matriz_utilidad.columns[(matriz_utilidad.loc[usuario_similar] > 0)])
        juegos_usuario = set(matriz_utilidad.columns[(matriz_utilidad.loc[user_id] > 0)])
        juegos_recomendados.update(juegos_usuario_similar.difference(juegos_usuario))
    
    juegos_recomendados = list(juegos_recomendados)[:top_n]
    
    # Obtener nombres de los juegos recomendados
    nombres_juegos = df[df['item_id'].isin(juegos_recomendados)]['app_name'].drop_duplicates().tolist()
    
    return nombres_juegos





# def best_developer_year(anio):
#     # Cargar el DataFrame desde el archivo parquet
#     df_merged = pd.read_parquet('data/df_merge.parquet')
    
#     # Convertir 'item_id' a object en ambos DataFrames
#     df_merged['Sentiment_analysis'] = df_merged['Sentiment_analysis'].astype('int')
#     df_merged['item_id'] = df_merged['item_id'].astype('object')
    
#     df_merged['recommend'] = df_merged['recommend'].astype(bool)
    
#     # Filtrar por el año dado
#     df_filtered = df_merged[df_merged['Años'] == anio]

#     # Filtrar por reviews positivas y recomendadas
#     df_filtered = df_filtered[(df_filtered['recommend'] == True) & (df_filtered['Sentiment_analysis'] == 2)]

#     # Contar el número de juegos recomendados por cada desarrollador
#     developer_counts = df_filtered.groupby('publisher')['item_id'].nunique()

#     # Obtener el top 3 de desarrolladores
#     top_developers = developer_counts.nlargest(3)

#     # Construir el resultado en el formato especificado
#     resultado = [{"Puesto {}".format(i+1): developer} for i, developer in enumerate(top_developers.index)]
#     cadena_json = json.dumps(resultado, indent=2)
#     return (cadena_json)