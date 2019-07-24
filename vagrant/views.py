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




#foursquare_client_id = ''

#foursquare_client_secret = ''

#google_api_key = ''

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  if request.method == 'GET':
    res = session.query(Restaurant).all()
    return jsonify(r.serialize for r in res)

  elif request.method == 'POST':
    meal = request.args.get('mealType', '')
    loc = request.args.get('location', '')
    resInfo = findARestaurant(meal, loc)
    if resInfo != 'none':
      res = Restaurant(restaurant_name = unicode(restaurant_info['name']),
      restaurant_address = unicode(restaurant_info['address']),
      restaurant_image = restaurant_info['image'])
      session.add(res)
      session.commit()
      return jsonify(restaurant = res.serialize)

@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  if request.method == 'GET':

  elif request.method == 'PUT':

  elif request.method == 'DELETE':


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
