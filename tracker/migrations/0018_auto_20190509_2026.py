# Generated by Django 2.2 on 2019-05-10 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0017_auto_20190509_2021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instapost',
            old_name='uploader_profile',
            new_name='uploader_profile_url',
        ),
    ]
