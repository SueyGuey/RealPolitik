# Generated by Django 3.1.1 on 2020-09-25 03:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0030_auto_20200925_0219'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='timeadded',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 25, 3, 51, 1, 731023, tzinfo=utc)),
        ),
    ]
