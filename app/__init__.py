from flask import Flask, jsonify, make_response, request, abort
from flask_sqlalchemy import SQLAlchemy
from config import app_config

db = SQLAlchemy()


def create_app(config_name):

    from app.models import Item

    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/todo/api/v1.0/items', methods=['GET'])
    def get_items():
        items = Item.get_all()
        response = jsonify([item.to_dict() for item in items])
        return make_response(response), 200

    @app.route('/todo/api/v1.0/items', methods=['POST'])
    def create_item():
        data = request.get_json()
        if not data or not data['name']:
            abort(400)
        item = Item(data['name'])
        item.save()
        response = jsonify(item.to_dict())
        return make_response(response), 201

    @app.route('/todo/api/v1.0/items/<int:id>', methods=['DELETE'])
    def delete_item(id):
        item = Item.query.filter_by(id=id).first()
        if not item:
            abort(404)
        item.delete()
        response = jsonify(item.to_dict())
        return make_response(response), 200

    return app
