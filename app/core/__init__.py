from flask import Flask, request, jsonify
from app.product import product_blueprint
from .settings import Config


def create_app():
    new_app = Flask(__name__)
    new_app.config.from_object(Config)
    new_app.root_path = new_app.config['ROOT_PATH']

    new_app.register_blueprint(product_blueprint, url_prefix="/")

    return new_app

app = create_app()
