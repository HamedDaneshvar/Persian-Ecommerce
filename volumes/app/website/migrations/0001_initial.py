# Generated by Django 4.2.11 on 2024-04-25 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
                ('sub_title', models.CharField(blank=True, max_length=250, null=True, verbose_name='Sub Title')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Link')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
