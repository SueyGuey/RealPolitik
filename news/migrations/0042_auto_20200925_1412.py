# Generated by Django 3.1.1 on 2020-09-25 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0041_auto_20200925_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='time_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
