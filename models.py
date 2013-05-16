from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
#from hello import engine, session

engine = create_engine("mysql://root:@localhost/Truckate")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

Base = declarative_base()



class User(Base):
        __tablename__ = 'users'
        id = Column(Integer,primary_key=True)
        email = Column(String(200))
        firstName = Column(String(50))
        lastName = Column(String(50))
        password = Column(String(200))
        phone = Column(String(20))

class Operator(Base):
        __tablename__ = 'operators'
        id = Column(Integer,primary_key=True)
        email = Column(String(200))
        password = Column(String(200))
        phone = Column(String(20))
        open = Column(Boolean)
        location = Column(String(50))
        name = Column(String(200))

class Item(Base):
        __tablename__ = 'items'
        id = Column(Integer,primary_key=True)
        name = Column(String(200))
        price = Column(Float)
        desc = Column(String(200))
        count = Column(Integer)
        operator_id = Column(Integer, ForeignKey('operators.id'))
        operator = relationship("Operator",backref=backref('item',order_by=id))

class Order(Base):
        __tablename__ = 'orders'
        id = Column(Integer,primary_key=True)
        operator = relationship("Operator",backref=backref('order',order_by=id))
        operator_id = Column(Integer, ForeignKey('operators.id'))
        user = relationship("User",backref=backref('order',order_by=id))
        user_id = Column(Integer,ForeignKey('users.id'))
        #status options: created, paid, completed
        status = Column(String(200))

class OrderItems(Base):
        __tablename__ = 'order_items'
        id = Column(Integer,primary_key=True)
        order = relationship("Order",backref=backref('order_item',order_by=id))
        item = relationship("Item",backref=backref('order_item',order_by=id))
        order_id = Column(Integer, ForeignKey('orders.id'))
        item_id = Column(Integer,ForeignKey('items.id'))




Base.metadata.create_all(engine)

#print 'Created'
#bathroom_new = Bathroom(location="harper", floor="1", gender="male")
#review_new = Review(content="stuff", rating=3)
#review_new.bathroom = bathroom_new
#session.add(bathroom_new)
#session.add(review_new)
#session.commit()