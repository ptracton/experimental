
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

# Global Setup
db_string = 'sqlite:///sqlalchemy_example.db'
db = sqlalchemy.create_engine(db_string)
base = sqlalchemy.ext.declarative.declarative_base()

class People(base):
    __tablename__ = 'people'

    PersonalNumber = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    FirstName = sqlalchemy.Column(sqlalchemy.String)
    LastName = sqlalchemy.Column(sqlalchemy.String)
    StreetAddress = sqlalchemy.Column(sqlalchemy.String)
    City = sqlalchemy.Column(sqlalchemy.String)
    Region = sqlalchemy.Column(sqlalchemy.String)
    Zip = sqlalchemy.Column(sqlalchemy.String)
    Country = sqlalchemy.Column(sqlalchemy.String)
    Pin = sqlalchemy.Column(sqlalchemy.String)
    Date = sqlalchemy.Column(sqlalchemy.String)
    Email = sqlalchemy.Column(sqlalchemy.String)
