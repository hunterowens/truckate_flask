from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
#from hello import engine, session

engine = create_engine("mysql://root:@localhost/Truckate")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

Base = declarative_base()


#association_table = Table('Orders_Items', Base.metadata,
 #       Column('order_id', Integer, ForeignKey('orders.id')),
 #       Column('item_id', Integer, ForeignKey('items.id'))
#)

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






Base.metadata.create_all(engine)

#print 'Created'
#bathroom_new = Bathroom(location="harper", floor="1", gender="male")
#review_new = Review(content="stuff", rating=3)
#review_new.bathroom = bathroom_new
#session.add(bathroom_new)
#session.add(review_new)
#session.commit()