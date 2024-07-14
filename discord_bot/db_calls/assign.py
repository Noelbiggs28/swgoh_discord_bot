import psycopg2
import os
def assign_plan():
    HOST = open("db_ip_addr").read().rstrip()
    PORT = os.environ.get('PORT')
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    DATABASE = "swgoh_database"
    with psycopg2.connect(
    host=HOST,
    port=PORT,  
    database=DATABASE,
    user = USER,
    password = PASSWORD

    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * from playerunits""")
            units = cursor.fetchall()
    conn.close()
    print(units)
    message="done"
        
    return message