from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
import sqlalchemy.orm
from numpy import average
from flask import current_app as app
from application.models import Song, Album, User, Rating, Songsearch, Playlist
from .database import db

#Common inputs:
genre_list = Song.query.with_entities(Song.genre).distinct()
song_list = Song.query.filter().all()
album_list = Album.query.with_entities(Album.aname).distinct()
recommend_list = Song.query.join(Song.rateR).group_by(Song.song_id).order_by(db.func.sum(Rating.rate).desc()).all()
sg = Song()
alb = Album()
pl = Playlist()
rt = Rating()
user_count = User.query.count()
creator_count = User.query.filter_by(user_type = "CRT").count()
song_count = Song.query.count()
album_count = Album.query.with_entities(Album.aname).distinct().count()
genre_count = Song.query.with_entities(Song.genre).distinct().count()
slist=[]
for song in song_list:
    if song not in recommend_list:
        slist.append(song)

#controllers
#Home page
@app.route("/", methods=["GET", "POST"])
def dashboard():
    return render_template("welcome.html")

#Login page
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        password = request.form['password']
        user_name = request.form['username']
        enter_user = User.query.filter_by(username=user_name,passw=password).first()
        if enter_user:
            uid = enter_user.user_id
            return redirect(url_for('userpage',uid=uid)) 
        else:
            return redirect("/login")

#register page
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        email = request.form['email']
        password = request.form['password']
        user_name = request.form['username']


        new_user = User(username=user_name, passw=password, email_id=email,user_type="USER")
        db.session.add(new_user)
        db.session.commit()
        uid = new_user.user_id
        return redirect(url_for('userpage',uid=uid))

#Returning main user page
@app.route("/login/<int:uid>/user_page",methods=["GET","POST"])
def userpage(uid):
    his_plist = Playlist.query.filter_by(user_id=uid).with_entities(Playlist.p_name).distinct()
    return render_template("song_page.html",sg=sg,alb=alb,plist=his_plist,genre_list=genre_list,uid=uid,rlist=recommend_list,slist=slist)

#Admin dashboard
@app.route("/admin_dashboard", methods=["GET","POST"])
def admin_dash():
    if request.method == "GET":
        return render_template("admin_login.html")
    else:
        password = request.form['password']
        user_name = request.form['username']

        check_admin = User.query.filter_by(username=user_name,passw=password).first()
        if check_admin and check_admin.user_type == 'ADMIN':
            return render_template("admin_dash_try.html",user_count=user_count,creator_count=creator_count,song_count=song_count,album_count=album_count,genre_count=genre_count,slist=recommend_list)
        else:
            return redirect("/")

#Admin dashboard : TRACKS
@app.route("/tracks", methods=["GET","POST"])
def tracks():
    if request.method == "GET":
        return render_template("tracks.html",song_list=song_list,genre_list=genre_list,sg=sg)

#Showing lyrics
@app.route("/show_lyrics", methods=["GET","POST"])
def show():
    if request.method == "POST":
        sid = request.form['sid']
        song = Song.query.filter_by(song_id=sid).first()
        return render_template("Lyrics.html",song = song)

#deleting the song
@app.route("/del_song/<int:uid>" , methods=["GET","POST"])
def del_song(uid):
    if request.method == "POST":
        sid = request.form['sid']
        song = Song.query.filter_by(song_id=sid).first()
        alsong = Album.query.filter_by(song_id = sid).first()
        rsongs = Rating.query.filter_by(song_id=sid).all()
        for k in rsongs:
            db.session.delete(k)
        db.session.delete(song)
        if alsong:
            db.session.delete(alsong)
        db.session.commit()
        if uid!=0:
            return redirect(url_for("registor_crt",uid=uid))
        else:
            return redirect("/tracks")

#ALBUMS
@app.route("/albums",methods=["GET"])
def albums():
    if request.method == "GET":
        return render_template("albums.html",song_list=song_list,album_list=album_list,alb=alb,sg=sg)

#Creating playlists
@app.route("/create_plist/<int:uid>",methods=["GET","POST"])
def crt_plist(uid):
    if request.method == "GET":
        return render_template("plist.html",sg=sg,uid=uid)
    else:
        song_to_add = request.form.getlist('addsid')
        pname = request.form['pname']
        for k in song_to_add:
            new_pl = Playlist(user_id=uid,p_name=pname,song_id=k)
            db.session.add(new_pl)
        db.session.commit()
        return redirect(url_for('userpage',uid=uid))

#showing tracks for playlists
@app.route("/show_tracks",methods=["POST"])
def show_tracks():
    playlist_name = request.form['pname']
    return render_template("pl_tracks.html",playlist_name=playlist_name,pl=pl,sg=sg)

