from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
secretKey = "".join(random.choice(string.ascii_uppercase + string.digits)
	for x in xrange(32))
#ADD YOUR USER MODEL HERE
class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String(32), index=True)
	passHash = Column(String(64))

	def hash_password(self, password):
		self.passHash = pwd_context.encrypt(password)
	
	def verify_password(self, password):
		return pwd_context.verify(password, self.passHash)

	def gen_auth_token(self, expiration = 3600):
		s = Serializer(secretKey, expires_in = expiration)
		return s.dumps({'id': self.id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(secretKey)
		try:
			d = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		user_id = data['id']
		return user_id

class Bagel(Base):
	__tablename__ = 'bagel'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	picture = Column(String)
	description = Column(String)
	price = Column(String)
	@property
	def serialize(self):
	    """Return object data in easily serializeable format"""
	    return {
	    'name' : self.name,
	    'picture' : self.picture,
	    'description' : self.description,
	    'price' : self.price
	        }


engine = create_engine('sqlite:///bagelShop.db')
 

Base.metadata.create_all(engine)
    
