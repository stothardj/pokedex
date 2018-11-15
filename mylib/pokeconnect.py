import psycopg2
from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    print('reading config')
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for k,v in params:
            db[k] = v
    else:
        raise Exception('Section {0} not fount in the {1} file'.format(section, filename))
    return db

class PokeConnect(object):
    def __init__(self):
        self.conn = None

    def __enter__(self):
        params = config()
        print('connecting to db')
        self.conn = psycopg2.connect(**params)
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        if self.conn:
            print('closing connection to db')
            self.conn.close()
