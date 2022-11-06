from .models import *
from .serializers import *

import pandas as pd
import numpy as np
from datetime import *

from django.db.models import Count

from datetime import datetime, timedelta


import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from collections import Counter

districts = {
700: "red",
500: "blue",
600: "green",
200: "yellow",
400: "orange",
800: "blue",
300: "red",
1000: "green",
100: "orange",
900: "yellow",
}

distrct_numbers = [600,500,600,200,400,800,300,1000,100,900]
"""
Дефекты, заявки по которым могут быть закрыты за 10 минут:
• Оповещение от 112 (корневой идентификатор дефекта 2303).
• Проникновение в шахту лифта (корневой идентификатор дефекта 2245).
• Заблокирована входная дверь подъезда, оборудованная домофоном, кодовым замком (на вход/выход) (корневой идентификатор дефекта 1903).
• Сообщить, заменить код домофона (корневой идентификатор дефекта 2396).
• Требуется обеспечение водой (отсутствует холодная вода более 4 часов) (корневой идентификатор дефекта 1922).
• Застревание пассажира в лифте (в данный момент) (корневой идентификатор дефекта 1771).
• Управление освещением подъезда (корневой идентификатор дефекта 2096).
• Ввод в эксплуатацию ИПУ воды (замена, демонтаж, пропуск межповерочного интервала) (корневой идентификатор дефекта 7907).
• Подача документов о поверке ИПУ воды в электронном виде 
(корневой идентификатор дефекта 7906).
"""

closed10 = [2303,2245,1903,2396,1922,1771,2096,7907,7906]


sns.set_theme(style="ticks")
sns.set(rc={'axes.facecolor':'#C4DFE3', 'figure.facecolor':'#64a8b3'})



def moscow_graph():
    bars = {
        'x' : [],
        'Обычные заявки' : [],
        'Аномальные заявки' : [],
    }
    for key in districts:
        df = pd.DataFrame(list(Adress.objects.filter(district_id=key).values('latitude', 'longitude')))
        df = df.loc[~(df==0).all(axis=1)]
        sns.scatterplot(x= df["latitude"], y=df["longitude"], color = districts[key])
        bars["x"].append(key)
        adcount = 0
        for adress in Adress.objects.filter(district_id=key):
            adcount += Application.objects.filter(anomaly = True).filter(adress_id = adress).count()
        bars['Аномальные заявки'].append(adcount)

        bars['Обычные заявки'].append(Adress.objects.filter(district_id=key).count() - adcount)


    plt.savefig('G:\innozhk\static\moscow.png')
    #bar = sns.barplot(x = 'x', y= 'y', data=bars, color='#64a8b3')
    print(bars)
    dfbars = pd.DataFrame.from_dict(bars)
    bar = dfbars.set_index('x').plot(kind='bar', stacked=True, color=['#64a8b3', '#C4DFE3'])
    #bar.set(xticklabels=[])
    bar.set(title='Кол-во заявок по региону')
    bar.set(ylabel=None, xlabel=None)
    plt.savefig('G:\innozhk\static\districts.png')

    return 'G:\innozhk\static\districts.png'


def district_graph(district):
    pie = {
        'data' : [],
        'label' : ['Обычные заявки', 'Аномальные заявки'],
    }

    fig, axs = plt.subplots(2)

    apps = []
    adcount = 0
    for adress in Adress.objects.filter(district_id=district):
        adcount += Application.objects.filter(anomaly = True).filter(adress_id = adress).count()
        apps.append(Application.objects.get(adress_id = adress))

    pie['data'].append(Adress.objects.filter(district_id=district).count() - adcount)
    pie['data'].append(adcount)


    #bar = sns.barplot(x = 'x', y= 'y', data=bars, color='#64a8b3')
    axs[1].pie(pie['data'], labels = pie['label'], colors = ['#C4DFE3','#64a8b3'], autopct='%.0f%%')
    #bar.set(xticklabels=[])
    #bar.set(title='Кол-во заявок по региону')
    #bar.set(ylabel=None, xlabel=None)

    time = []
    for app in apps:
        time.append(app.created_at.hour)
    
    x = Counter(time).keys()
    y = Counter(time).values()
    print(y)

    axs[0].bar(x,y)
    plt.savefig('G:\innozhk\static\district_pie.png')
    return 'G:\innozhk\static\district_pie.png'


def region_graph(region):
    pie = {
        'data' : [],
        'label' : ['Обычные заявки', 'Аномальные заявки'],
    }

    fig, axs = plt.subplots(2)

    apps = []
    adcount = 0
    for adress in Adress.objects.filter(region_id=region):
        adcount += Application.objects.filter(anomaly = True).filter(adress_id = adress).count()
        apps.append(Application.objects.get(adress_id = adress))

    pie['data'].append(Adress.objects.filter(region_id=region).count() - adcount)
    pie['data'].append(adcount)


    #bar = sns.barplot(x = 'x', y= 'y', data=bars, color='#64a8b3')
    axs[1].pie(pie['data'], labels = pie['label'], colors = ['#C4DFE3','#64a8b3'], autopct='%.0f%%')
    #bar.set(xticklabels=[])
    #bar.set(title='Кол-во заявок по региону')
    #bar.set(ylabel=None, xlabel=None)

    time = []
    for app in apps:
        time.append(app.created_at.hour)
    
    x = Counter(time).keys()
    y = Counter(time).values()
    print(y)

    axs[0].bar(x,y)
    plt.savefig('G:/innozhk/static/region_pie.png')
    return 'G:/innozhk/static/region_pie.png'
        
