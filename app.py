import numpy
import os
from flask import Flask, render_template, url_for, send_file
from PIL import Image
from StringIO import StringIO

app = Flask(__name__)

@app.route("/magic.png")
def magic():
    arr = numpy.zeros(500,500,3)
    arr[...,0]=256
    im = Image.fromarray(numpy.uint8(arr))
    
    img_io = StringIO()
    im.save(img_io,format='PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
    
@app.route("/")
def index():
    return render_template('show.html')

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=True)
