from flask import render_template
from flask.views import MethodView
from .cached import DatabaseCached


class CategoryView(DatabaseCached, MethodView):
    def get(self):
        categories = self.get_main_categories()
        # print("category tree:", categories)
        return render_template('include/category_list.html', category_list=categories)


class SubCategoryView(DatabaseCached, MethodView):
    def get(self, category_id):
        subcategory_list = []
        for cat in self.get_all_categories():
            if cat.get('parentID') == int(category_id) and not cat.get('parentID') in subcategory_list:
                subcategory_list.append(cat)

        context = {
            "category_id": category_id,
            "subcategory_list": subcategory_list
        }
        # print("subcategory context:", context)
        return render_template('include/subcategory_list.html', **context)


class ProductListView(DatabaseCached, MethodView):
    def get(self, category_id, subcategory_id):
        context = self.get_products_category(subcategory_id)
        context["category_id"] = category_id
        context["subcategory_id"] = subcategory_id
        # print("product context:", context)
        return render_template('include/product_list.html', **context)


class ProductDetailView(DatabaseCached, MethodView):
    def get(self, category_id, subcategory_id, product_id):
        product = self.get_product_info(subcategory_id, product_id)
        context = {
            "product": product,
            "category_id": category_id,
            "subcategory_id": subcategory_id,
        }
        print("product context:", context)
        return render_template('include/product_detail.html', **context)


# http://127.0.0.1:5000/7/1815/3729196



# class ProductView(MethodView):
#     def get(self):
#         return render_template('include/index.html')
#
#     def post(self):
#         data = request.get_json()
#         option = data.get('option')
#
#         if option == 'getProducts':
#             cat_id = data.get('url')
#             print(cat_id)
#
#             # https://products.mti.ua/api/?action=loadContent&key=Sqceh4xB9PvL&cat_id=216
#             # parser = ParserProductList(cat_id=cat_id)
#             # context = parser.get_all_data()
#             parser = ParserStructureCategory()
#             parser.get_categories()
#             tree = parser.build_tree(0, parser.categories)
#             print("tree:", tree)
#             # print("tree:", json.dumps(tree, ensure_ascii=False, indent=2))
#             context = tree
#             return jsonify(context), 200
#
#         if option == 'saveImg':
#             imgs = []
#             picture = data.get('picture')
#             photos = data.get('photos')
#             card_id = data.get('cardId')
#             if picture:
#                 imgs.append({card_id: picture})
#             if photos:
#                 imgs.extend(photos)
#             if imgs:
#                 return download_and_convert_images(image_urls=imgs, name_zip=card_id)
#             else:
#                 return jsonify({'error': 'no image'}), 400
#
#         else:
#             return jsonify({'error': 'url invalid'}), 400