# Music-Player
Web Development
## PROJECT DESCRIPTION
This project is Music streaming platform for playing the music where user can register as a new user and play songs, read lyrics, create playlists and rate the songs. User can then register as a creator for uploading the music on this app. Admins are another type of users who have control over the app and its data. They can delete/flag the song which is not appropriate according to policies.

## TECHNOLOGIES USED
*	Flask – used for backend code of application
*	Jinja2 templates and CSS for HTML styling
*	SQLite and SQLAlchemy for data storage of the application

## ARCHITECTURE AND FEATURES
The project is created using the Model-View-Controller (MVC) architecture where controllers handle the routing and logic part of application, view handles the templates for display as well as styling of app and model is used for database. 
This application includes features implemented,
1. New user can register and existing user can login in the application.
2.	Once the user is logged in, he/she can play songs, view lyrics, create customized playlists and rate any song. He/she can search any song by its name or genre or lyrics or singer.
3.	Normal user can register himself as creator who can upload any song, delete any of his uploaded song or edit the uploaded song, assign it to some album.
4.	Admin login: admin registration is done in SQL database. Admin login form link is given on main page and after logging in admin can see total songs, creators, users, albums. Admin can view lyrics of songs and can delete any song.
5.	Creator also have all features of normal users of playing songs and rating them etc.
6.	User can see songs recommended songs on the basis of song rating.
7.	User can logout from the application.

## DB SCHEMA DESIGN
The database is created and designed to store the user information, song information, album details, playlist and rating update. The database contains tables created using SQLAlchemy ORM. The schema includes:
*	User: stores the user information like user id, username, password and user type to differentiate between normal user, creator and admin.
*	Song: stores the details of every uploaded song such as song name, song id, singer, genre, lyrics and date at which created.
*	Album: stores the information of albums and songs in it.
*	Rating: it contains the ratings given to each song.
*	Playlist: stores the information of playlist name, user id of the user who created it and song.
