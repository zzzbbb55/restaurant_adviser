# Generated by Django 2.1.5 on 2020-03-05 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_adv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='rate',
            field=models.FloatField(default=0),
        ),
    ]