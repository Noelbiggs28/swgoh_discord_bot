import psycopg2
import os
def sith2_plan():
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
            cursor.execute("""
WITH playersunits AS(
Select character_name, max(relic) as maxrelic from playerunits
group by character_name
)
SELECT p.planet,p.phase, p.operations, p.character_name, maxrelic
FROM platoons p
LEFT JOIN playersunits pu ON p.character_name=pu.character_name
WHERE p.phase < 4
AND p.planet !='Zeffo'
AND maxrelic < p.phase+4
GROUP BY p.phase,p.planet, p.operations, p.character_name, maxrelic
;""")
            units = cursor.fetchall()
    conn.close()    
    
    results = {'impossible_ops': units if units else "doable"}
    
    if results['impossible_ops']== "doable":
        return "all missions doable"
    message = f""
    relics = 1
    planets = {'Mustafar':[], 'Corellia':[], 'Coruscant':[], 'Geonosis':[], 'Felucia':[], 'Bracca':{}, 'Dathomir':[], 'Tatooine':[], 'Kashyyyk':[]}# 'Zeffo', 'Haven-class Medical Station', 'Kessel', 'Lothal', 'Malachor', 'Vandor', 'Ring of Kafrene', 'Death Star', 'Hoth', 'Scarif']
    for planet in planets.keys():
        relic_words = "Relic 5+" if relics < 4 else "Relic 6+" if relics < 7 else "relic 7+"
 
        for unit in results['impossible_ops']:
            if unit[0] == planet:
                planets[planet].append((unit[2],"".join(unit[3])))

        if len(planets[planet]) > 0:
            message += f'{planet}\n{relic_words}\n'
            for pair in planets[planet]:
                message+=f'Operation: {pair[0]} {pair[1]}\n'

        relics += 1
        message +="\n"
    return message