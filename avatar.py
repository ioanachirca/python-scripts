"""Module for downloading and showing github avatars
"""
from urllib2 import urlopen, HTTPError
import json
import imghdr
import os
from PIL import Image


def show(username):
    """ Shows the avatar of a user
    """
    api_url = "https://api.github.com/users/"+username

    try:
        data = urlopen(api_url)
    except HTTPError as err:
        print "[API-ERROR] " + err.msg
        exit(-1)

    json_dict = json.loads(data.read())
    for key in json_dict:
        if "avatar" in key:
            avatar_key = key
    pic_url = json_dict[str(avatar_key)]

    try:
        image_data = urlopen(pic_url).read()
    except Exception as err:
        print "[AVATAR-ERROR] " + err.message
        exit(-1)

    picname = "avatar_" + username
    with open(picname, "wb") as img:
        img.write(image_data)

    image_type = imghdr.what(picname)
    complete_picname = picname + "." + image_type
    os.rename(picname, complete_picname)

    print username + "'s Github avatar has been downloaded."

    img = Image.open(complete_picname)
    img.show()
