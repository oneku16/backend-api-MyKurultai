# Generated by Django 4.0.5 on 2022-07-01 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_room_title_meeting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='title',
            new_name='name',
        ),
    ]
