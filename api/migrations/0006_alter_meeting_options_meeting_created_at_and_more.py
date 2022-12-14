# Generated by Django 4.0.5 on 2022-07-17 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_room_id_meeting_room'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='meeting',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='is_repeated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(blank=True, choices=[('p', 'Pending'), ('d', 'Declined'), ('a', 'Accepted')], default='p', help_text='Meeting status', max_length=1),
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