#creator registor
@app.route("/crt_reg/<int:uid>",methods=["GET","POST"])
def registor_crt(uid):
    if request.method == "GET":
        user = User.query.filter_by(user_id=uid).first()
        if user.user_type == "USER":
            return render_template("creator_reg.html",uid=uid)
        else:
            u = User.query.filter_by(user_id=uid).first()
            singer = u.username
            sids = Song.query.filter_by(singer=singer).with_entities(Song.song_id).all()
            rate=[]
            for (i,) in sids:
                for (j,) in Rating.query.filter_by(song_id=i).with_entities(Rating.rate).all():
                    rate.append(j)
            avg_rt = round(average(rate),1)
            total_album= Song.query.join(Song.albR).filter(Song.singer==singer).with_entities(Album.aname).count()
            return render_template("creator_dash.html",uid=uid,sg=sg,alb=alb,rt=rt,singer=singer,avg_rt=avg_rt,ta=total_album)
    else:
        u = User.query.filter_by(user_id=uid).first()
        print(u.user_type)
        u.user_type="CRT"
        db.session.add(u)
        db.session.commit()
        print(u.user_type)
        singer = u.username
        sids = Song.query.filter_by(singer=singer).with_entities(Song.song_id).all()
        rate=[]
        for (i,) in sids:
            for (j,) in Rating.query.filter_by(song_id=i).with_entities(Rating.rate).all():
                rate.append(j)
        avg_rt = round(average(rate),1)
        total_album=Song.query.join(Song.albR).filter(Song.singer==singer).with_entities(Album.aname).count()
        return render_template("creator_dash.html",uid=uid,sg=sg,alb=alb,rt=rt,singer=singer,avg_rt=avg_rt,ta=total_album)

#Uploading the song
@app.route("/upload_song/<int:uid>",methods=["GET","POST"])
def upload(uid):
    if request.method == "GET":
        return render_template("upload.html",uid=uid)
    else:
        title = request.form['title']
        singer = request.form['singer']
        date = request.form['date']
        lyrics = request.form['lyrics']
        album = request.form['album']
        genre = request.form['genre']

        new_song = Song(name=title,lyrics=lyrics,date_cr=date,genre=genre,singer=singer)
        db.session.add(new_song)
        db.session.commit()

        sid = new_song.song_id
        if album:
            new_song_album = Album(aname=album,song_id=sid)
            db.session.add(new_song_album)
            db.session.commit()
        return redirect(url_for('registor_crt',uid=uid))

#edit the uploaded song
@app.route("/edit_song/<int:sid>",methods=["GET","POST"])
def edit(sid):
    if request.method == "GET":
        song = Song.query.filter_by(song_id=sid).first()
        alsong = Album.query.filter_by(song_id=sid).first()
        title = song.name
        singer = song.singer
        date = song.date_cr
        lyrics = song.lyrics
        genre = song.genre
        if alsong:
            album = alsong.aname
        else:
            album = ""
        return render_template("editSong.html",sid=sid,title=title,singer=singer,date=date,album=album,lyrics=lyrics,genre=genre)
    else:
        old_song = Song.query.filter_by(song_id=sid).first()
        old_al = Album.query.filter_by(song_id = sid).first()
        old_song.name = request.form['title']
        old_song.singer = request.form['singer']
        old_song.date_cr = request.form['date']
        old_song.lyrics = request.form['lyrics']
        old_song.genre = request.form['genre']
        album = request.form['album']

        db.session.add(old_song)
        db.session.commit()

        uid = User.query.filter_by(username=old_song.singer).with_entities(User.user_id).first()[0]
        if album != old_al.aname:
            db.session.delete(old_al)
            db.session.commit()

            new_song_album = Album(aname=album,song_id=sid)
            db.session.add(new_song_album)
            db.session.commit()
        return redirect(url_for('registor_crt',uid=uid))

#Rating the song
@app.route("/rating/<int:song_id>/<int:song_rate>",methods=["GET"])
def rating(song_id,song_rate):
    new = Rating(song_id=song_id,rate=song_rate)
    db.session.add(new)
    db.session.commit()
    return "OK", 200

#Searching the songs
@app.route("/search",methods=["GET"])
def search():
    q = request.args.get('q')
    print(q)
    results = Songsearch.query.filter(Songsearch.name.op("LIKE")(q) | Songsearch.lyrics.op("LIKE")(q) | Songsearch.genre.op("LIKE")(q) | Songsearch.singer.op("LIKE")(q)).all()
    print(results)
    return render_template("results.html",q=q,results=results)

#LOGOUT
@app.route("/logout")
def logout():
    return redirect("/")