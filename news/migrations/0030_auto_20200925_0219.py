# Generated by Django 3.1.1 on 2020-09-25 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0029_auto_20200925_0217'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='article',
            unique_together={('title', 'author')},
        ),
    ]