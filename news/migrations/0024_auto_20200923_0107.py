# Generated by Django 3.1.1 on 2020-09-23 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0023_auto_20200827_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(default='Author', max_length=100),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='site',
            field=models.CharField(default='News', max_length=100),
        ),
        migrations.AlterField(
            model_name='article',
            name='site_url',
            field=models.URLField(default='google.com', max_length=100),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(max_length=100),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=100),
        ),
    ]