from django.shortcuts import render, HttpResponse
from . import instascrape
from .models import InstaPost, DayRoute
import json


# Create your views here.
condition = False
if condition:
    instascrape.main()

posts = []
try:
    for post in InstaPost.objects.all():
        post_context = []
        post_context.append(post.pk)
        post_context.append(str(post.date))
        post_context.append(post.caption)
        post_context.append(post.location_text)
        post_context.append(post.lat)
        post_context.append(post.lng)
        post_context.append(post.pic_url)
        post_context.append(post.thumb_url)
        post_context.append(post.uploader_name)
        post_context.append(post.uploader_profile_url)
        posts.append(post_context)
except:
    pass

routes_2016 = []
routes_2020 = []
try:
    for day in DayRoute.objects.order_by('day').filter(year=2016):
        day_context = []
        day_context.append(day.year)
        day_context.append(day.day)
        day_context.append('/get_gpx/' + str(day.year) + '/' + str(day.day) + '/')
        if len(day.title) > 50:
            day.title = day.title[:49] + "..."
        day_context.append(day.title)
        day_context.append(day.journal)
        routes_2016.append(day_context)
    for day in DayRoute.objects.order_by('day').filter(year=2020):
        day_context = []
        day_context.append(day.year)
        day_context.append(day.day)
        day_context.append('/get_gpx/' + str(day.year) + '/' + str(day.day) +'/')
        if len(day.title) > 50:
            day.title = day.title[:49] + "..."
        day_context.append(day.title)
        day_context.append(day.journal)
        routes_2020.append(day_context)

except:
    print('error')

def index(request):

    return render(request, 'index.html', { 'posts': json.dumps(posts), 'routes_2016': routes_2016,
                                           'routes_2020': routes_2020 })


def get_gpx(request, year, day):
    try:
        file = DayRoute.objects.get(year=year, day=day)
        if file.gps_file:
            return HttpResponse(file.gps_file)
        else:
            x = [file.lat, file.lng, file.title, file.journal, file.day]
            return HttpResponse(json.dumps(x))
    except:
        pass
