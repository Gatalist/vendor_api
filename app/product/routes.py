from flask import render_template, request, jsonify
from flask.views import MethodView
from app.mti_api.parser import Parser


class HomeView(MethodView):
    def get(self):
        # parser = Parser(url='https://products.mti.ua/api/?action=loadContent&key=Sqceh4xB9PvL&cat_id=216')
        # context = parser.get_all_data()
        context = {
            "cards": [
                'first', 'second', 'third', 'fourth', 'fifth', 'sixth',
            ]
        }
        return render_template('include/index.html', **context)
