#! /usr/bin/env python3

import requests
import urllib

import datetime
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


def highestRevenue(session=None, startDate=None, endDate=None):
    qry = session.query(
        sqlalchemy.sql.func.max(
            Movies.revenue).label("highest_revenue")).filter(
                sqlalchemy.and_(Movies.release_date >= startDate,
                                Movies.release_date < endDate))
    revenue = qry.all()[0][0]
    qry = session.query(Movies).filter(Movies.revenue == revenue)
    title = qry.all()
    return title[0]


def totalRevenue(session=None, startDate=None, endDate=None):
    qry = session.query(
        sqlalchemy.sql.func.sum(Movies.revenue).label("all_revenue")).filter(
            sqlalchemy.and_(Movies.release_date >= startDate,
                            Movies.release_date < endDate))
    revenue = qry.all()[0][0]
    return revenue


def highestBudget(session=None, startDate=None, endDate=None):
    qry = session.query(
        sqlalchemy.sql.func.max(Movies.budget).label("highest_budget")).filter(
            sqlalchemy.and_(Movies.release_date >= startDate,
                            Movies.release_date < endDate))
    budget = qry.all()[0][0]
    qry = session.query(Movies).filter(Movies.budget == budget)
    title = qry.all()
    return title[0]

    return


def genresString(genres=None):

    jsonGenres = json.loads(genres)
    #print(jsonGenres)
    returnString = ""
    for x in jsonGenres:
        #print (x['name'])
        returnString = returnString + " " + x['name']
    return returnString


if __name__ == "__main__":

    ia = imdb.IMDb()  # by default access the web.

    # Search for a movie (get a list of Movie objects).
    s_result = ia.search_movie('Star')

    #print(s_result)
    # Print the long imdb canonical title and movieID of the results.
    #for item in s_result:
    #    print(item['long imdb canonical title'], item['year'], item.movieID)

    #sys.exit(0)

    Session = sqlalchemy.orm.sessionmaker(db)
    session = Session()

    base.metadata.create_all(db)

    movies = session.query(Movies)

    year2010 = datetime.date(year=2010, month=1, day=1)
    year2010 = '2015-01-01'
    year2011 = datetime.date(year=2011, month=1, day=1)
    year2011 = '2016-01-01'
    movies_2010 = session.query(Movies).filter(
        sqlalchemy.and_(Movies.release_date >= year2010,
                        Movies.release_date < year2011))
    #movies_2010 = session.query(Movies).filter(Movies.release_date > year2010)
    for x in movies_2010:
        print("{:30} {:12} {:12} {:10} {:10}".format(x.title, x.release_date,
                                                     x.revenue, x.budget,
                                                     genresString(x.genres)))

    revenue = highestRevenue(session, year2010, year2011)
    print("{} {} ".format(revenue.title, revenue.revenue))
    trevenue = totalRevenue(session, year2010, year2011)
    print("{} ".format(trevenue))
    print("Highest Revenue Movie Percent {}%".format(
        100 * (revenue.revenue / trevenue)))
    budget = highestBudget(session, year2010, year2011)
    print("{} {} ".format(budget.title, budget.budget))

    # https://stackoverflow.com/questions/4582264/python-sqlalchemy-order-by-datetime?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    entities = session.query(Movies).order_by(
        sqlalchemy.desc(Movies.release_date)).limit(10).all()
    print(entities)
    for x in entities:
        print("{} {}".format(x.title, x.release_date))


    sys.exit(0)

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
