import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """Drop any existing tables from sparkifydb.

    Keyword arguments:
    * cur --    cursory to connected DB. Allows to execute SQL commands.
    * conn --   (psycopg2) connection to Postgres database (sparkifydb).

    Output:
    * Old sparkifydb database tables are dropped from AWS Redshift.
    """
    for query in drop_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print("Error: Issue dropping table: " + query)
            print(e)

    print("Tables dropped successfully.")

def create_tables(cur, conn):
    """Create new tables (songplays, users, artists, songs, time)
        to sparkifydb.

    Keyword arguments:
    * cur --    cursory to connected DB. Allows to execute SQL commands.
    * conn --   (psycopg2) connection to Postgres database (sparkifydb).

    Output:
    * New sparkifydb database tables are created into AWS Redshift.
    """
    for query in create_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print("Error: Issue creating table: " + query)
            print(e)
    print("Tables created successfully.")

def main():
    """Connect to AWS Redshift, create new DB (sparkifydb),
        drop any existing tables, create new tables. Close DB connection.

    Keyword arguments (from dwh.cfg):
    * host --       AWS Redshift cluster address.
    * dbname --     DB name.
    * user --       Username for the DB.
    * password --   Password for the DB.
    * port --       DB port to connect to.
    * cur --        cursory to connected DB. Allows to execute SQL commands.
    * conn --       (psycopg2) connection to Postgres database (sparkifydb).

    Output:
    * New sparkifydb is created, old tables are droppped,
        and new tables (songplays, users, artists, songs, time)
        are created..
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
