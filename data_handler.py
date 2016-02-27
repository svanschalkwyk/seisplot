import psycopg2

#!/usr/bin/python
from psycopg2._psycopg import connection

hostname = 'localhost'
username = 'postgres'
password = 'postgres'
database = 'seisplot'
connection = None

table = \
"CREATE SEQUENCE user_id_seq;" \
"CREATE  TABLE public.nav_meta (" \
"  id bigint NOT NULL DEFAULT nextval('user_id_seq')," \
"  year int NOT NULL," \
"  day int NOT NULL," \
"  hr int NOT NULL," \
"  min int NOT NULL," \
"  sec int NOT NULL," \
"  latlon point NOT NULL," \
"  utmx float NOT NULL," \
"  utmy float NOT NULL," \
"  lineid char(6) NOT NULL," \
"  cmp int NOT NULL," \
"  ffid int NOT NULL," \
"  PRIMARY KEY (year,lineid,cmp,ffid));" \
"  ALTER SEQUENCE user_id_seq OWNED BY nav_meta.id;"   \
"  ALTER TABLE nav_meta OWNER TO postgres; GRANT SELECT ON TABLE nav_meta TO public;"

def createTable() :
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(table)

def insertLine(year, day, hr, min, sec, latlon, utmx, utmy, lineid, cmp, ffid) :
    conn = get_connection()
    cur = conn.cursor()
    cur.execute( "INSERT INTO nav_meta (year, day, hr, min, sec, latlon, utmx, utmy, lineid, cmp, ffid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
       (year, day, hr, min, sec, latlon, utmx, utmy, lineid, cmp, ffid))

def get_connection():
    global connection
    if not connection:
        connection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    #if connection.closed :
    #    connection.
    return connection

def commit_and_close() :
    conn = get_connection()
    conn.commit()
    #conn.close()



if __name__ == "__main__":
    print("Using psycopg2")
    createTable()
    connection.commit()
    connection.close()
