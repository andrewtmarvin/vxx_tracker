# Generated by Django 3.2.6 on 2021-08-20 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0023_auto_20190513_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instapost',
            name='pic_url',
        ),
        migrations.RemoveField(
            model_name='instapost',
            name='thumb_url',
        ),
        migrations.AddField(
            model_name='instapost',
            name='pic_file',
            field=models.FileField(blank=True, upload_to='post_pics/'),
        ),
        migrations.AddField(
            model_name='instapost',
            name='thumb_file',
            field=models.FileField(blank=True, upload_to='post_thumbs/'),
        ),
    ]