# Generated by Django 2.2 on 2019-05-04 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0010_auto_20190504_0215'),
    ]

    operations = [
        migrations.AddField(
            model_name='instapost',
            name='post_id',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
