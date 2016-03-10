from werkzeug.routing import BaseConverter
from flask import Flask
from flask.ext.cors import CORS



class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]




def configure_app(app):
    if isinstance(app, Flask) == False:
        raise TypeError("app must be a Flask application instance")

    CORS(app, resources=r'*', send_wildcard=True)

    app.url_map.converters['regex'] = RegexConverter

    return app 
