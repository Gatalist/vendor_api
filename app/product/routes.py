from flask import render_template, request, jsonify
from flask.views import MethodView

from app.mti_api.downloader import download_and_convert_images
from app.mti_api.parser import Parser


class HomeView(MethodView):
    def get(self):
        return render_template('include/index.html')

    def post(self):
        data = request.get_json()
        option = data.get('option')

        if option == 'getProducts':
            url = data.get('url')
            if url.startswith('https://products.mti.ua/api'):
                print(url)
                # https://products.mti.ua/api/?action=loadContent&key=Sqceh4xB9PvL&cat_id=216
                parser = Parser(url=url)
                context = parser.get_all_data()
                return jsonify(context), 200
            else:
                return jsonify({'error': 'url invalid'}), 400

        if option == 'saveImg':
            imgs = []
            picture = data.get('picture')
            photos = data.get('photos')
            card_id = data.get('cardId')
            if picture:
                imgs.append({card_id: picture})
            if photos:
                imgs.extend(photos)
            print("photos", photos)
            print("imgs", imgs)
            if imgs:
                return download_and_convert_images(image_urls=imgs, name_zip=card_id)
            else:
                return jsonify({'error': 'no image'}), 400