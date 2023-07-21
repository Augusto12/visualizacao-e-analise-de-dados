import pandas as pd
import geopandas as gpd

def load_data():
    subestacoes = pd.read_csv('./data/subestacoes-base-existentes.csv')
    estados_regioes_brasil = pd.read_csv('./data/estados-regioes.csv')
    geodados_brasil = gpd.read_file('./data/geodados-brasil.json')

    subestacoes = subestacoes.fillna('')
    subestacoes['Nome'] = subestacoes['Nome'].str.replace('SE ', '')

    geosubestacoes = gpd.GeoDataFrame(
        subestacoes,
        geometry=gpd.points_from_xy(subestacoes.Longitude, subestacoes.Latitude),
        crs=geodados_brasil.crs
    )

    geosubestacoes = gpd.sjoin(geosubestacoes, geodados_brasil, how="inner", op="within")
    geosubestacoes = geosubestacoes.merge(estados_regioes_brasil, on='id', how='left')

    geosubestacoes.rename(columns={'Latitude':'lat', 'Longitude':'lon'},inplace=True)

    return geosubestacoes

