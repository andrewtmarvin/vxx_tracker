# Generated by Django 2.2 on 2019-05-01 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20190430_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='instapost',
            name='caption',
            field=models.CharField(max_length=5000, null=True),
        ),
    ]
