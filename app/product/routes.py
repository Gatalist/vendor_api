from flask import render_template, request, jsonify
from flask.views import MethodView


class HomeView(MethodView):
    def get(self):
        context = {}
        # data = {"message": "This is your API response"}
        # return jsonify(data)
        return render_template('include/index.html', **context)
