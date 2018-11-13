"""
Set Up MySQL Databases
"""
from torndb import Connection
from sqlalchemy import create_engine
from db_config.mysql_creds import MYSQL_USERNAME, MYSQL_PASSWORD, DATABASE_NAME

ROOT_CONNECT_NEW_DB = Connection(host='127.0.0.1',
                                 user=MYSQL_USERNAME,
                                 password=MYSQL_PASSWORD,
                                 database='',
                                 charset='utf8')

PANDAS_SQL_ENGINE = create_engine('mysql://%s:%s@127.0.0.1/%s' % (MYSQL_USERNAME,
                                                                  MYSQL_PASSWORD,
                                                                  DATABASE_NAME),
                                  encoding='utf8')

def create_new_db(conn=ROOT_CONNECT_NEW_DB, db_name=DATABASE_NAME):
    """Create db
    """
    db_obj = {'Database': db_name}
    # If db exists already, drop it and create it again
    if db_obj in conn.query('SHOW DATABASES'):
        conn.execute('DROP DATABASE %s' % db_name)
        print 'old db [%s] dropped.' % db_name

    # Create db
    conn.execute('CREATE DATABASE %s' % db_name)
    print 'new db [%s] created.'  % db_name


def create_new_tables(conn=PANDAS_SQL_ENGINE):
    """Create tables
    """
    from pandas import ExcelFile, read_excel
    data_excel = ExcelFile('./db_config/data.xlsx')
    # Import all sheets into MySQL
    for sheet in data_excel.sheet_names:
        df_temp = read_excel(data_excel, sheet_name=sheet, index_col='id')
        df_temp.to_sql(con=conn, name=sheet, if_exists='replace')
        conn.execute('ALTER TABLE %s MODIFY COLUMN id INT NOT NULL AUTO_INCREMENT' % sheet)
        print 'table [%s] imported.' % sheet


def set_up_mysql_db():
    """Set up Mysql DB Env
    """
    create_new_db()
    create_new_tables()
    print 'MySQL DB Env Ready to use!'
