import psycopg2
import os
def get_number(character_name):
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
            cursor.execute(f"SELECT player_name, relic, rarity  FROM playerunits WHERE character_name ILIKE %s order by relic desc,rarity desc", (character_name,))
            units = cursor.fetchall()
    conn.close()
    message=""
    for unit in units:
        message+=f"{unit[0]}: relic {unit[1]}, stars {unit[2]}\n"
    return message