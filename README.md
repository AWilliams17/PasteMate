I have no idea when/if this will ever be finished.
# What is this
This is a Pastebin clone implemented using the Flask library in Python. The version of Python used for this project is 3.7 (first time writing in 3.7
as well, woo hoo! Happy new-version!)

This is also my first time using Vue.JS, and making a Single Page Application.

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

# State of the code
The server part of this project is okay as far as I can see, but the client is a bit messy right now due to state issues.  
I'm going to be doing some revisions to implement VueX (https://github.com/vuejs/vuex) which is probably going to be the  
very next thing I do before moving onto the actual functionality of the pastes.

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
![alt text](https://i.imgur.com/0bDqDTi.png)