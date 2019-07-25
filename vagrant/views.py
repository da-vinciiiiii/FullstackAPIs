from models import Base, User, Bagel
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth() 


engine = create_engine('sqlite:///bagelShop.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

#ADD @auth.verify_password here
@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username = username).first()
    if not user:
        return False
    elif not user.verify_password(password):
        return False
    else:
        g.user = user
        return True

@auth.verify_password
def verify_password(userOrToken, password):
    user_id = User.verify_auth_token(userOrToken)
    if user_id:
        user = session.query(User).filter_by(id = user_id).first()
    else:
        user = session.query(User).filter_by(username = userOrToken).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
    

@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.gen_auth_token()
    return jsonify({'token': token.decode('ascii')})

#ADD a /users route here
@app.route('/users', methods = ['POST'])
def addUser():
    username = request.args.get('username')
    password = request.args.get('password')
    
    if username != None and password != None:
        if session.query(User).filter_by(username = username).first() != None:
            user = session.query(User).filter_by(username = username).first()
            return jsonify({'error':'This user is already in our system'})
    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'username': user.username}), 201

@app.route('/bagels', methods = ['GET','POST'])
@auth.login_required
def showAllBagels():
    if request.method == 'GET':
        bagels = session.query(Bagel).all()
        return jsonify(bagels = [bagel.serialize for bagel in bagels])
    elif request.method == 'POST':
        name = request.json.get('name')
        description = request.json.get('description')
        picture = request.json.get('picture')
        price = request.json.get('price')
        newBagel = Bagel(name = name, description = description, picture = picture, price = price)
        session.add(newBagel)
        session.commit()
        return jsonify(newBagel.serialize)

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
