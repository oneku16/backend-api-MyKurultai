# Generated by Django 4.0.5 on 2022-07-12 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_meeting_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='is_repeated',
            field=models.BooleanField(default=False),
        ),
    ]