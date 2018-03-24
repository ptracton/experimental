#! /usr/bin/env python3

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


class Film(base):
    __tablename__ = 'films'

    title = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    director = sqlalchemy.Column(sqlalchemy.String)
    year = sqlalchemy.Column(sqlalchemy.String)


if __name__ == "__main__":

    Session = sqlalchemy.orm.sessionmaker(db)
    session = Session()

    base.metadata.create_all(db)

    # Create
    doctor_strange = Film(
        title="Doctor Strange", director="Scott Derrickson", year="2016")
    thor_ragnarok = Film(
        title="Thor Ragnarok", director="Taika Watiti", year="2017")
    session.add(doctor_strange)
    session.add(thor_ragnarok)
    session.commit()

    # Read
    films = session.query(Film)
    for film in films:
        print(film.title)

    # Update
    doctor_strange.title = "Some2016Film"
    session.commit()

    # Delete
    session.delete(doctor_strange)
    session.commit()
