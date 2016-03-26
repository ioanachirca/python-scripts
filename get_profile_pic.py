#! /usr/bin/python
from urllib2 import urlopen, HTTPError
import sys
import json
import imghdr
import os
from PIL import Image
if len(sys.argv) == 1:
    print "Feed me a Github username"
    quit(-1)

username = str(sys.argv[1])
api_url = "https://api.github.com/users/"+username
try:
    data = urlopen(api_url)
except HTTPError as e:
    print "[API-ERROR] " + e.msg
    exit(-1)
json_dict = json.loads(data.read())
for key,val in json_dict.items():
    if "avatar" in key:
        avatar_key = key
pic_url = json_dict[str(avatar_key)]
picname = "avatar_" + username
try:
    image_data = urlopen(pic_url).read()
except Exception as e:
    print "[AVATAR-ERROR] " + e.message
    exit(-1)


with open(picname, "wb") as img:
    img.write(image_data)
image_type = imghdr.what(picname)
os.rename(picname, picname + '.' + image_type)
complete_picname = picname + "." + image_type
print username + "'s Github avatar has been downloaded."
img = Image.open(complete_picname)
img.show()
