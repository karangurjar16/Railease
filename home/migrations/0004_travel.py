# Generated by Django 5.0.2 on 2024-03-29 07:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_route_charge_register'),
    ]

    operations = [
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('age', models.IntegerField(null=True)),
                ('gender', models.CharField(max_length=30, null=True)),
                ('route', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=30, null=True)),
                ('date1', models.DateField(null=True)),
                ('fare', models.IntegerField(null=True)),
                ('train', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.train')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.register')),
            ],
        ),
    ]
