# Generated by Django 5.0.2 on 2024-04-20 21:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('info', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('favorite_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.plant_info')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
