# Generated by Django 3.1 on 2020-08-16 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_filter_teamname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='name',
            field=models.CharField(default='filter', max_length=20),
        ),
        migrations.AlterField(
            model_name='rule',
            name='name',
            field=models.CharField(default='rule', max_length=20),
        ),
    ]
