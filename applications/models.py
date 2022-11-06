from django.db import models
from traitlets import default
from rest_framework import serializers

# Create your models here.


class Application(models.Model):
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

class Feedback(models.Model):
    application_id = models.ForeignKey('Application', on_delete=models.CASCADE,)
    notified = models.BooleanField(default = False)
    comment = models.TextField()
    evaluation = models.IntegerField()
    free = models.BooleanField(default = True)
    date = models.DateTimeField()
    cardpay = models.BooleanField(default = False)

class Performance(models.Model):
    application_id = models.ForeignKey('Application', on_delete=models.CASCADE,)
    performing_id = models.ForeignKey('Performing', on_delete=models.CASCADE,)
    name = models.CharField(max_length = 255)
    type = models.CharField(max_length = 255)
    material = models.CharField(max_length = 255)
    return_count = models.IntegerField()
    last_return_at = models.DateTimeField()
    at_revision = models.BooleanField()


class Adress(models.Model):
    region_id = models.IntegerField()
    district_id = models.IntegerField()
    adress = models.TextField()
    entrance = models.CharField(max_length = 255)
    floor = models.CharField(max_length = 255)
    flat = models.CharField(max_length = 255)
    managing_id = models.ForeignKey('Managing', on_delete=models.CASCADE,)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    


class Performing(models.Model):
    id  = models.CharField(primary_key=True, max_length=20, unique=True)
    name = models.CharField(max_length = 255)
    inn = models.CharField(max_length=30)

class Managing(models.Model):
    id  = models.CharField(primary_key=True, max_length=20, unique=True)
    name = models.CharField(max_length = 255)
    inn = models.CharField(max_length=30)

class Defect(models.Model):
    id  = models.CharField(primary_key=True, max_length=20, unique=True)
    name = models.CharField(max_length = 255)
    category = models.CharField(max_length = 255)
    revision = models.IntegerField(default = None)
    description = models.CharField(max_length = 255, default = None)


