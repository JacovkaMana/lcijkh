from math import remainder
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from .scripts import reload
from .models import *
from .serializers import *
from .visualizers import *
from .analizers import *

import pandas as pd
import numpy as np
from datetime import *

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.serializers import serialize
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import FileResponse

from geopy.geocoders import Nominatim, GoogleV3
import re

import googlemaps
from datetime import datetime

#gmaps = googlemaps.Client(key='AIzaSyBgN3Uwko9uPJ1BYusYuxQlzGJFyZ9BKk0')
geolocator = Nominatim(user_agent='myGeocoder')
#geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)

#from geopy.extra.rate_limiter import RateLimiter
#geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
#df2['location'] = df['name'].apply(geocode)

#tudes = []

#geolocator = GoogleV3()
def anomaly_predicts(request):
    path = anomaly_apps()
    with open(path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")

def get_geo(s):
    #s = df['Адрес проблемы'][i]
    s = s.split(',')
    street = s[0]
    house = ''.join(x for x in s[1] if x.isdigit())
    geo = house + ' ' + street + ' Москва'
    location = geolocator.geocode(geo, timeout=5)
    if (location):
        return [location.latitude, location.longitude]
    else:
        return [0, 0]




def get_date(date_df):
    date_df = date_df[:date_df.rfind('.')]
    new_date = datetime.strptime(date_df, '%Y-%m-%d %H:%M:%S')
    return new_date


@api_view(['GET', 'POST'])
def application(request, region = None, district = None, id = None):


        if request.GET:

            data = request.GET


            if "id" in data:
                apps = Application.objects.filter(unique_id=data['id'])
                adress = apps.values('adress_id_id')

            elif "region" in data:
                adress = Adress.objects.filter(region_id=data['region'])
                apps = []
                for ad in adress:
                    apps.append(Application.objects.get(adress_id_id=ad))

            elif "district" in data:
                if (data["district"] == '0'):
                    apps = Application.objects.all()
                else:
                    adress = Adress.objects.filter(district_id=data['district'])
                    apps = []
                    for ad in adress:
                        apps.append(Application.objects.get(adress_id_id=ad))
            
            else:

                return HttpResponse("Select id or region or district")
            appserializer = AppSerializer(apps, many=True)

            return Response(appserializer.data)

        else:
            return HttpResponse("Do a GET")

@api_view(['GET', 'POST'])
def visualization(request, region = None, district = None, all = None):

            
        if request.GET:

            data = request.GET

            if ("region" in data) and (data["region"] == 0):
                path = moscow_graph()
                with open(path, "rb") as f:
                    return HttpResponse(f.read(), content_type="image/jpeg")

            elif "region" in data:
                path = region_graph(data['region'])
                with open(path, "rb") as f:
                    return HttpResponse(f.read(), content_type="image/jpeg")

            elif "district" in data:
                if (data["district"] == '0'):
                    path = moscow_graph()
                    with open(path, "rb") as f:
                        return HttpResponse(f.read(), content_type="image/jpeg")
                else:    
                    path = district_graph(data['district'])
                    with open(path, "rb") as f:
                        #return FileResponse(f)
                        return HttpResponse(f.read(), content_type="image/jpeg")
            
            else:

                return HttpResponse("Select id or region or district")

            appserializer = AppSerializer(apps, many=True)

            return Response(appserializer.data)

        else:
            return HttpResponse("Do a GET")

def index(request):
    return HttpResponse("Страница applications.")

def categories(request):
    if(request.GET):
        print(request.GET)

    if(request.POST):
        print(request.POST)

    return HttpResponse("<h1> Статьи по категорям </h1>")

def district(request, district_id):
    return HttpResponse(f"<h1> {district_id} </h1>")

def archive(request, year):
    if int(year) > 2020:
        #raise Http404()
        return redirect('/', permanent=True)
    return HttpResponse(f' Архив по году {year}')


def pageNotFound(request, exception):
    return HttpResponseNotFound(' Страница не найдена ')

def reload_applications(request):

    Defect.objects.all().delete()
    Application.objects.all().delete()
    Adress.objects.all().delete()
    Managing.objects.all().delete()
    Performing.objects.all().delete()

    defect = pd.read_excel('G:/innozhk/applications/defects1.xlsx')
    defect = defect.replace({'-': 0})
    defect = defect.replace({np.nan: 0})

    defect['Повторное'] = defect['Повторное'].replace({0: '-'})

    for i in range(len(defect['Корневой идентификатор'])):
        
        defic = Defect(
            id = int(defect['Корневой идентификатор'][i]), 
            name = defect['Наименование'][i], 
            category = defect['Категория'][i], 
            revision = int(defect['Повторное срок'][i]), 
            description = defect['Повторное'][i], 
            )
        defic.save()

    """
    for i in [1928,2240, 2254, 2288, 2232, 2435]:
        new = Defect(
                id = i, 
                name = '?', 
                category = '?', 
                revision = 0, 
                description = '?', 
                )

        new.save()
    """


    df = pd.read_csv('G:/innozhk/applications/Part_16_09_22.csv', sep='$')
    df = df.replace({np.nan: 0})

    for i in range(len(df['ИД версии заявки'])):
        try:
            defic = Defect.objects.get(pk=int(df['Идентификатор дефекта'][i]))
        except Defect.DoesNotExist:
            defic = Defect(
            id = int(df['Идентификатор дефекта'][i]), 
            name = df['Наименование дефекта'][i], 
            category = '?', 
            revision = 0, 
            description = df['Описание'][i], 
            )
            print(i)
            defic.save()
    

    for i in range(len(df['ИД версии заявки'])):


        if (Managing.objects.filter(name=df['Наименование управляющей компании'][i])):
            
            man = Managing.objects.filter(name=df['Наименование управляющей компании'][i]).first()
        else:
            man = Managing(
                id  = i,
                name = df['Наименование управляющей компании'][i],
                inn = 0,
            )
            man.save()


        if (Performing.objects.filter(name=df['Наименование обслуживавшей организации (исполнителя)'][i])):

            perf = Performing.objects.filter(name=df['Наименование обслуживавшей организации (исполнителя)'][i]).first()
        else:
            
            perf = Performing(
                id  = df['Идентификатор организации-исполнителя'][i],
                name = df['Наименование обслуживавшей организации (исполнителя)'][i],
                inn = df['ИНН организации-исполнителя'][i],
            )
            perf.save()


        coords = get_geo(df['Адрес проблемы'][i])

        adress = Adress(
            region_id = df['Код района'][i],
            district_id = df['Код округа'][i],
            adress = df['Адрес проблемы'][i],
            entrance = df['Подъезд'][i],
            floor = df['Этаж'][i],
            flat = df['Квартира'][i],
            managing_id = man,
            latitude = coords[0],
            longitude = coords[1],
        )

        adress.save()
        #print(df['Дата создания заявки в формате Timezone'][i])

        app = Application(
            unique_id  = int(df['Корневой ИД заявки'][i]),
            created_at = get_date(df['Дата создания заявки в формате Timezone'][i]),
            started_at = get_date(df['Дата начала действия версии заявки в формате Timezone'][i]),
            created_from_id = df['Код источника поступления заявки'][i],
            created_by = df['Имя создателя заявки'][i],
            incident = False,
            edited_by = df['Пользователь, внесший последнее изменение'][i],
            edited_organization = df['Роль организации пользователя'][i],
            defect_id = Defect.objects.get(pk=int(df['Идентификатор дефекта'][i])),
            adress_id = adress,
            description = df['Описание'][i],
            has_question = False,
            status = df['Код статуса заявки'][i],
            deny_id = 0,
            closed_at = get_date(df['Дата закрытия'][i]),
            time_from = None,
            time_until = None,
        )

        app.save()


    return HttpResponse(' Reload applications')

def test(request):
    anomaly_apps()
    #district_graph()
    #get_one()
    return HttpResponse('test')

def reload_defects():
    Defect.objects.all().delete()

    defect = pd.read_excel('G:/innozhk/applications/defects1.xlsx')
    defect = defect.replace({'-': 0})
    defect = defect.replace({np.nan: 0})

    defect['Повторное'] = defect['Повторное'].replace({0: '-'})

    for i in range(len(defect['Корневой идентификатор'])):
        
        defic = Defect(
            id = int(defect['Корневой идентификатор'][i]), 
            name = defect['Наименование'][i], 
            category = defect['Категория'][i], 
            revision = int(defect['Повторное срок'][i]), 
            description = defect['Повторное'][i], 
            )
        defic.save()

    for i in [1928,2240, 2254, 2288, 2232, 2435]:
        new = Defect(
                id = i, 
                name = '?', 
                category = '?', 
                revision = 0, 
                description = '?', 
                )

        new.save()
    
    return 'succ'


"""
class GetApplicationInfoView(APIView):
    def get(self, request):

        if(request.GET):
            data = request.GET
            print(data)
            if ('id' in data):
                id = data['id']
                print(id)
                app = get_object_or_404(Application, pk=id)
                return JsonResponse({'name' : 'Пидорас'})
                return JsonResponse(model_to_dict(app))
        return HttpResponse('well')
"""