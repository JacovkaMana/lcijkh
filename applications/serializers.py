from django.db import models
from traitlets import default
from rest_framework import serializers
from .models import *





class AdressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Adress
        fields = ('adress', 'latitude', 'longitude', 'region_id', 'district_id')

"""
    region_id = models.IntegerField()
    district_id = models.IntegerField()
    adress = models.TextField()
    entrance = models.CharField(max_length = 255)
    floor = models.CharField(max_length = 255)
    flat = models.CharField(max_length = 255)
    managing_id = models.ForeignKey('Managing', on_delete=models.CASCADE,)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
"""


class AppSerializer(serializers.ModelSerializer):
    adress_id = AdressSerializer(many=False)
    
    class Meta:
        model = Application
        fields = ('unique_id', 'description', 'started_at', 'defect_id_id', 'status', 'anomaly', 'adress_id')

"""
    unique_id  = models.CharField(primary_key=True, max_length=10, unique=True)
    created_at = models.DateTimeField()
    started_at = models.DateTimeField()
    created_from_id = models.CharField(max_length = 255)
    created_by = models.CharField(max_length = 255)
    incident = models.BooleanField(default=False)
    edited_by = models.CharField(max_length = 255)
    edited_organization = models.CharField(max_length = 255)
    defect_id = models.ForeignKey('Defect', on_delete=models.CASCADE,)
    adress_id = models.ForeignKey('Adress', on_delete=models.CASCADE,)
    description = models.TextField(blank = True)
    has_question = models.BooleanField(default=False)
    status = models.CharField(max_length = 255)
    deny_id = models.IntegerField()
    closed_at = models.DateTimeField()
    time_from = models.TimeField(null = True, blank = True, default=None)
    time_until = models.TimeField(null = True, blank = True, default=None)
    anomaly = models.BooleanField(default = False)

"""

