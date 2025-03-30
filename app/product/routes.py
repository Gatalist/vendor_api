from flask import render_template, jsonify, request
from flask.views import MethodView
from .cached import DatabaseCached
from app.mti_api.downloader import download_and_convert_images, download_file_in_zip


class CategoryView(DatabaseCached, MethodView):
    def get(self):
        context = {
            "category_list": self.get_main_categories(),
            "is_search": True,
        }
        # print("category tree:", categories)
        return render_template('include/category_list.html', **context)


class SubCategoryView(DatabaseCached, MethodView):
    def get(self, category_id):
        subcategory_list = []
        for cat in self.get_all_categories():
            if cat.get('parentID') == int(category_id) and not cat.get('parentID') in subcategory_list:
                subcategory_list.append(cat)

        context = {
            "category_id": category_id,
            "subcategory_list": subcategory_list,
            "is_search": True,
        }
        # print("subcategory context:", context)
        return render_template('include/subcategory_list.html', **context)


class ProductListView(DatabaseCached, MethodView):
    def get(self, category_id, subcategory_id):
        context = self.get_products_category(subcategory_id)
        context["category_id"] = category_id
        context["subcategory_id"] = subcategory_id
        context["is_search"] = True
        # print("product context:", context)
        return render_template('include/product_list.html', **context)


class ProductDetailView(DatabaseCached, MethodView):
    def get(self, category_id, subcategory_id, product_id):
        product = self.get_product_info(subcategory_id, product_id)
        context = {
            "product": product,
            "category_id": category_id,
            "subcategory_id": subcategory_id,
            "is_search": False,
        }
        print("product context:", context)
        return render_template('include/product_detail.html', **context)


class ProductFilesView(DatabaseCached, MethodView):
    def post(self):
        data = request.get_json()
        option = data.get('option')
        subcategory_id = data.get('subcategoryId')
        product_id = data.get('productId')
        product = self.get_product_info(subcategory_id, product_id)
        print("data:", data)

        if option == 'getImageWebp':
            picture = product['detail_picture']
            photos = product['photos']

            imgs = []
            if picture:
                imgs.append({product_id: picture})
            if photos:
                imgs.extend(photos)
            if imgs:
                return download_and_convert_images(image_urls=imgs, name_zip=product_id)
            else:
                return jsonify({'error': 'no image'}), 400

        if option == 'getImageOrigin':
            picture = product['detail_picture']
            photos = product['photos']

            imgs = []
            if picture:
                imgs.append({product_id: picture})
            if photos:
                imgs.extend(photos)
            if imgs:
                return download_file_in_zip(links=imgs, name_zip=product_id, filename="image")
            else:
                return jsonify({'error': 'no image'}), 400

        if option == 'getInstruction':
            attributes = product.get('attributes')
            files = []
            count = 1
            print("attributes:", attributes)
            if attributes:
                for attribute in attributes:
                    if attribute.get('code_name') == 'file':
                        print(attribute)
                        files.append({attribute.get("id") or f"file_{count}": attribute.get("value")})
                        count += 1
            print("files:", files)
            if files:
                return download_file_in_zip(links=files, name_zip=product_id, filename="file")
            else:
                return jsonify({'error': 'no files'}), 400


# http://127.0.0.1:5000/7/1815/3729196
