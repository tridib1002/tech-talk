from flask import Flask, render_template , session , request , redirect , url_for , g , jsonify ,json
import dbHandler # importing 'dbHandler.py' file.
from werkzeug import secure_filename # secure_filename will be used for renaming the upload file.
import os
from PIL import Image # PIL is used for image resizing
import time
import random

app = Flask(__name__)

app.secret_key = os.urandom(24) # This secret_key is used for session control.
# user could look at the contents of the cookie but not modify it, unless they know the secret key used for signing.

UPLOAD_FOLDER = 'static/img/' # Uploaded image will be stored here.

@app.route('/') # when users will visit hope url, below code will be executed.
def home_page():
    counter = 0
    blogtag = 'all'
    username = 'none'

    blog_data = dbHandler.retrieve_blog_data(counter,blogtag,username) # Check 'dbHandler.py' file

    my_data = {}

    for data in blog_data: # looping through blog_data for getting individual blogs.
        my_data.update({'username' + str(counter) : data[0], 
        'blogname'  + str(counter) : data[1], 
        'blogtag'  + str(counter) : data[2], 
        'image'  + str(counter) : data[3], 
        'datestamp'  + str(counter) : data[4], 
        'blog'  + str(counter) : data[5]})
        counter += 1

    if g.user: # check before_request
        user = session['user'] # It returns the name of user of the session.
        return render_template('users.html', user = user, data = my_data)
    else:
        return render_template('main.html', data = my_data)

# This function will be executed before every request comes from client.
@app.before_request
def before_request():
    # g is a data shared between different parts of the code base within one request 
    # data set on g is only available for the lifetime of request. 
    # once the request is done and sent out to the client, g is cleared.
    g.user = None 
    if 'user' in session: 
        g.user = session['user']

@app.route('/SignUp', methods = ['POST', 'GET'])
def SignUp():
    if request.method == 'POST':
        session.pop('user',None) # this function clears the session of the current user.
        # request.form[''] is used to handlinng the post request. It will fetch the data form name value pair.
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        users = dbHandler.retrieveUsers()
        for user in users:
            if username == user[0]:
                return redirect(url_for('home_page'))
        
        dbHandler.insertUser(username, password, email)

        users = dbHandler.retrieveUsers()
        for user in users:
            if username == user[0] and password == user[1]:
                session['user'] = username
                return redirect(url_for('home_page', user = username))
    else:
        return redirect(url_for('home_page'))


@app.route('/LogIn', methods = ['POST', 'GET'])
def LogIn():
    if request.method == 'POST':
        session.pop('user',None) # this function clears the session of the current user.
        # request.form[''] is used to handlinng the post request. It will fetch the data form name value pair.
        username = request.form['username'] 
        password = request.form['password']
        users = dbHandler.retrieveUsers()
        for user in users:
            if username == user[0] and password == user[1]:
                session['user'] = username # Setting the user session with the username. 
                # In the browser a cookie will be generated with the 'app.secret_key'.
                return redirect(url_for('home_page', user = username))   
        else:
            return 'notFound'

@app.route('/fetchBlog', methods = ['GET','POST'])
def fetchBlog():
    # request.form[''] is used to handlinng the post request. It will fetch the data form name value pair.
    counter = int(request.form['val'])
    blogtag = request.form['blogtag']
    username = request.form['userName']

    blog_data = dbHandler.retrieve_blog_data(counter,blogtag,username) # Check 'dbHandler.py' file

    my_data = {}

    for data in blog_data:
        my_data.update({'username' + str(counter) : data[0], 
        'blogname'  + str(counter) : data[1], 
        'blogtag'  + str(counter) : data[2], 
        'image'  + str(counter) : data[3], 
        'datestamp'  + str(counter) : data[4], 
        'blog'  + str(counter) : data[5]})
        counter += 1
                
    return jsonify(my_data) # returning my data dictionary as a JSON string.
    
@app.route('/logout')
def dorpsession():
    session.pop('user',None) # this function clears the session of the current user.
    return redirect(url_for('home_page'))

# This function will be used to check if a username is available or not.
@app.route('/checkUser', methods = ['POST', 'GET'])
def checkUser():
    if request.method == 'POST':
        newUser = request.form['newUser']
        users = dbHandler.retrieveUsers()
        for user in users:
            if newUser == user[0]:
                return 'exists'
        return 'notExists'

# Return the blogtemplate by which a user can write and post their blogs.
@app.route('/addblog') 
def addblog():
    if g.user:
        user = session['user']
        return render_template('add_blog.html', user = user)
    else:
        return render_template("main.html")

ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg',\
    'JPEG', 'jpe', 'JPE', 'bmp', 'BMP', 'svg' 'SVG'])

# This function will check wheather a 'photo' submitted by user is allowed to server or not.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# This function is used to store blogdata to the DataBase which is submitted by user.
@app.route("/upload", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':    
        username = session['user']
        blogname = request.form['blogname']
        blogtag = request.form['blogtag']
        blog = request.form['blog']

        file = request.files['photo']
        filename = secure_filename(file.filename) # secure_filename will be used for renaming the upload file.
        if filename == "":
            image = "NA" # If there is no image submitted by user image name will be stored "NA"
        else:
            if allowed_file(file.filename) == False:
                return 'Unaccepted file format for image' # returning with a text message if file is unaccepted by server
            elif file and allowed_file(file.filename):  
                image = photo_upload(filename,file) # Check 'photo_upload' function.

        dbHandler.blog_data_entry(username, blogname , blogtag , image , blog) # Updating blogdata to database.

        return redirect(url_for('home_page', user = username)) 

    return home_page()

def photo_upload(filename,file):
    name , extension = filename.rsplit('.') # Splitting the name and extension of the photo.
    new_name =  session['user'] + '_' + str(int(time.time())) # Setting the name of the uploaded image as unix timestamp.
    filename_mod = new_name +'.'+ extension
    file.save(os.path.join(UPLOAD_FOLDER, filename_mod)) # Saving the photo to the database with New Name.
    photo_resize(UPLOAD_FOLDER,filename_mod) # Resizing the photo / Check 'photo_resize' function
    return filename_mod

def photo_resize(UPLOAD_FOLDER,filename_mod):
    # image function is imported from 'PILLOW' library.
    image = Image.open(UPLOAD_FOLDER+filename_mod)
    image.thumbnail( (250,250) ) # Resizing the image with pixel size of 250X250
    image.save(UPLOAD_FOLDER+filename_mod)
    

if __name__ == "__main__":
    app.run(debug = 'True', host="0.0.0.0")