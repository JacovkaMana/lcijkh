from .models import *
from .serializers import *

import pandas as pd
import numpy as np
from datetime import *

from django.db.models import Count

from datetime import datetime, timedelta

import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


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


def get_one():
    id = 73408572
    print(Application.objects.get(unique_id = id).description)

def anomaly_apps():

    time_count = 0
    for app in Application.objects.all():
        app.anomaly = False
        timdel = app.closed_at - app.created_at
        if timdel.seconds//60 < 5:
            if (not int(app.defect_id.id) in closed10):
                app.anomaly = True
                app.save()
                time_count += 1
                #print('Anomaly at', app.unique_id, 'defect ', app.defect_id.id)
    print('Аномалий по времени = ', time_count)

    adress_count = 0

    for adress in Adress.objects.all():
            if (adress.latitude >= 56) or (adress.latitude <= 55) or (adress.longitude >= 38) or (adress.longitude <= 37):
                app = Application.objects.get(adress_id = adress)
                app.anomaly = True
                app.save()
                adress_count += 1

    for adress in Adress.objects.filter(district_id=1000):
        app = Application.objects.get(adress_id = adress)
        app.anomaly = False
        timdel = app.closed_at - app.created_at
        if timdel.seconds//60 < 14:
            if (not int(app.defect_id.id) in closed10):
                app.anomaly = True
        app.save()
    
    print('Аномалий по координатам = ', adress_count)



    df = pd.DataFrame(list(Application.objects.all().values()))
    df = df.drop(['created_by', 'time_from', 'time_until', 'has_question', 'description'], axis = 1)

    ord_enc = OrdinalEncoder()
    for time in ['created_at', 'started_at', 'closed_at']:
        df[time + 'Year'] = df[time].apply(lambda timedel: timedel.year)

        df[time + 'Month'] = df[time].apply(lambda timedel: timedel.month)

        df[time + 'Day'] = df[time].apply(lambda timedel: timedel.day)

        df[time + 'Hour'] = df[time].apply(lambda timedel: timedel.hour)

        df[time + 'Minute'] = df[time].apply(lambda timedel: timedel.minute)

    df2 = pd.DataFrame(list(Adress.objects.all().values()))

    df2["adress_id_id"] = df2["id"]
    df2 = df2.drop(['id'], axis = 1)
    df2["adress"] = ord_enc.fit_transform(df2[["adress"]])


    df = df.drop(['created_at', 'started_at', 'closed_at', 'unique_id'], axis = 1)

    df["created_from_id"] = ord_enc.fit_transform(df[["created_from_id"]])
    df["anomaly"] = ord_enc.fit_transform(df[["anomaly"]])
    df["status"] = ord_enc.fit_transform(df[["status"]])
    df["incident"] = ord_enc.fit_transform(df[["incident"]])
    df["edited_by"] = ord_enc.fit_transform(df[["edited_by"]])
    df["edited_organization"] = ord_enc.fit_transform(df[["edited_organization"]])
    #df["country_of_origin"] = ord_enc.fit_transform(df[["country_of_origin"]])
    #df["variety"] = ord_enc.fit_transform(df[["variety"]])

    data = pd.merge(df, df2, on="adress_id_id")
    data = data.drop(["adress_id_id", 'entrance', 'floor', 'flat'], axis = 1)
    print(data.iloc[1])

    model = LinearRegression()
    x = data.drop(['anomaly'], axis = 1)
    y = data['anomaly']
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.50, random_state = 2020, stratify=y)
    ss = StandardScaler()
    X_train_scaled = ss.fit_transform(X_train)
    X_test_scaled = ss.transform(X_test)
    y_train = np.array(y_train)

    rfc = RandomForestClassifier()
    rfc.fit(X_train_scaled, y_train)
    print(rfc.score(X_train_scaled, y_train))



    feats = {}
    for feature, importance in zip(data.columns, rfc.feature_importances_):
        feats[feature] = importance
    importances = pd.DataFrame.from_dict(feats, orient='index').rename(columns={0: 'Gini-Importance'})
    importances = importances.sort_values(by='Gini-Importance', ascending=False)
    importances = importances.reset_index()
    importances = importances.rename(columns={'index': 'Features'})
    #sns.set(font_scale = 5)
    #sns.set(style="whitegrid", color_codes=True, font_scale = 1.7)
    fig, ax = plt.subplots()
    fig.set_size_inches(30,15)
    sns.barplot(x=importances['Gini-Importance'], y=importances['Features'], data=importances, color='skyblue')
    plt.xlabel('Importance', fontsize=25, weight = 'bold')
    plt.ylabel('Features', fontsize=25, weight = 'bold')
    plt.title('Feature Importance', fontsize=25, weight = 'bold')

    plt.savefig('G:/innozhk/static/mlearning.png')
    return 'G:/innozhk/static/mlearning.png'