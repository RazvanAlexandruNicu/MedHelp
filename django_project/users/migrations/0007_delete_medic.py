# Generated by Django 3.0.4 on 2020-04-02 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('users', '0006_medic'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Medic',
        ),
    ]