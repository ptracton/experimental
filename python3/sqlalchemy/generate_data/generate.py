#! /usr/bin/env python3

import json
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import ORM


if __name__ == "__main__":

    json_file = open("dataMar-23-2018.json")
    json_data = json.load(json_file)


    Session = sqlalchemy.orm.sessionmaker(ORM.db)
    session = Session()
    ORM.base.metadata.create_all(ORM.db)

    index = 0
    for x in json_data['data']:
        print("{} {} {} {} {} {} {} {} {} {} {} {}".format(
            index, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10]))
        if index > 0:
            person = ORM.People()
            person.PersonalNumber = x[0]
            person.FirstName = x[1]
            person.LastName = x[2]
            person.StreetAddress = x[3]
            person.City = x[4]
            person.Region = x[5]
            person.Zip = x[6]
            person.Country = x[7]
            person.Pin = x[8]
            person.Date = str(x[9])
            person.Email = x[10]
            try:
                session.add(person)
                session.commit()
            except:
                print("FAIL on {}".format(x))

            del (person)
        index = index + 1

