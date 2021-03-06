# Generated by Django 3.0.5 on 2020-04-26 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200426_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.extendedUser'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.extendedUser'),
        ),
    ]
