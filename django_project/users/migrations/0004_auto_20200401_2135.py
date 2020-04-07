# Generated by Django 3.0.4 on 2020-04-01 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200401_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendeduser',
            name='medic_code',
            field=models.CharField(default='MEDIC_DEFAULT', max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.extendedUser'),
        ),
    ]