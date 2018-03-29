import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

# Global Setup
user = "postgres"
password = "python"
host = "localhost"
port = 5432
database = "postgres"
url = 'postgresql://{}:{}@{}:{}/{}'
db_string = url.format(user, password, host, port, database)
db = sqlalchemy.create_engine(db_string)
base = sqlalchemy.ext.declarative.declarative_base()


class LibraryBranches(base):
    # see: https://data.lacity.org/A-Livable-and-Sustainable-City/Library-Branches/a4nt-4gca
    __tablename__ = 'LibraryBranches'

    BranchName = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    PhoneNumber = sqlalchemy.Column(sqlalchemy.String)
    Email = sqlalchemy.Column(sqlalchemy.String)
    CouncilDistrict = sqlalchemy.Column(sqlalchemy.Integer)
    Address = sqlalchemy.Column(sqlalchemy.String)
    City = sqlalchemy.Column(sqlalchemy.String)
    State = sqlalchemy.Column(sqlalchemy.String)
    Zip = sqlalchemy.Column(sqlalchemy.String)
