#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    
    bakeries = []
    for bakery in BakedGood.query.all():
        bakery_dict = {
            "name": bakery.name,
            "price": bakery.price,
            "id": bakery.id,
            "updated_at": bakery.updated_at,
            "created_at": bakery.created_at,
            "bakery_id": bakery.bakery_id
        }
        bakeries.append(bakery_dict)
        
        response = make_response(
            bakeries, 
            200,
            {"Content-Type": "application/json"}
            )
        
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(
        # it still needs to be JSON, after all
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    bakery = BakedGood.query.order_by(BakedGood.price.desc()).all()

    bakery_dict = [bakery_good.to_dict() for bakery_good in bakery]
 
    response = make_response(
        # it still needs to be JSON, after all
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price).first()
     
    baked_good = baked_good.to_dict()
     
    response = make_response(
        # it still needs to be JSON, after all
        jsonify(baked_good),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
