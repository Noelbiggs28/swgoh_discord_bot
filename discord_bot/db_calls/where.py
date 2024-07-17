import psycopg2
import os
def where_at(character_name):
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
            cursor.execute(f"Select planet, STRING_AGG(operations::VARCHAR, ', ') AS operations from platoons where character_name ilike %s and phase < 4 group by planet", (character_name,))
            units = cursor.fetchall()
    conn.close()
    message=""
    for unit in units:
        message+=f"{unit[0]} {''.join(unit[1])}\n"
    return message