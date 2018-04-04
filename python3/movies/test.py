#! /usr/bin/env python3

import json
import sys

import imdb

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

# Global Setup
user = "postgres"
password = "python"
host = "localhost"
port = 5432
db = "postgres"
url = 'postgresql://{}:{}@{}:{}/{}'
db_string = url.format(user, password, host, port, db)
db = sqlalchemy.create_engine(db_string)
base = sqlalchemy.ext.declarative.declarative_base()


class Movies(base):
    __tablename__ = "Movies"
    id = sqlalchemy.Column(sqlalchemy.Numeric, primary_key=True)

    budget = sqlalchemy.Column(sqlalchemy.Numeric)
    popularity = sqlalchemy.Column(sqlalchemy.Numeric)
    runtime = sqlalchemy.Column(sqlalchemy.Numeric)
    vote_average = sqlalchemy.Column(sqlalchemy.Numeric)
    vote_count = sqlalchemy.Column(sqlalchemy.Numeric)
    revenue = sqlalchemy.Column(sqlalchemy.Numeric)

    genres = sqlalchemy.Column(sqlalchemy.String)
    homepage = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    tagline = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.String)

    release_date = sqlalchemy.Column(sqlalchemy.DateTime)


class MovieCredits(base):
    __tablename__ = "Credits"
    movie_id = sqlalchemy.Column(sqlalchemy.Numeric, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    cast = sqlalchemy.Column(sqlalchemy.String)
    crew = sqlalchemy.Column(sqlalchemy.String)


if __name__ == "__main__":


    ia = imdb.IMDb() # by default access the web.

    # Search for a movie (get a list of Movie objects).
    s_result = ia.search_movie('Star')


    #print(s_result)
    # Print the long imdb canonical title and movieID of the results.
    for item in s_result:
        print(item['long imdb canonical title'], item['year'], item.movieID)

    #sys.exit(0)
        
    Session = sqlalchemy.orm.sessionmaker(db)
    session = Session()

    base.metadata.create_all(db)

    movies = session.query(Movies)

    film = 'Avatar'
    film_id = int(109445)
    movie_credits = session.query(MovieCredits).filter(
        MovieCredits.title == film)

    movie_credits_count = session.query(MovieCredits).filter(
        MovieCredits.title == film).count()

    print(movie_credits_count)
    cast = json.loads(movie_credits[0].cast)
    crew = movie_credits[0].crew

    print(type(cast))
    for x in cast:
        print("{:20} {:20} ".format(x['name'], x['character']))
    #sys.exit(0)

    for movie in movies:
        if movie.tagline is None:
            movie.tagline = "NONE"
        if movie.budget is None:
            movie.budget = 0
        if movie.release_date is None:
            movie.release_date = "UNKNOWN"

        movie_credits = session.query(MovieCredits).filter(
            MovieCredits.title == movie.title)
        movie_credits_count = session.query(MovieCredits).filter(
            MovieCredits.title == movie.title).count()

        cast = json.loads(movie_credits[0].cast)
        if len(cast) == 0:
            cast = []
            cast.append({})
            cast[0]['name'] = "NONE"
            
        print("{:20} {:40} {:10}".format(movie.title, movie.revenue,
                                         cast[0]['name']))
