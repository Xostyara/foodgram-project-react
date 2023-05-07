# Generated by Django 3.2.15 on 2022-09-27 19:58

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название тэга')),
                ('color', colorfield.fields.ColorField(default='#ffffff', image_field=None, max_length=7, samples=None, unique=True, verbose_name='Цвет тэга')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Идентификатор тэга')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
    ]