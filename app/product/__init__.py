from flask import Blueprint
from .routes import HomeView


product_blueprint = Blueprint('product', __name__)

product_blueprint.add_url_rule('/', view_func=HomeView.as_view('home'))
