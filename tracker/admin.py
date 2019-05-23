from django.contrib import admin
from .models import InstaPost, DayRoute, PostRecord

# Register your models here.
admin.site.register(InstaPost)
admin.site.register(PostRecord)
admin.site.register(DayRoute)
