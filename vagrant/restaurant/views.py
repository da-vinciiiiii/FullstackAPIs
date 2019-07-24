from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


engine = create_engine('sqlite:///restaurants.db',connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  if request.method == 'GET':
    res = session.query(Restaurant).all()
    return jsonify(restaurants = [r.serialize for r in res])

  elif request.method == 'POST':
    meal = request.args.get('mealType', '')
    loc = request.args.get('location', '')
    resInfo = findARestaurant(meal, loc)
    if resInfo != 'none':
      res = Restaurant(restaurant_name = unicode(resInfo['name']),
      restaurant_address = unicode(resInfo['address']),
      restaurant_image = resInfo['image'])
      session.add(res)
      session.commit()
      return jsonify(restaurant = res.serialize)

@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  res = session.query(Restaurant).filter_by(id = id).first()
  if request.method == 'GET':
    return jsonify(restaurant = res.serialize)
  elif request.method == 'PUT':
    name = request.args.get('name')
    addr = request.args.get("address")
    img = request.args.get ('image')
    if name:
      res.restaurant_name = name
    if addr:
      res.restaurant_address = addr
    if img:
      res.restaurant_image = img
    return jsonify(restaurant = res.serialize)
  elif request.method == 'DELETE':
      session.delete(res)
      session.commit()
      return "deleted"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
