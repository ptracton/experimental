import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

# Global Setup
db_string = 'sqlite:///sqlalchemy_example.db'
db = sqlalchemy.create_engine(db_string)
base = sqlalchemy.ext.declarative.declarative_base()


class LALibraryBranches(base):
    # see: https://data.lacity.org/A-Livable-and-Sustainable-City/Library-Branches/a4nt-4gca
    __tablename__ = 'LALibraryBranches'

    BranchName = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    PhoneNumber = sqlalchemy.Column(sqlalchemy.String)
    Email = sqlalchemy.Column(sqlalchemy.String)
    CouncilDistrict = sqlalchemy.Column(sqlalchemy.Integer)
    Address = sqlalchemy.Column(sqlalchemy.String)
    City = sqlalchemy.Column(sqlalchemy.String)
    State = sqlalchemy.Column(sqlalchemy.String)
    Zip = sqlalchemy.Column(sqlalchemy.String)


class QueensLibraryBranches(base):
    # see: https://data.cityofnewyork.us/Recreation/Queens-Libraries/swsf-ed7j
    __tablename__ = "QueensLibraryBranches"

    BranchName = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    PhoneNumber = sqlalchemy.Column(sqlalchemy.String)
    Address = sqlalchemy.Column(sqlalchemy.String)
    City = sqlalchemy.Column(sqlalchemy.String)
    Zip = sqlalchemy.Column(sqlalchemy.String)
    Burough = sqlalchemy.Column(sqlalchemy.String)
    CommunityCouncil = sqlalchemy.Column(sqlalchemy.String)


class ChicagoLibraryBranches(base):
    # see: https://data.cityofchicago.org/Education/Libraries-Locations-Hours-and-Contact-Information/x8fc-8rcq
    __tablename__ = "ChicagoLibraryBranches"

    BranchName = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    PhoneNumber = sqlalchemy.Column(sqlalchemy.String)
    Address = sqlalchemy.Column(sqlalchemy.String)
    City = sqlalchemy.Column(sqlalchemy.String)
    Zip = sqlalchemy.Column(sqlalchemy.String)
    Website = sqlalchemy.Column(sqlalchemy.String)
