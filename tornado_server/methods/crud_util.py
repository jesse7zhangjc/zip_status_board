"""
Database CRUD Utils
"""

from torndb import Connection
from db_config.mysql_creds import MYSQL_USERNAME, MYSQL_PASSWORD, DATABASE_NAME

ROOT_CONNECT = Connection(host='127.0.0.1',
                          user=MYSQL_USERNAME,
                          password=MYSQL_PASSWORD,
                          database=DATABASE_NAME,
                          charset='utf8')


def execute_query(query, conn=ROOT_CONNECT, **kw_dict):
    """Execute query
    """
    if kw_dict is None:
        try:
            return conn.execute(query)
        except Exception, e:
            print e
    else:
        try:
            return conn.execute(query, **kw_dict)
        except Exception, e:
            print e

def get_query_result(query, conn=ROOT_CONNECT, **kw_dict):
    if kw_dict is None:
        try:
            return conn.query(query)
        except Exception, e:
            print e
    else:
        try:
            return conn.query(query, **kw_dict)
        except Exception, e:
            print e