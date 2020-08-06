import requests
import firebase_admin
from firebase_admin import credentials
from google.cloud import storage
import json
import datetime

def getImages(bucket, next_path, ref):
    contents = json.loads(requests.get(ref + "user_data/" + next_path + ".json").text)
    print(contents)
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
                new_contents.append(temp)
            except Exception as e:
                print(e)
                continue
        print(new_contents)
        contents = new_contents
    else:
        contents = []

    return contents