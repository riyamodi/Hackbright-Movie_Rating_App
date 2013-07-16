from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here

class User(Base):
    
    __tablename__ = "users"
    print "I'm here!"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)
    gender = Column(String(1), nullable = True)
    occupation = Column(String(30), nullable=True)


class Movies(Base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    movie_title = Column(String(64), nullable = True)
    release_date = Column(Integer, nullable = True)
    video_release_date = Column(Integer, nullable = True)
    imdb_url = Column(String(64), nullable=True)
    unknown = Column(Integer, nullable=True)
    action = Column(Integer, nullable=True)
    adventure = Column(Integer, nullable=True)
    animation = Column(Integer, nullable=True)
    childrens = Column(Integer, nullable=True)
    comedy = Column(Integer, nullable=True)
    crime = Column(Integer, nullable=True)
    documentary = Column(Integer, nullable=True)
    drama = Column(Integer, nullable=True)
    fantasy = Column(Integer, nullable=True)
    film_noir = Column(Integer, nullable=True)
    horror = Column(Integer, nullable=True)
    musical = Column(Integer, nullable=True)
    mystery = Column(Integer, nullable=True)
    romance = Column(Integer, nullable=True)
    sci_fi = Column(Integer, nullable=True)
    thriller = Column(Integer, nullable=True)
    war = Column(Integer, nullable=True)
    western = Column(Integer, nullable=True)



class Ratings(Base):

    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)
    timestamp = Column(Integer)

    user = relationship("User",backref=backref("ratings",order_by=id))

### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()