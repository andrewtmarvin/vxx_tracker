import instaloader, geopy, requests
from .models import PostRecord, InstaPost, DayRoute
from random import uniform
from PIL import Image
from io import BytesIO

def main():
    # enter Instagram account info here
    username = ""
    password = ""

    # database check and update steps
    session = insta_login(username, password)
    dead_url_check()
    insta_check(session)
    insta_tagged_check(session)


# function to authenticate session
def insta_login(username, password):
    session = instaloader.Instaloader(compress_json=False)
    session.login(username, password)
    return session


# function to check for dead url links and delete corresponding objects here
def dead_url_check():
    for post in InstaPost.objects.all():
        try:
            cont = requests.get(post.pic_url).content
            Image.open(BytesIO(cont))
            cont = requests.get(post.thumb_url).content
            Image.open(BytesIO(cont))
            print('both pic and thumb URLs live for post in ' + post.location_text)
        except:
            print('dead url, deleting post...')
            print(post.id)
            post.delete()


# function to check for and download new posts
def insta_check(session):
    profile = instaloader.Profile.from_username(session.context, 'vong_xe_xanh')
    x = 0
    y = 0
    z = 0
    for post in profile.get_posts():
        try:
            p = InstaPost.objects.get(post_id=post.mediaid)
            print('post ID: ' + str(post.mediaid) + ' already in database')
        except:
            # if not in the database, check if in the records
            try:
                pr = PostRecord.objects.get(post_id=post.mediaid)
                if pr.keep == False:
                    print('post ID: ' + str(post.mediaid) + ' should not be kept')
                else:
                    print('ERROR! Post flagged as should be kept, but not in the database! Deleting PostRecord ID=' + str(
                        post.mediaid))
                    pr.delete()
                    print('Post record deleted. You should run instacrape again to save the post to the database!')
            except:
                # only stores posts in database which have a geolocation
                if post.location == None:
                    newpostrecord = PostRecord()
                    newpostrecord.post_id = post.mediaid
                    newpostrecord.keep = False
                    newpostrecord.save()
                    if post.caption:
                        x += 1
                        print('post "' + post.caption.rstrip()[:10] + '" does not have geolocation data. x ' + str(x))
                else:
                    # only stores posts if location is in Vietnam
                    p = geopy.point.Point(post.location.lat, post.location.lng)
                    geolocator = geopy.Nominatim(user_agent='macekid421')
                    try:
                        location = geolocator.reverse(p, timeout=15)
                    except geopy.exc.GeocoderTimedOut as err:
                        print("Error: " + str(err))
                    if location.raw['address']['country_code'] == 'vn':
                        y += 1
                        print("in " + location.raw['address']['country'], 'saving to database. x ' + str(y))
                        update_database(post)
                        newpostrecord = PostRecord()
                        newpostrecord.post_id = post.mediaid
                        newpostrecord.keep = True
                        newpostrecord.save()
                    else:
                        z += 1
                        print("outside of vietnam, database not updated. x " + str(z))
                        print(location.raw['address']['country_code'])
                        newpostrecord = PostRecord()
                        newpostrecord.post_id = post.mediaid
                        newpostrecord.keep = False
                        newpostrecord.save()

# function to check for and download new tagged posts
def insta_tagged_check(session):
    profile = instaloader.Profile.from_username(session.context, 'vong_xe_xanh')
    x = 0
    y = 0
    z = 0
    for post in profile.get_tagged_posts():
        try:
            p = InstaPost.objects.get(post_id=post.mediaid)
            print('post ID: ' + str(post.mediaid) + ' already in database')
        except:
            # if not in the database, check if in the records
            try:
                pr = PostRecord.objects.get(post_id=post.mediaid)
                if pr.keep == False:
                    print('post ID: ' + str(post.mediaid) + ' should not be kept')
                else:
                    print('ERROR! Post flagged as should be kept, but not in the database! Deleting PostRecord ID=' + str(
                        post.mediaid))
                    pr.delete()
                    print('Post record deleted. You should run instacrape again to save the post to the database!')
            except:
                # only stores posts in database which have a geolocation
                if post.location == None:
                    newpostrecord = PostRecord()
                    newpostrecord.post_id = post.mediaid
                    newpostrecord.keep = False
                    newpostrecord.save()
                    if post.caption:
                        x += 1
                        print('post "' + post.caption.rstrip()[:10] + '" does not have geolocation data. x ' + str(x))
                else:
                    # only stores posts if location is in Vietnam
                    p = geopy.point.Point(post.location.lat, post.location.lng)
                    geolocator = geopy.Nominatim(user_agent='macekid421')
                    try:
                        location = geolocator.reverse(p, timeout=15)
                    except geopy.exc.GeocoderTimedOut as err:
                        print("Error: " + str(err))

                    if location.raw['address']['country_code'] == 'vn':
                        y += 1
                        print("in " + location.raw['address']['country'], 'saving to database. x ' + str(y))
                        # json structure of tagged posts require slight modification
                        post._node.update({'thumbnail_resources': {0: {'src': post._node['thumbnail_src']}}})

                        update_database(post)
                        newpostrecord = PostRecord()
                        newpostrecord.post_id = post.mediaid
                        newpostrecord.keep = True
                        newpostrecord.save()
                    else:
                        z += 1
                        print("outside of vietnam, database not updated. x " + str(z))
                        print(location.raw['address']['country_code'])
                        newpostrecord = PostRecord()
                        newpostrecord.post_id = post.mediaid
                        newpostrecord.keep = False
                        newpostrecord.save()


def update_database(post):
    newpost = InstaPost()

    # Check for idential geocoordinates
    x = InstaPost.objects.filter(lat=post.location.lat, lng=post.location.lng)
    # If an extant post has the same coordinates, adjust by random amount up to .005 so both markers visible
    if len(x) > 0:
        print('Identical geolocation found, adjusting...')
        newpost.lat = post.location.lat + uniform(-.004, .004)
        newpost.lng = post.location.lng + uniform(-.004, .004)
    # If geocoordinates unique, save unchanged
    else:
        print("Post coordinates unique, saving as is.")
        newpost.lat = post.location.lat
        newpost.lng = post.location.lng
    newpost.post_id = post.mediaid
    newpost.date = post.date
    newpost.caption = post.caption
    newpost.location_text = post.location.name

    # Change the URL if it's a video
    if post._full_metadata_dict["is_video"]:
        newpost.pic_url = post.video_url
    else:
        newpost.pic_url = post.url
    newpost.thumb_url = post._node['thumbnail_resources'][0]['src']
    newpost.uploader_name = post.owner_profile.full_name
    newpost.uploader_profile_url = "https://www.instagram.com/{}/".format(post.owner_profile.username)
    newpost.save()
    print('database updated')




