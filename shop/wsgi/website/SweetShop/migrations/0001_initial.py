# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 23:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('price', models.TextField()),
                ('product_logo', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='basket',
            name='productID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SweetShop.Product'),
        ),
        migrations.AddField(
            model_name='basket',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
