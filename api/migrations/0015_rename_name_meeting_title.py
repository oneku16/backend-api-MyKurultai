# Generated by Django 4.0.5 on 2022-07-21 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_room_seats'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='name',
            new_name='title',
        ),
    ]
