import requests
import firebase_admin
from firebase_admin import credentials
from google.cloud import storage
import json
import datetime

def getImages(bucket, next_path, ref):
    contents = json.loads(requests.get(ref + "user_data/" + next_path + ".json").text)
    contents2 = json.loads(requests.get(ref + "user_liked_images/" + next_path + ".json").text)
    liked_map = {"Heh"}
    print(contents2)
    if contents2 is not None:
        for content in contents2:
            try:
                #print(contents2[content]["impath"])
                liked_map.add(contents2[content]["impath"])
            except:
                continue
    counter = 0
    #print(liked_map)
    if contents is not None:
        new_contents = []
        for content in contents:
            try:
                if contents[content] == "datacount":
                    continue
                blob = bucket.blob(contents[content]["impath"])
                temp = {}
                temp["desc"] = contents[content]["desc"]
                temp["heading"] = contents[content]["heading"]
                temp["impath"] = blob.generate_signed_url(datetime.timedelta(seconds=3600), method='GET')
                temp["index"] = counter
                temp["key"] = content
                temp["user"] = next_path
                if contents[content]["impath"] in liked_map:
                    temp["liked"] = 1
                else:
                    temp["liked"] = 0
                counter = counter + 1
                new_contents.append(temp)
            except Exception as e:
                print(e)
                continue
        #print(new_contents)
        contents = new_contents
    else:
        contents = []

    return contents