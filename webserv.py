import sys
import json
import re as regex
import math
import numpy as np
from PIL import Image
from io import BytesIO
import base64 as bs64
import json
import os
from flask import Flask, request, Response, json, app, render_template
from flask_cors import CORS, extension
import pathlib

app = Flask(__name__)

# @cross_origin is for Cross domain access
CORS(app, supports_credentials=True)
# the method is a catch all route
@app.route('/getNearPhotos/',defaults={'u_path': ''})
@app.route('/getNearPhotos/<path:u_path>')

def Main(u_path):


    #
    # if the path is not starting with pid 
    # get the pathand the full directory
    #
    if not u_path.startswith('pid'):
        #Work as normal web server
        #Return file as specified
        rt_path=app.root_path
        dir='\\getNearPhotos\\'+u_path
        full_path=rt_path+dir
        
        #
        # Check the extention of the files so they will
        # be shown correctly.
        # It gets the content of the file and then it passes it
        # accordingly
        # Any unnecessary quotes are removed
        #
        if(full_path[-2:] == 'js'):
            content= readfile(full_path)
            content=regex.sub(r'^"','',content)
            content=regex.sub(r'"$','',content)
            return render_template('getjs.html', value=content)
        elif(full_path[-4:] == 'html'):
            content= readfile(full_path)
            content=regex.sub(r'^"','',content)
            content=regex.sub(r'"$','',content)
            print(content)
            return render_template('gethtml.html', value=content)
        else:
            content= readfile(full_path)
            content=regex.sub(r'^"','',content)
            content=regex.sub(r'"$','',content)
            print(content)
            return render_template('gethtml.html', value=content)
    else:
        #
        # idnum - get the pic id
        # p_abs - the absolute path
        # Open the image with Pillow save it as jpeg on a file-like object in memory to save image without using disk
        # then convert it as bytes and then to string  
        #
        #
        idnum=u_path[4:]
        p_abs='Z:\\home.jpg'
        img = Image.open(p_abs)
        imdata=BytesIO() #create file-like object in memory to save image without using disk
        img.save(imdata,format='jpeg')  # save image in file-like object
        data=imdata.getvalue() # get data from file (BytesIO)
        data=bs64.b64encode(data) # convert to base64 as bytes
        data=data.decode()  # convert bytes to string
        passimg='data:image/png;base64,'+format(data) # data that will be passed to html in order to show image
        
        return render_template ('photopath.html', value=passimg, pid=idnum )

        #Get absolute path of image
        #dbname = 'PhotoData.db'
        #conn = sqlite3.connect(dbname)
        #conn.row_factory = sqlite3.Row
        #cur = conn.cursor()
        #sql = 'SELECT Id, filepath FROM photos WHERE id= ? '
        
        #data = (idnum, )
        #cur.execute(sql,data)
        #rows = cur.fetchall()

        #for row in rows:
        #    p_abs = pathlib.Path(str(row['filepath']))
        #
        #Return file in absolute path as "p_abs"
        #******** I Need you to do here **********
      
#
# Reads and returns the content of the file
#
def readfile(file):
    with open (file) as fl:
        fl_cont=fl.read()
    return '"{}"'.format(fl_cont)

if __name__ == '__main__':
    app.run(port=8890,debug=True)
