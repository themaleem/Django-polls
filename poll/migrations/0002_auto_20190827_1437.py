# Generated by Django 2.1.5 on 2019-08-27 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='first_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='poll',
            name='last_name',
            field=models.CharField(max_length=200),
        ),
    ]
