# Generated by Django 4.1.1 on 2022-10-28 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_defect_revision'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defect',
            name='nickname',
        ),
        migrations.AlterField(
            model_name='defect',
            name='description',
            field=models.CharField(default=None, max_length=255),
        ),
    ]