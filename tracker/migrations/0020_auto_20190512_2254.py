# Generated by Django 2.2 on 2019-05-13 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0019_auto_20190512_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instapost',
            name='thumb_url',
            field=models.URLField(max_length=2000, null=True),
        ),
    ]
