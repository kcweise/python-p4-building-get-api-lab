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
    
    all_bakeries = Bakery.query.all()
    
    bakeries_dict=[bakery.to_dict() for bakery in all_bakeries]
      
    response = make_response(bakeries_dict, 200)
    
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    
    serialized_bakery = bakery.to_dict()  
    
    return jsonify(serialized_bakery),200

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    
    serialized_goods = [good.to_dict() for good in goods]
            
    return jsonify(serialized_goods)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    serialized_goods = goods.to_dict()
            
    return jsonify(serialized_goods)
   

if __name__ == '__main__':
    app.run(port=5555, debug=True)
