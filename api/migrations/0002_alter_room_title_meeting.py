# Generated by Django 4.0.5 on 2022-07-01 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='title',
            field=models.CharField(max_length=150),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('room_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.room')),
            ],
        ),
    ]