import pandas as pd
import numpy as np

def developer(desarrollador):
    
    devv = pd.read_csv('datasets/data_transf/data_fusionada.csv')
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

    udata = pd.read_csv('datasets/data_transf/data_fusionada.csv')
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

    ufg = pd.read_csv('datasets/data_transf/data_fusionada.csv')
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
    
    bdy = pd.read_csv('datasets/data_transf/data_fusionada.csv')
    filtered_data = bdy[(bdy['release_date'] == año) & (bdy['recommend'] == True) & (bdy['Sentiment_analysis'] > 0)]
    developer_counts = filtered_data.groupby('developer').size().reset_index(name='counts')
    sorted_developers = developer_counts.sort_values(by='counts', ascending=False).head(3)
    
    result = [{"Puesto 1": sorted_developers.iloc[0]['developer']}, 
              {"Puesto 2": sorted_developers.iloc[1]['developer']}, 
              {"Puesto 3": sorted_developers.iloc[2]['developer']}]
    
    return result

def developer_reviews_analysis(desarrolladora):
    
    dra = pd.read_csv('datasets/data_transf/data_fusionada.csv')
    data_filtrada = dra[dra['developer'] == desarrolladora]
    
    negative_reviews = len(data_filtrada[data_filtrada['Sentiment_analysis'] == 0])
    neutral_reviews = len(data_filtrada[data_filtrada['Sentiment_analysis'] == 1])
    positive_reviews = len(data_filtrada[data_filtrada['Sentiment_analysis'] == 2])
    resultado = {desarrolladora: {"Negative": negative_reviews, "Positive": positive_reviews}}
    
    return resultado