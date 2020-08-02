# Generated by Django 3.0.6 on 2020-07-30 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('faqs', '0002_auto_20200630_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Category'),
        ),
    ]
