# Generated by Django 2.2 on 2019-05-08 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0014_auto_20190508_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayroute',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='dayroute',
            name='lng',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='dayroute',
            name='rest_day_text',
            field=models.TextField(null=True),
        ),
    ]