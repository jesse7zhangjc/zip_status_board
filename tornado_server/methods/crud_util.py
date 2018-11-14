"""
Database CRUD Utils
"""

from torndb import Connection
from db_config.mysql_creds import MYSQL_USERNAME, MYSQL_PASSWORD, DATABASE_NAME

MYSQL_SETTINGS = {
    'host': '127.0.0.1',
    'user': MYSQL_USERNAME,
    'password': MYSQL_PASSWORD,
    'database': DATABASE_NAME,
    'charset': 'utf8'
}

# ROOT_CONNECT = Connection(host='127.0.0.1',
#                           user=MYSQL_USERNAME,
#                           password=MYSQL_PASSWORD,
#                           database=DATABASE_NAME,
#                           charset='utf8')


def execute_query(query, **kw_dict):
    """Execute query
    """
    conn = Connection(**MYSQL_SETTINGS)
    if kw_dict is None:
        try:
            result = conn.execute(query)
            conn.close()
            return result
        except Exception, e:
            print e
    else:
        try:
            result = conn.execute(query, **kw_dict)
            conn.close()
            return result
        except Exception, e:
            print e

def get_query_result(query, **kw_dict):
    """get query result
    """
    conn = Connection(**MYSQL_SETTINGS)
    if kw_dict is None:
        try:
            result = conn.query(query)
            conn.close()
            return result
        except Exception, e:
            print e
    else:
        try:
            result = conn.query(query, **kw_dict)
            conn.close()
            return result
        except Exception, e:
            print e