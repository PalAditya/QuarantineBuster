# Simple Instagram like App
Basically, a test project to brush up on my skills and compare various performances, primarily MySQL and server combination vs Firebase Realtime DB/Cloudstore , and hopefully Flask vs NodeJs/React combination in future

The Flask app needs a few configurations to run locally :
- Use **pip install -r requirements.txt**
- Create a new project at the Firebase [console](https://console.firebase.google.com). Note down the credentials and save the credentials file
- Use **set FLASK_APP=application.py** (Windows) and **export FLASK_APP=application.py** (Linux/MAC)
- Likewise, use **set/export GOOGLE_APPLICATION_CREDENTIALS=\<path-to-credentials-file>** as might be necessary.

More instructions coming soon!

## Features

- Signup/Login with hashed password
- Uploading images with image preview, text and description
- Viewing all uploaded images
- Global feed to see images from other users

## TODO

- Give users the ability to delete images and modify description
- Follow users and generate a custom feed out of them
- Favourite images and save them locally
- Hashtag/Title based search
- Revamping the UI (primarily introduce load on scroll)
- Reduce network requirements by loading in phases
- Use a caching layer (Memcached/Redis)
- Write a robust configuration file so that user doesn't need to manually configure the FireBase project
- Deploy on Heroku

## State of the project

I don't have much up right now, so have a look at the error page with the classic CS50 (The course which sparked my interest in Web Development) cat :smile:

![Error](https://user-images.githubusercontent.com/25523604/64475286-7802d400-d19e-11e9-8ddc-72da3565a085.PNG)
