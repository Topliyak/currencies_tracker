from server.app import app
from os import environ


host = environ.get('HOST') or 'localhost'
port = int(environ.get('PORT') or '5000')

if environ.get('DONTRUN') is None:
    app.run(host, port)
