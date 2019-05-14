import instaloader, geopy
import glob, json
from .models import InstaPost, DayRoute
from django.core.files import File
from PIL import Image
from io import BytesIO


def main():
    username = ""
    password = ""
    session = insta_login(username, password)
    # insta_check(session)
    insta_tagged_check(session)


# authenticate session
def insta_login(username, password):
    session = instaloader.Instaloader(compress_json=False)
    session.login(username, password)
    return session


# function to check for and download new posts
def insta_check(session):
    profile = instaloader.Profile.from_username(session.context, 'andrew_vxx')
    x = 0
    y = 0
    for post in profile.get_posts():
        if glob.glob('andrew_vxx/' + str(post.date).replace(' ', '_').replace(':','-') + '*.jpg'):
            print('exists already x ' + str(x + 1))
            x += 1
        else:
            print("doesn't exist, downloading... x " + str(y + 1))
            session.download_post(post, target=profile.username)
            print("saving tagged post files.")

            # only stores posts in database which have a geolocation
            if post.location == None:
                if post.caption:
                    print('tagged post "' + post.caption + '" does not have geolocation data.')
            else:
                # only stores posts if location is in Vietnam
                p = geopy.point.Point(post.location.lat, post.location.lng)
                geolocator = geopy.Nominatim(user_agent='macekid421')
                location = geolocator.reverse(p)
                if location.raw['address']['country_code'] == 'vn':
                    print("in " + location.raw['address']['country'], 'saving to database.')
                    update_database(post)
                else:
                    print("outside of vietnam, database not updated")
                    print(location.raw['address']['country_code'])
            y += 1
    print(str(x) + " posts already existed. " + str(y) + " posts updated.")

def insta_tagged_check(session):
    profile = instaloader.Profile.from_username(session.context, 'andrew_vxx')
    x = 0
    y = 0
    for post in profile.get_tagged_posts():
        if glob.glob('andrew_vxx/' + str(post.date).replace(' ', '_').replace(':','-') + '*.jpg'):
            print('exists already x ' + str(x + 1))
            x += 1
        else:
            print("doesn't exist, downloading... x " + str(y + 1))
            session.download_post(post, target=profile.username)
            print("saving post files.")

            # only stores posts in database which have a geolocation
            if post.location == None:
                if post.caption:
                    print('post "' + post.caption + '" does not have geolocation data.')
            else:
                # only stores posts if location is in Vietnam
                p = geopy.point.Point(post.location.lat, post.location.lng)
                geolocator = geopy.Nominatim(user_agent='macekid421')
                location = geolocator.reverse(p)
                if location.raw['address']['country_code'] == 'vn':
                    print("in " + location.raw['address']['country'], 'saving to database.')
                    # before updating, moving attributes around so structure is same as post
                    post._node.update({'thumbnail_resources':{0:{'src':post._node['thumbnail_src']}}})
                    update_database(post)
                else:
                    print("outside of vietnam, database not updated")
                    print(location.raw['address']['country_code'])
            y += 1
    print(str(x) + " posts already existed. " + str(y) + " posts updated.")


def update_database(post):
            newpost = InstaPost()
            newpost.date = post.date
            newpost.caption = post.caption
            newpost.lat = post.location.lat
            newpost.lng = post.location.lng
            newpost.pic_url = post.url
            newpost.thumb_url = post._node['thumbnail_resources'][0]['src']
            newpost.location_text = post.location.name

            # some posts have multiple images so need to look for both types
            try:
                file_name = str(post.date).replace(' ', '_').replace(':','-') + '_UTC.jpg'
            except FileNotFoundError:
                file_name = str(post.date).replace(' ', '_').replace(':', '-') + '_UTC_1.jpg'
            # convert to thumb size
            size = (75, 75)
            with Image.open('andrew_vxx/' + file_name) as f:
                f.thumbnail(size)
                blob = BytesIO()
                f.save(blob, 'JPEG')
                newpost.thumb.save(file_name.replace('.jpg', '_thumb.jpg'), File(blob), save=True)

            file_name = str(post.date).replace(' ', '_').replace(':', '-') + '_UTC.json'
            with open('andrew_vxx/' + file_name) as f:
                # saving json file itself
                newpost.json_file.save(file_name, File(f), save=True)
            newpost.save()
            print('database updated')



