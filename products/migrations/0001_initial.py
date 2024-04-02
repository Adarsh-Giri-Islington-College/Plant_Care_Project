# Generated by Django 5.0.2 on 2024-03-28 20:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('product_image', models.ImageField(upload_to='')),
                ('product_name', models.CharField(max_length=200)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_quantity', models.IntegerField()),
                ('product_description', models.TextField()),
                ('product_for', models.CharField(blank=True, max_length=500, null=True)),
                ('added_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
