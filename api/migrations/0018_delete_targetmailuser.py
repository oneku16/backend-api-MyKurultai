# Generated by Django 4.0.5 on 2022-07-28 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_targetmailuser_alter_meeting_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TargetMailUser',
        ),
    ]
