# Music-Player
Web Development
## PROJECT DESCRIPTION
This project is Music streaming platform for playing the music where user can register as a new user and play songs, read lyrics, create playlists and rate the songs. User can then register as a creator for uploading the music on this app. Admins are another type of users who have control over the app and its data. They can delete/flag the song which is not appropriate according to policies.

## TECHNOLOGIES USED
*	Flask – used for backend code of application
*	Jinja2 templates and CSS for HTML styling
*	SQLite and SQLAlchemy for data storage of the application

## ARCHITECTURE AND FEATURES
The project is created using the Model-View-Controller (MVC) architecture where controllers handle the routing and logic part of the application, view handles the templates to display as well as styling of the app and model is used for the database. 
This application includes features such as,
1. New user can register and existing user can login in the application.
2.	Once the user is logged in, he/she can play the songs, view lyrics, create the customized playlists and rate any song. He/she can search any song by its name or genre or lyrics or singer.
3.	A Normal user can register himself as a creator who can upload a song, delete any of his uploaded song or edit the uploaded song and assign it to some album.
4.	Admin login: admin registration is done in SQL database. Admin login link is given on the main page and after logging in, admin can see total songs, creators, users, albums. Admin can view lyrics of songs and can delete any song.
5.	User gets song recommendations on the basis of rating.
6.	User can logout from the application.

## DB SCHEMA DESIGN
The database is created and designed to store the user information, song information, album details, playlist and rating update. The database contains tables created using SQLAlchemy ORM. The schema includes:
*	User: stores the user information like user id, username, password and user type to differentiate between normal user, creator and admin.
*	Song: stores the details of every uploaded song such as song name, song id, singer, genre, lyrics and date on which it is created.
*	Album: stores the information of albums and songs in it.
*	Rating: it contains the ratings given to each song.
*	Playlist: stores the information of playlist name, user id of the user who created it and songs in it.
