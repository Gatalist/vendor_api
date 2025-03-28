from flask import Blueprint
from .routes import CategoryView, SubCategoryView, ProductListView, ProductDetailView

product_blueprint = Blueprint('product', __name__)

product_blueprint.add_url_rule('/', view_func=CategoryView.as_view('category_list'), endpoint='category_list')
product_blueprint.add_url_rule('/<int:category_id>', view_func=SubCategoryView.as_view('subcategory_list'), endpoint='subcategory_list')
product_blueprint.add_url_rule('/<int:category_id>/<int:subcategory_id>', view_func=ProductListView.as_view('product_list'), endpoint='product_list')
product_blueprint.add_url_rule('/<int:category_id>/<int:subcategory_id>/<int:product_id>', view_func=ProductDetailView.as_view('product_detail'), endpoint='product_detail')
