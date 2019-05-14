from django.db import models
import os
from django.dispatch import receiver
# Create your models here.


class PostRecord(models.Model):
    keep = models.BooleanField()
    post_id = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return 'Post ID: ' + str(self.post_id) + ' ---- Keep: ' + str(self.keep)

class InstaPost(models.Model):
    post_id = models.IntegerField(unique=True, null=True)
    date = models.DateTimeField(auto_now=False)
    caption = models.CharField(null=True, max_length=5000)
    location_text = models.CharField(max_length=2000)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    pic_url = models.URLField()
    thumb_url = models.URLField(null=True, max_length=2000)
    uploader_name = models.CharField(null=True, max_length=200)
    uploader_profile_url = models.URLField(null=True)

    def __str__(self):
        return 'Post from ' + str(self.date)


class DayRoute(models.Model):
    title = models.CharField(max_length=100, null=True)
    day = models.IntegerField()
    year = models.IntegerField()
    gps_file = models.FileField(blank=True, upload_to='gps_files/')
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    journal = models.TextField(null=True)

    def __str__(self):
        return 'Year: ' + str(self.year) + '. Day: ' + str(self.day)








# Ensures thumbnail and json files are deleted when an InstaPost object is removed from the database
# No longer necessary because not saving files on server anymore
# @receiver(models.signals.post_delete, sender=InstaPost)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.thumb:
#         if os.path.isfile(instance.thumb.path):
#             os.remove(instance.thumb.path)
#     if instance.json_file:
#         if os.path.isfile(instance.json_file.path):
#             os.remove(instance.json_file.path)
