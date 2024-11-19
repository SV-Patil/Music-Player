from .database import db

#defining data models
class Song(db.Model):
    __tablename__ = 'song'
    song_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lyrics = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    date_cr = db.Column(db.String, nullable=False)
    singer = db.Column(db.String,nullable=False)
    
    rateR = db.relationship("Rating",backref="Rating.song_id")
    albR = db.relationship("Album",backref="Album.song_id")

class Album(db.Model):
    __tablename__ = 'album'
    album_id = db.Column(db.Integer ,primary_key=True)
    aname = db.Column(db.String, nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey(Song.song_id))
    
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    passw = db.Column(db.String, nullable=False)
    user_type = db.Column(db.String, nullable=False)
    email_id = db.Column(db.String, nullable=False, unique=True)

class Playlist(db.Model):
    __tablename__ = 'playlist'
    user_id = db.Column(db.Integer,db.ForeignKey(User.user_id),primary_key=True)
    p_name = db.Column(db.String,nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey(Song.song_id),primary_key=True)

class Rating(db.Model):
    __tablename__ = 'rating'
    temp_id = db.Column(db.Integer,primary_key=True)
    song_id = db.Column(db.Integer,db.ForeignKey(Song.song_id))
    rate = db.Column(db.Integer,default=0)

#virtual table
class Songsearch(db.Model):
    __tablename__ = 'songsearch'
    rowid = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    lyrics = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    singer = db.Column(db.String,nullable=False)