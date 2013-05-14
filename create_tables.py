from models import Base, Review, Bathroom
from hello import engine

Base.metadata.create_all(engine)
