# Generated by Django 3.0.4 on 2020-04-26 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20200426_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='time',
            field=models.CharField(default='ok guys', max_length=10),
        ),
    ]
