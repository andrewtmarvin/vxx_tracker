from .models import InstaPost, PostRecord
import requests, threading, fleep


# Utilizes multithreading to check for dead url links and delete corresponding objects
def dead_url_check():
    url_list = []
    for post in InstaPost.objects.all():
        url_list.append(post)

    def thread():
        while url_list:
            post = url_list.pop()
            # Tries to open each Instagram post picture and thumbnail picture
            try:
                # Main image
                main_cont = requests.get(post.pic_url).content
                main_kind = fleep.get(main_cont)
                # Thumbnail image
                thumb_cont = requests.get(post.thumb_url).content
                thumb_kind = fleep.get(thumb_cont)
                # If the URL leads to a media file, do nothing
                if main_kind.type and thumb_kind.type:
                    print(threading.current_thread().name + ': both ' + str(main_kind.type) + ' and ' +
                          str(thumb_kind.type) + ' URLs live for post in ' + post.location_text)
                # If the URL does not lead to a media file, deletes posts so that it can be refreshed by instacrape.py
                else:
                    print(threading.current_thread().name + ': dead url, deleting post and post record for id: ' + str(
                        post.post_id) + str(post.location_text))
                    post.delete()
                    try:
                        rec = PostRecord.objects.get(post_id=post.post_id)
                        rec.delete()
                    except:
                        print("error deleting post record.")
            except:
                print('error')

    t1 = threading.Thread(target=thread, name='thread 1')
    t2 = threading.Thread(target=thread, name='thread 2')
    t3 = threading.Thread(target=thread, name='thread 3')
    t4 = threading.Thread(target=thread, name='thread 4')
    t5 = threading.Thread(target=thread, name='thread 5')

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()


# _____________________------------------------------_________________________
# Original script that did not utilize multithreading. Might be needed when deploying online.
# _____________________------------------------------_________________________
# from .models import InstaPost
# from PIL import Image
# from io import BytesIO
# import requests
#
# # function to check for dead url links and delete corresponding objects here
# def dead_url_check():
#     for post in InstaPost.objects.all():
#
#         # Tries to open each Instagram post picture and thumbnail picture
#         try:
#             cont = requests.get(post.pic_url).content
#             Image.open(BytesIO(cont))
#             cont = requests.get(post.thumb_url).content
#             Image.open(BytesIO(cont))
#             print('both pic and thumb URLs live for post in ' + post.location_text)
#
#         # If the Instagram picture link is dead, deletes post so that it can be refreshed
#         except:
#             print('dead url, deleting post...')
#             print(post.id)
#             post.delete()
