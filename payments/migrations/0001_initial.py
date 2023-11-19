# Generated by Django 3.2.15 on 2023-11-19 05:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('merchant', models.CharField(max_length=36, validators=[django.core.validators.RegexValidator(code='invalid_length', message='Merchant must be exactly 36 characters and like Zarinpal         merchant be', regex='.{8}\\-.{4}\\-.{4}\\-.{4}\\-.{12}')], verbose_name='Merchant')),
                ('types', models.CharField(choices=[('zarinpal', 'Zarinpal Payment Gateway')], max_length=50, unique=True, verbose_name='Payment Type')),
                ('available', models.BooleanField(default=True, verbose_name='Available')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
