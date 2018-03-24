#! /usr/bin/env python3

import sqlalchemy


def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


if __name__ == "__main__":
    conn, meta = connect("postgres", "python", "postgres")
    print(conn)
    print(meta)
    
    slams = sqlalchemy.Table('slams', meta,
                             sqlalchemy.Column(
                                 'name', sqlalchemy.String, primary_key=True),
                             sqlalchemy.Column('country', sqlalchemy.String))
    
    results = sqlalchemy.Table('results', meta,
                               sqlalchemy.Column(
                                   'slam', sqlalchemy.String,
                                   sqlalchemy.ForeignKey('slams.name')),
                               sqlalchemy.Column('year', sqlalchemy.Integer),
                               sqlalchemy.Column('result', sqlalchemy.String))

    # Create the above tables
    meta.create_all(conn)
    for tables in meta.tables:
        print(tables)

    clause = slams.insert().values(name='Wimbledon', country='United Kingdom')
    conn.execute(clause)

    clause = slams.insert().values(name='Roland Garros', country='France')
    conn.execute(clause)

    victories = [{
        'slam': 'Wimbledon',
        'year': 2003,
        'result': 'W'
    }, {
        'slam': 'Wimbledon',
        'year': 2004,
        'result': 'W'
    }, {
        'slam': 'Wimbledon',
        'year': 2005,
        'result': 'W'
    }]

    conn.execute(meta.tables['results'].insert(), victories)


    results = meta.tables['results']
    for c in results.c:
        print(c)


    for row in conn.execute(results.select()):
        print(row)

    clause = results.select().where(results.c.year == 2005)    
    for row in conn.execute(clause):
        print(row)
