# What is this
This is a Pastebin clone implemented using the Flask library with Python 3.7, and Vue.JS on the backend.

# Features
* Account Creation, Editing, Deletion
* Paste Submission, Editing, Deletion, Collaboration (although collaboration will be a while),
  Expiration, Protection (passwords, encryption)

# What is used here
-Bootstrap 4 using Creative Tim's BlackDashboard (https://www.creative-tim.com/product/black-dashboard)  
-Nucleo Icon Pack  
-SQLAlchemy  
-Vue.JS  
-Flask w/ Flask-Restful + Flask-SqlAlchemy + Flask-Wtforms + Wtforms-Json + Flask-JWT-Extended

# About the JWT implementations here...
If I ever get around to it, I'm probably going to migrate off JWTs and just use regular session
cookies for authentication. The JWT stuff in here is a mess, and while it may just be my
own follies with implementing them, I really think now that JWTs are just a terrible idea
for authentication/sessions. Especially after reading [this.](http://cryto.net/~joepie91/blog/2016/06/13/stop-using-jwt-for-sessions/)  
And from what I've seen a lot of other people are starting to agree that JWTs are terrible
and cookies should just be used as well.

# Client Setup
``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

# Preview
![alt text](https://i.imgur.com/GklVl2M.png)
