from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('', index), # http://127.0.0.1:8000/applications/
    path('applications/', application),
    path('visualization/', visualization),
    path('anomaly/', anomaly_predicts),
    #path('categories/', categories),
    #path('reload/', reload_defects),
    #path('reload_strict/', reload_applications),
    #path('test/', test),
    #path('view/<int:district_id>', district),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive), 
]