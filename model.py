from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import correlation

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,autocommit=False,autoflush=False))

Base = declarative_base()
Base.query = session.query_property()


### Class declarations go here

class User(Base):
    
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)
    gender = Column(String(1), nullable = True)
    occupation = Column(String(30), nullable=True)

    def similarity(self,other):
        u_ratings={}
        paired_ratings=[]
        for r in self.ratings:
            u_ratings[r.movie_id]=r
        for r in other.ratings:
            u_r=u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append((u_r.rating,r.rating))
        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    # ratings added by Ratings backref (list of ratings for this user)

class Movie(Base):

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

    #rating = relationship("Rating",backref=backref("movie",order_by=id)) #get rid of this

class Rating(Base):

    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)
    timestamp = Column(Integer)

    user = relationship("User",backref=backref("ratings",order_by=id)) 
    movie = relationship("Movie",backref=backref("ratings", order_by=id))

### End class declarations

# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///ratings.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
