# Generated by Django 3.0.6 on 2020-07-05 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analytic',
            name='ip_address',
        ),
        migrations.RemoveField(
            model_name='analytic',
            name='user',
        ),
    ]
