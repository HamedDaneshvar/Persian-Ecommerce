# Generated by Django 4.2.11 on 2024-04-25 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slider',
            name='sub_title',
        ),
        migrations.AddField(
            model_name='slider',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='slider',
            name='subtitle',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Subtitle'),
        ),
    ]
