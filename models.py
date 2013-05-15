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
        password = Column(String(200))
        phone = Column(Integer)

class Operator(Base):
        __tablename__ = 'operators'
        id = Column(Integer,primary_key=True)
        email = Column(String(200))
        password = Column(String(200))
        phone = Column(Integer)
        open = Column(Boolean)

class Item(Base):
        __tablename__ = 'items'
        name = Column(String(200))
        price = Column(Float)
        operator_id = Column(Integer, ForeignKey('operators.id'))
        operator = relationship("Operator",backref=backref('item',order_by=id))



Base.metadata.create_all(engine)

print 'Created'
#bathroom_new = Bathroom(location="harper", floor="1", gender="male")
#review_new = Review(content="stuff", rating=3)
#review_new.bathroom = bathroom_new
#session.add(bathroom_new)
#session.add(review_new)
#session.commit()