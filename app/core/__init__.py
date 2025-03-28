from flask import Flask
from app.product import product_blueprint
from .settings import Config
from .extensions import cache


def create_app():
    new_app = Flask(__name__)
    new_app.config.from_object(Config)
    new_app.root_path = new_app.config['ROOT_PATH']
    new_app.register_blueprint(product_blueprint, url_prefix="/")
    return new_app

app = create_app()
app.config.from_mapping({"CACHE_TYPE": "SimpleCache"})

from . import extensions
extensions.cache.init_app(app)
