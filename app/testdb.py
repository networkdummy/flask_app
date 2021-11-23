import psycopg
sql="select * from shipment"
try:
    #connection=psycopg.connect("host='localhost' dbname='exercises' user='ist' password='ist'")
    connection=psycopg.connect('postgresql://ist:ist@localhost:5432/exercises')
    print(connection)
    print(sql)
    cursor=connection.cursor()
    cursor.execute(sql)
    colnames = [desc[0] for desc in cursor.description]
    print(colnames)
    rows=cursor.fetchall()
    print(cursor.fetchall())
    for x in rows:
        print(x)
except:
    print("error")
    print(psycopg.OperationalError)
