# Generated by Django 5.0.2 on 2024-03-27 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_profile_delete_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
