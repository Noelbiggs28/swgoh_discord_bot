import psycopg2
import os
def get_number(relic_level,character_name):
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
            cursor.execute(f"SELECT {relic_level} FROM units WHERE character_name ILIKE %s", (character_name,))
            number_of_units = cursor.fetchone()
    conn.close()
    return str(number_of_units[0]) if number_of_units else "0 Players"