from geopy.geocoders import Nominatim
from functools import partial
import pandas as pd

dataset = pd.read_csv('df2021-08-03.csv')
# Создание экземпляра геокодера
geolocator = Nominatim(user_agent="my_application")
geocode = partial(geolocator.geocode, language="es")
#Функция для получения координат по названию населенного пункта
def get_coordinates(location):
    try:
        # Поиск координат местоположения
        geo = geocode(location.split(',')[0].strip())
        # Возвращаем координаты (широта, долгота) в виде кортежа
        return (geo.latitude, geo.longitude)
    except:
        # Если координаты не найдены, возвращаем None
        return None
# Применение функции к столбцу 'area' и сохранение результатов в двух новых столбцах 'latitude' и 'longitude'
dataset[['latitude', 'longitude']] = dataset['area'].apply(get_coordinates).apply(pd.Series)