# Generated by Django 4.2.10 on 2024-02-16 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_product_image_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_image',
            old_name='Product',
            new_name='product',
        ),
    ]
