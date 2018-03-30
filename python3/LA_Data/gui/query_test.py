#! /usr/bin/env python3
import json
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

import LACityData
import NYCityData
import ORM

if __name__ == "__main__":

    Session = sqlalchemy.orm.sessionmaker(ORM.db)
    session = Session()
    ORM.base.metadata.create_all(ORM.db)
    query = session.query(ORM.LALibraryBranches).all()
    print(query)
    for x in query:
        print(x.Zip)
    print(ORM.LALibraryBranches.__table__.columns.keys())
    
    for instance in session.query(ORM.LALibraryBranches).order_by(ORM.LALibraryBranches.BranchName):
        print(instance.BranchName, instance.Address)
