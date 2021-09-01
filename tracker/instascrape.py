import instaloader, geopy
from .models import PostRecord, InstaPost
from random import uniform
from django.utils.timezone import make_aware
from django.core.files import File
from urllib.request import urlretrieve, urlcleanup
import mimetypes
import magic

# from credentials import *


def main():
    L = instaloader.Instaloader()
    L.login(USERNAME, PASSWORD)
    profile = instaloader.Profile.from_username(L.context, USERNAME)
    # Check VXX profile
    insta_posts = profile.get_posts()
    insta_check(insta_posts)
    # Check posts VXX profile tagged in
    tagged_insta_posts = profile.get_tagged_posts()
    insta_check(tagged_insta_posts)

# Function to check for and download new Instagram posts
def insta_check(posts):
    x = 0
    y = 0
    z = 0
    for post in posts:
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
                    print(
                        'ERROR! Post flagged as should be kept, but not in the database! Deleting PostRecord ID=' + str(
                            post.mediaid))
                    pr.delete()
                    print('Post record deleted. You should run instacrape again to save the post to the database!')
            except:
                # only stores posts in database which have a geolocation
                if post.location == None:
                    x += 1
                    if post.mediaid:
                        update_database(post)
                        newpostrecord = PostRecord()
                        newpostrecord.post_id = post.mediaid
                        newpostrecord.keep = True
                        newpostrecord.save()
                        print('post "' + str(post.mediaid) + '" does not have geolocation data. Storing in database. Manual action: If in Vietnam, add location. Else, add PostRecord set to False then delete InstaPost. x ' + str(x))
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
                        
                        # JSON structure of tagged posts requires slight modification from regular posts
                        if post._node['owner']['id'] != VXX_PROFILE_ID:
                            print('this tagged post came from user ID: ' + post._node['owner']['id'])
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


# Function to update the Django database
def update_database(post):
    newpost = InstaPost()
    try:
        # Check for identical geo coordinates
        x = InstaPost.objects.filter(lat=post.location.lat, lng=post.location.lng)
        # If an extant post has the same coordinates, adjust by random amount up to .005 so both markers visible on map
        if len(x) > 0:
            print('Identical geolocation found, adjusting...')
            newpost.lat = post.location.lat + uniform(-.004, .004)
            newpost.lng = post.location.lng + uniform(-.004, .004)
        # If geo coordinates unique, save unchanged
        else:
            print("Post coordinates unique, saving as is.")
            newpost.lat = post.location.lat
            newpost.lng = post.location.lng
        newpost.location_text = post.location.name
    except:
        pass
    newpost.post_id = post.mediaid
    newpost.date = make_aware(post.date)
    newpost.caption = post.caption
    # Change the URL if it's a video
    post._obtain_metadata()
    post_media_url = post.url
    if post._full_metadata_dict["is_video"]:
        post_media_url = post.video_url
    # Save post pic/video to server and store local URI to database
    try:
        mime = magic.Magic(mime=True) 
        tempname, _ = urlretrieve(post_media_url)
        mimes = mime.from_file(tempname)
        ext = mimetypes.guess_all_extensions(mimes)[0]
        newpost.pic_file.save("pic_file_%s_%s%s" % (newpost.date.year, newpost.post_id, ext), File(open(tempname, 'rb')))
    finally:
        urlcleanup()
    # Save post thumbnail to server and store local URI to database
    try:
        post_thumbnail_url = post._node['thumbnail_resources'][0]['src']
    except:
        try:
            post_thumbnail_url = post._node['thumbnail_src']
        except:
            print("couldn't get thumb file")
            print(post._node)
            exit()
    try:
        mime = magic.Magic(mime=True) 
        tempname, _ = urlretrieve(post_thumbnail_url)
        mimes = mime.from_file(tempname)
        ext = mimetypes.guess_all_extensions(mimes)[0]
        newpost.thumb_file.save("pic_thumbs_%s_%s%s" % (newpost.date.year, newpost.post_id, ext), File(open(tempname, 'rb')))
    finally:
        urlcleanup()
    newpost.uploader_name = post.owner_profile.full_name
    newpost.uploader_profile_url = "https://www.instagram.com/{}/".format(post.owner_profile.username)
    newpost.save()
    print('database updated')