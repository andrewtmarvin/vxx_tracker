# Generated by Django 2.2 on 2019-05-04 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_instapost_thumb_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instapost',
            name='json_file',
        ),
        migrations.RemoveField(
            model_name='instapost',
            name='thumb',
        ),
    ]