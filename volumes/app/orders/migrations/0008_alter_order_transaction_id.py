# Generated by Django 3.2.23 on 2023-12-05 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20231123_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Transaction ID'),
        ),
    ]