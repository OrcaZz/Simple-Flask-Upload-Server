'''
Andrew Martin
Simple Upload Server
'''

import os
from flask import Flask, request, redirect, flash, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/")
def HomePage():
    
    ''' Renders home page '''
    
    return render_template("homePage.html")

@app.route("/upload", methods = ['GET', 'POST'])
def UploadPage():
    
    ''' Handles file uploading and redirects back to empty upload page '''
    
    if request.method == 'POST':
        
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        
        return redirect("/upload")
        
    return render_template("upload.html")

@app.route("/upload/<name>")
def GetFileByURL(name):
    
    '''Serves file directly from directory by URL'''
    
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/download', defaults={'req_path': ''})
def dir_listing(req_path):
    
    ''' Lists files in upload directory via hyperlinks to above function
        Currently no sub-directory support '''
    
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('download.html', files=files)

if __name__ == "__main__":
    app.run(host = "0.0.0.0")