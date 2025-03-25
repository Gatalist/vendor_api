import os
import datetime


class Config(object):
    HOST: str = "0.0.0.0"
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_LIFETIME = datetime.timedelta(days=10)
    ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    STATIC_PATH = os.path.join(ROOT_PATH, 'static')
    TEMPLATES_PATH = os.path.join(ROOT_PATH, 'templates')
    MEDIA_PATH = os.path.join(STATIC_PATH, 'media')
