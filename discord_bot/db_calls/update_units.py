import requests
from collections import defaultdict
import psycopg2
import os
def update_units():
    HOST = open("db_ip_addr").read().rstrip()
    PORT = os.environ.get('PORT')
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    DATABASE = "swgoh_database"


    def get_ally_codes():
        with psycopg2.connect(
        host=HOST,
        port=PORT,   # whatever port postgres is running on
        database=DATABASE,
        user=USER,
        password=PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("select ally_code, player_name from players")
                ally_codes = cursor.fetchall()
        conn.close()
        
        return [(ally_code[0],ally_code[1]) for ally_code in ally_codes] if ally_codes else "0 Players"

    
    def get_swgoh_player_data(ally_codes):
        all_units = []
        for code in ally_codes:

            url = f"https://swgoh.gg/api/player/{code[0]}/"
        
            try:
                response = requests.get(url)
                response.raise_for_status()  
                data = response.json()

                for unit in data['units']:
                    name = unit['data']['name']
                    combat_type = unit['data']['combat_type']
                    rarity = unit['data']['rarity']
                    if combat_type == 2:
                        relic = 0
                        if rarity == 7:
                            relic = 100
                        all_units.append((code[1],name, relic, rarity)) 
                    if combat_type == 1:
                        relic = unit['data']['relic_tier'] - 2
                        all_units.append((code[1],name,relic,rarity))


            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                return None
        return all_units
    allies = get_ally_codes()
    all_units_list = get_swgoh_player_data(allies)
    

    with psycopg2.connect(
    host=HOST,
    port=PORT,   
    database=DATABASE,
    user="postgres",
    password="password") as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM PLAYERUNITS;")
            for unit in all_units_list:
                cursor.execute("INSERT INTO PLAYERUNITS (player_name, character_name, relic, rarity) VALUES (%s, %s, %s, %s);", (unit[0],unit[1],unit[2],unit[3]))
            
            conn.commit()

    return "complete"

if __name__ == "__main__":
    update_units()

