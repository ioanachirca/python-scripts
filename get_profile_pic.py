#! /usr/bin/python
from urllib2 import urlopen
import sys
import json

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
picname = username + "_gitpic"
with open(picname, "wb") as img:
    img.write(urlopen(pic_url).read())
print username + "'s Github avatar has been downloaded."