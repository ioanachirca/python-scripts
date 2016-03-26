#! /usr/bin/python
from urllib2 import urlopen
import sys
import json
import imghdr
import os
from PIL import Image
if len(sys.argv) == 1:
    print "Feed me a Github username"
    quit()

username = str(sys.argv[1])
api_url = "https://api.github.com/users/"+username
data = urlopen(api_url)
json_dict = json.loads(data.read())
for key,val in json_dict.items():
    if "avatar" in key:
        avatar_key = key
pic_url = json_dict[str(avatar_key)]
picname = "avatar_" + username  
with open(picname, "wb") as img:
    img.write(urlopen(pic_url).read())
image_type = imghdr.what(picname)
os.rename(picname, picname + '.' + image_type)
complete_picname = picname + "." + image_type
print username + "'s Github avatar has been downloaded."
img = Image.open(complete_picname)
img.show()
