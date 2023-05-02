# Предобработка данных по мотивам задания для python 

from geopy.geocoders import Nominatim
from functools import partial
import pandas as pd
import requests
import re
import numpy as np
from datetime import datetime

df = pd.read_csv('df2021-08-03.csv')

df['created'] = pd.to_datetime(df['created'], format='%Y-%m-%dT%H:%M:%S%z')
df['created'] = df['created'].dt.strftime('%Y-%m-%d %H:%M:%S')

def get_currency_rate(date):
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    response = requests.get(url)
    response.encoding = 'utf-8'
    content = response.text
    rate = content.split('<Valute ID="R01235">')[1].split('<Value>')[1].split('</Value>')[0]
    return float(rate.replace(',', '.'))

def convert_salary_to_rubles(salary_from, salary_to, currency, created):
    if currency == 'RUR':
        return np.nanmean([salary_from, salary_to])
    elif pd.isna(currency):
        return None
    else:
        try:
            rate_date = datetime.strptime(created, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
            rate = get_currency_rate(rate_date)
        except:
            return None
        if currency == 'USD':
            return round(np.nanmean([salary_from, salary_to]) * rate, 2)
        elif currency == 'EUR':
            return round(np.nanmean([salary_from, salary_to]) * rate, 2)    
        else:
            return None

df['mean_salary_rub'] = df.apply(lambda x: convert_salary_to_rubles(x['salary_from'], x['salary_to'], x['currency'], x['created']), axis=1)
df['experience'] = df['experience'].astype(str)
df['experience_min'] = df['experience'].apply(lambda x: re.findall('\d+', x)[0] if re.findall('\d+', x) else None)
df['experience_min'] = pd.to_numeric(df['experience_min'], errors='coerce')

befor_len = len(df.columns)

skills_set = set()
for skills in df['skills']:
    if isinstance(skills, str):
        skills_list = skills.split(';')
        skills_set.update(skills_list)

skills_set.discard('')
len_skills = len(skills_set)
for skill in skills_set:
    df[skill] = df['skills'].apply(lambda x: int(skill in x.split(';')) if isinstance(x, str) else 0)
for skill in skills_set:
    df[skill + '_freq'] = df.apply(lambda row: row[skill] / sum(x for x in row[skills_set] if x) if row[skill] != 0 else 0, axis=1)
for skill in skills_set:
    df[skill + '_a_salary'] = df[skill] * df['mean_salary_rub']
for skill in skills_set:
    df[skill + '_f_salary'] = df[skill + '_freq'] * df['mean_salary_rub']

skills_count_top = df.iloc[:, befor_len:(len_skills+befor_len)].sum().sort_values(ascending=False).reset_index().rename(columns={0: 'Количество'})
skills_freq_top = df.filter(regex='_freq$').mean().sort_values(ascending=False).reset_index().rename(columns={0: 'Частота'})
skills_a_salary_top = df.filter(regex='_a_salary$').mean().sort_values(ascending=False).reset_index().rename(columns={0: 'Абсолютная стоимость'})
skills_f_salary_top = df.filter(regex='_f_salary$').mean().sort_values(ascending=False).reset_index().rename(columns={0: 'Относительная стоимость'})
skills_freq_top['index'] = skills_freq_top['index'].str.replace('_freq', '')
skills_a_salary_top['index'] = skills_a_salary_top['index'].str.replace('_a_salary', '')
skills_f_salary_top['index'] = skills_f_salary_top['index'].str.replace('_f_salary', '')
skills_count_top['rank'] = list(reversed(range(1, (len_skills+1))))
skills_freq_top['rank'] = list(reversed(range(1, (len_skills+1))))
skills_a_salary_top['rank'] = list(reversed(range(1, (len_skills+1))))
skills_f_salary_top['rank'] = list(reversed(range(1, (len_skills+1))))
skills_count_top = skills_count_top.set_index('index')
skills_freq_top = skills_freq_top.set_index('index')
skills_a_salary_top = skills_a_salary_top.set_index('index')
skills_f_salary_top = skills_f_salary_top.set_index('index')
top_skills = pd.concat([skills_count_top, skills_freq_top, skills_a_salary_top, skills_f_salary_top], axis=1, join='outer')
top_skills['total_score'] = top_skills['rank'].sum(axis=1)
top_skills.to_csv('top_skills.csv', index=False)


geolocator = Nominatim(user_agent="my_application")
geocode = partial(geolocator.geocode, language="ru")

#Функция для получения координат по названию населенного пункта
def get_coordinates(location):
    try:
        geo = geocode(location.split(',')[0].strip())
        return (geo.latitude, geo.longitude)
    except:
        return None
    
df[['latitude', 'longitude']] = df['area'].apply(get_coordinates).apply(pd.Series)

keywords = {'Разработчик': ['разработчик', 'developer', 'программист', 'Programmer', 'dev', 'разработки'],
            'Тестировщик': ['тестировщик', 'tester', 'qa', 'автотестированию'],
            'Аналитик': ['аналитик', 'analyst'],
            'Инженер': ['архитектор', 'architect', 'Tech', 'Engineer', 'инженер'],
            'Team Lead': ['lead', 'руководитель', 'manager', 'менеджер'],
            'Преподаватель': ['преподаватель', 'учитель', 'педагог', 'методист', 'автор', 'Teacher', 'наставник', 'course', 'курс'],
            'Data Scientis': ['scientist', 'learning']}

def get_profession(vacancy):
    for profession, words in keywords.items():
        for word in words:
            if re.search(word, vacancy, re.IGNORECASE):
                return profession
    return 'Не определено'

df['profession'] = df['vacancy'].apply(get_profession)



df.to_csv('file.csv', index=False)


"""
Было бы круто, если бы можно было вводить ключевое слово в поле и нейросеть сопоставляла бы по смыслу с описанием вакансии и выдавала подходящие вакансии, например "наук", 'биология', 'игры'.
"""