# Generated by Django 2.2 on 2019-05-13 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0021_auto_20190512_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayroute',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dayroute',
            name='lng',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
