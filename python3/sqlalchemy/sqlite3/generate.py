#! /usr/bin/env python3

import json
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import ORM


def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i) < 128)


if __name__ == "__main__":

    json_file = open("dataMar-23-2018.json", encoding='utf-8')
    json_data = json.load(json_file)

    Session = sqlalchemy.orm.sessionmaker(ORM.db)
    session = Session()
    ORM.base.metadata.create_all(ORM.db)

    index = 0
    for x in json_data['data']:
        # print("{} {} {} {} {} {} {} {} {} {} {} {}".format(
        #    index, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10]))
        if index > 0:
            person = ORM.People()
            person.PersonalNumber = remove_non_ascii(x[0])
            person.FirstName = remove_non_ascii(x[1])
            person.LastName = remove_non_ascii(x[2])
            person.StreetAddress = remove_non_ascii(x[3])
            person.City = remove_non_ascii(x[4])
            person.Region = remove_non_ascii(x[5])
            person.Zip = remove_non_ascii(x[6])
            person.Country = remove_non_ascii(x[7])
            person.Pin = remove_non_ascii(x[8])
            person.Date = str(x[9])
            person.Email = remove_non_ascii(x[10])
            try:
                session.add(person)
                session.commit()
            except:
                print("FAIL on {}".format(x))

            del (person)
        index = index + 1
