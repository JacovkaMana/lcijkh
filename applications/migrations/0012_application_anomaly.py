# Generated by Django 4.1.1 on 2022-11-01 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0011_alter_adress_entrance'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='anomaly',
            field=models.BooleanField(default=False),
        ),
    ]
