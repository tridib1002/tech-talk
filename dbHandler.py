import sqlite3 as sql
import time
import datetime

DATABASE = 'tech_talk.db'

# This function is used to insert 'User Details' to the Data Base.
def insertUser(username,password,email):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password,email) VALUES (?,?,?)", (username,password,email))
    con.commit()
    con.close()

# This function is used to retrieve 'User Details' from the Data Base.
def retrieveUsers():
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchall()
    con.close()
    return users

# This function will insert 'Blog Data' to the Data Base.
def blog_data_entry(username,blogname,blogtag,image,blog):
    unix = int(time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO blogdata(username,blogname,blogtag,image,datestamp,unix,blog) \
        VALUES (?,?,?,?,?,?,?)", (username,blogname,blogtag,image,date,unix,blog))
    con.commit()
    con.close()

# This function will retrieve 'Blog Data' from the Data Base.
def retrieve_blog_data(counter,blogtag,username):
    con = sql.connect(DATABASE)
    cur = con.cursor()

    if blogtag == 'all':
        blogtag = "%%"

    if username == 'none':
        username = "%%"

    LIMIT = 3
    OFFSET = counter

    cur.execute("SELECT username,blogname,blogtag,\
        image,datestamp, blog FROM blogdata \
        WHERE blogtag LIKE ? and username LIKE ? ORDER BY unix DESC LIMIT ? OFFSET ? ",(blogtag, username, LIMIT , OFFSET))
    data = cur.fetchall()
    con.close()
    return data
