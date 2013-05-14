from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from EnumSymbol import DeclEnum
#from hello import engine, session

engine = create_engine("mysql://root:@localhost/Scav")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

Base = declarative_base()

class GenderType(DeclEnum):
    female = "female", "Female"
    male = "male", "Male"
    either = "either", "Either"
    neither = "neither", "Neither"
    what = "what", "what?"

class Bathroom(Base):
        __tablename__ = 'bathrooms'
        id = Column(Integer, primary_key=True)
        location = Column(String(200))
        floor = Column(String(200))
        gender = Column(String(200))


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    content = Column(String(2000), nullable=False)
    rating = Column(Integer)
    bathroom_id = Column(Integer, ForeignKey('bathrooms.id'))
    bathroom = relationship("Bathroom", backref=backref('reviews', order_by=id))

Base.metadata.create_all(engine)

bathroom_new = Bathroom(location="harper", floor="1", gender="male")
review_new = Review(content="stuff", rating=3)
review_new.bathroom = bathroom_new
session.add(bathroom_new)
session.add(review_new)
session.commit()