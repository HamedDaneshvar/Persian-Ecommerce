# Generated by Django 3.2.15 on 2022-12-28 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_transtport_order_transport'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.IntegerField(null=True, verbose_name='Transaction ID'),
        ),
    ]