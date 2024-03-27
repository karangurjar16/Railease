# Generated by Django 5.0.2 on 2024-03-26 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_route_train'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='station',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='route',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='home.train'),
        ),
    ]
