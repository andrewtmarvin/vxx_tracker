# Generated by Django 2.2 on 2019-05-14 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0022_auto_20190513_1329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dayroute',
            old_name='day_text',
            new_name='journal',
        ),
    ]
