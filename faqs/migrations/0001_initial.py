# Generated by Django 3.0.6 on 2020-07-01 03:23

import codewithtm.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('slug', models.SlugField(blank=True, max_length=20, unique=True)),
                ('question', models.TextField(validators=[codewithtm.validators.validate_content])),
                ('answer', models.TextField(validators=[codewithtm.validators.validate_content])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_faqs', to='categories.Category')),
            ],
        ),
    ]
