import instaloader, geopy
from .models import PostRecord, InstaPost
from random import uniform
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from . import readgmail


def main():
    # Enter Instagram account info here
    username = ""
    password = ""
    # Creates authenticated session
    session = instaloader.Instaloader(compress_json=False)
    # Attempts to log into Instagram.
    try:
        session.login(username, password)
    # If login triggers "suspicious login attempt" from Instagram, calls function to overcome two-factor authentication
    except instaloader.ConnectionException as err:
        insta_checkpoint(err)
    # Creates a profile object that will be used to access all Instagram posts
    profile = instaloader.Profile.from_username(session.context, 'vong_xe_xanh')
    insta_check(profile)
    insta_tagged_check(profile)


# Function to check for and download new Instagram posts
def insta_check(profile):
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
                    print(
                        'ERROR! Post flagged as should be kept, but not in the database! Deleting PostRecord ID=' + str(
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


# Function to check for and download new tagged Instagram posts
def insta_tagged_check(profile):
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
                    print(
                        'ERROR! Post flagged as should be kept, but not in the database! Deleting PostRecord ID=' + str(
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
                        # json structure of tagged posts requires slight modification from regular posts
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


# Function to overcome the two-factor authentication required by Instagram when "suspicious login attempt" is generated
def insta_checkpoint(err):
    check_url = err.args[0][50:-38]
    # Sets Selenium to run in background
    ops = Options()
    ops.add_argument('-headless')
    ops.add_argument("--disable-dev-shm-usage")
    ops.add_argument("--no-sandbox")
    # Initiates Instagram checkpoint confirmation code
    driver = webdriver.Firefox(firefox_options=ops)
    driver.get(check_url)
    driver.find_element_by_xpath("//*[contains(text(), 'Send Security Code')]").click()
    time.sleep(2)  # Sleeps two seconds to give Instagram time to send email to inbox
    # Gets security code from Gmail API
    code = readgmail.main()
    # Inputs confirmation code into Instagram browser to complete authentication process
    driver.find_element_by_name('security_code').send_keys(code)
    driver.find_element_by_xpath("//button[contains(text(), 'Submit')]").click()
    time.sleep(1)
    driver.close()
    print('Instagram security check completed')
