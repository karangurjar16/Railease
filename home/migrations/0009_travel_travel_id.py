# Generated by Django 5.0.2 on 2024-04-01 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_helper_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='travel_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
