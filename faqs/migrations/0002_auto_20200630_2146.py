# Generated by Django 3.0.6 on 2020-07-01 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='slug',
            field=models.SlugField(blank=True, max_length=140, unique=True),
        ),
        migrations.AlterField(
            model_name='faq',
            name='title',
            field=models.CharField(max_length=140),
        ),
    ]
