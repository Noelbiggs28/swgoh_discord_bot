import requests
from collections import defaultdict
import psycopg2
import os
def update_roster():
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
                cursor.execute("select ally_code from players")
                ally_codes = cursor.fetchall()
        conn.close()
        return {'ally_codes': [ally_code[0] for ally_code in ally_codes] if ally_codes else "0 Players"}

    
    def get_swgoh_player_data(ally_codes):
        all_units = {"r5": defaultdict(int),"r6": defaultdict(int),"r7": defaultdict(int),"r8": defaultdict(int),"r9": defaultdict(int)}
        for code in ally_codes:
            print(code)
            url = f"https://swgoh.gg/api/player/{code}/"
        
            try:
                response = requests.get(url)
                response.raise_for_status()  
                data = response.json()
                for unit in data['units']:
                    name = unit['data']['name']
                    combat_type = unit['data']['combat_type']
                    rarity = unit['data']['rarity']
                    if combat_type == 2 and rarity == 7:
                        all_units['r5'][name] +=1 
                        all_units['r6'][name] +=1 
                        all_units['r7'][name] +=1 
                        all_units['r8'][name] +=1 
                        all_units['r9'][name] +=1 
                    if combat_type == 1:
                        relic = unit['data']['relic_tier'] - 2
                        if relic >= 5:
                            all_units['r5'][name] +=1 
                        if relic >= 6:
                            all_units['r6'][name] +=1 
                        if relic >= 7:
                            all_units['r7'][name] +=1 
                        if relic >= 8:
                            all_units['r8'][name] +=1 
                        if relic >= 9:
                            all_units['r9'][name] +=1 

            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                return None
        
        return all_units
    allies = get_ally_codes()["ally_codes"]
    all_units_dicts = get_swgoh_player_data(allies)
    

    with psycopg2.connect(
    host=HOST,
    port=PORT,   
    database=DATABASE,
    user="postgres",
    password="password") as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Units;")
            for unit_name in all_units_dicts['r5'].keys():
                r5 = all_units_dicts['r5'].get(unit_name, 0)
                r6 = all_units_dicts['r6'].get(unit_name, 0)
                r7 = all_units_dicts['r7'].get(unit_name, 0)
                r8 = all_units_dicts['r8'].get(unit_name, 0)
                r9 = all_units_dicts['r9'].get(unit_name, 0)
                cursor.execute("INSERT INTO Units (character_name, r5, r6, r7, r8, r9) VALUES (%s, %s, %s, %s, %s, %s);", (unit_name, r5, r6, r7, r8, r9))
            
            conn.commit()

    return "complete"

if __name__ == "__main__":
    update_roster()

