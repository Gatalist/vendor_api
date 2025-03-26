from flask import render_template, request, jsonify
from flask.views import MethodView
from app.mti_api.parser import Parser


class HomeView(MethodView):
    def get(self):
        return render_template('include/index.html')

    def post(self):
        data = request.get_json()
        url = data.get('url')
        if url.startswith('https://products.mti.ua/api'):
            print(url)
            # https://products.mti.ua/api/?action=loadContent&key=Sqceh4xB9PvL&cat_id=216
            parser = Parser(url=url)
            context = parser.get_all_data()
            return jsonify(context), 200
        else:
            return jsonify({'error': 'url invalid'}), 400
