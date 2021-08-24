from django.shortcuts import render, HttpResponse
from . import instascrape
from .models import InstaPost, DayRoute
import json


# Upon server reload, run function to update the Django database
# instascrape.main()


# View for main page
def index(request):
    # Refreshes context data from database each page reload
    posts, routes_2016, routes_2020 = generate_context()
    # Renders page from template by passing three context variables
    return render(request, 'index.html', {'posts': json.dumps(posts), 'routes_2016': routes_2016,
                                          'routes_2020': routes_2020})


# View for asynchronous Ajax calls to retrieve large .gpx files from database
def get_gpx(request, year, day):
    # If the day chosen by user is a ride day, returns the .gpx file so Leaflet can draw ride route on map
    try:
        file = DayRoute.objects.get(year=year, day=day)
        if file.gps_file:
            return HttpResponse(file.gps_file)
        # If the day is a rest day (no .gpx file), returns a json containing meta data for that day to diplay on map
        else:
            x = [file.lat, file.lng, file.title, file.journal, file.day]
            return HttpResponse(json.dumps(x))
    except:
        pass


# Generates context variables for use in rendering the Django template
def generate_context():
    # Posts context variable is used by Leaflet to generate map markers
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
            post_context.append(post.pic_file.url)
            post_context.append(post.thumb_file.url)
            post_context.append(post.uploader_name)
            post_context.append(post.uploader_profile_url)
            posts.append(post_context)
    except:
        pass
    print(posts[0])

    # Routes context variables are used by the frontend to create the menu
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
            day_context.append('/get_gpx/' + str(day.year) + '/' + str(day.day) + '/')
            if len(day.title) > 50:
                day.title = day.title[:49] + "..."
            day_context.append(day.title)
            day_context.append(day.journal)
            routes_2020.append(day_context)
    except:
        print('error generating context')
    return posts, routes_2016, routes_2020
