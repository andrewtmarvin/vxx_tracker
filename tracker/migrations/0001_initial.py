# Generated by Django 2.2 on 2019-05-01 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('year', models.IntegerField()),
                ('url', models.URLField()),
                ('gps_file', models.FileField(upload_to='gps_files/')),
            ],
        ),
        migrations.CreateModel(
            name='InstaPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('thumb', models.ImageField(blank=True, default='default.png', null=True, upload_to='')),
                ('json_file', models.FileField(blank=True, null=True, upload_to='')),
                ('location_text', models.CharField(max_length=2000)),
                ('pic_url', models.URLField()),
            ],
        ),
    ]