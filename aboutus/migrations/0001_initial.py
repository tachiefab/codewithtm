# Generated by Django 3.0.6 on 2020-07-01 03:23

import codewithtm.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(validators=[codewithtm.validators.validate_content])),
                ('contact_information', models.TextField(validators=[codewithtm.validators.validate_content])),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'About Us',
                'verbose_name_plural': 'About Us',
                'ordering': ['-timestamp'],
            },
        ),
    ]
