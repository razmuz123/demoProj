from bottle import route, run, request, static_file, template, Bottle
from pymemcache.client.base import Client
import beanstalkc

app = application = Bottle()

# Setting up the homepage for the web application
@app.route('/')
def root():
    resp = static_file('site.html', root='html')
    return resp

# Handles the upload from the dropzone, and adds a job for backend to handle
@app.route('/upload', method='POST')
def do_upload():

    upload = request.files.get('file')
    beanstalk = beanstalkc.Connection(host='localhost', port=11300)
    beanstalk.put(upload.filename)
    beanstalk.close()

# Handles the information text in the application, reads text stored in memcache by backend
@app.route('/res')
def res():
    client = Client(('localhost', 11211))
    text = client.get('info')
    client.delete('info')
    client.close()
    return text

# Sets paths for the application, this to find folders during runtime
@app.route('/html/<path:path>')
def html(path):
    return static_file(path, root='html/')

@app.route('/js/<path:path>')
def static_js(path):
    return static_file(path, root='js/')

@app.route('/css/<path:path>')
def static_css(path):
    return static_file(path, root='css/')

#Starts up the webpage when run
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True, reloader=True)

