from flask import Blueprint
from .routes import CategoryView, SubCategoryView, ProductListView, ProductDetailView, ProductFilesView

product_blueprint = Blueprint('product', __name__)
product_blueprint.strict_slashes = False

product_blueprint.add_url_rule('/', view_func=CategoryView.as_view('category_list'), endpoint='category_list', methods=['GET'])
product_blueprint.add_url_rule('/<int:category_id>', view_func=SubCategoryView.as_view('subcategory_list'), endpoint='subcategory_list', methods=['GET'])
product_blueprint.add_url_rule('/<int:category_id>/<int:subcategory_id>', view_func=ProductListView.as_view('product_list'), endpoint='product_list', methods=['GET'])
product_blueprint.add_url_rule('/<int:category_id>/<int:subcategory_id>/<int:product_id>', view_func=ProductDetailView.as_view('product_detail'), endpoint='product_detail', methods=['GET'])
product_blueprint.add_url_rule('/product-files', view_func=ProductFilesView.as_view('product_files'), endpoint='product_files', methods=['POST'])
