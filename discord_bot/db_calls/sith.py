import psycopg2
import os
def sith_plan():
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
            cursor.execute("""SELECT 
                                p.planet, 
                                p.operations, 
                                STRING_AGG(p.character_name, ', ') AS character_names
                            FROM 
                                platoons p
                            LEFT JOIN 
                                units u ON p.character_name = u.character_name
                            WHERE 
                                p.phase < 4
                            AND (
                                (p.phase = 1 AND (u.r5 IS NULL OR u.r5 = 0))
                                OR (p.phase = 2 AND (u.r6 IS NULL OR u.r6 = 0))
                                OR (p.phase = 3 AND (u.r7 IS NULL OR u.r7 = 0))
                                OR (p.phase = 4 AND (u.r8 IS NULL OR u.r8 = 0))
                                OR (p.phase > 4 AND (u.r9 IS NULL OR u.r9 = 0))
                            )
                            GROUP BY 
                                p.planet,
                                p.phase,
                                p.operations
                                
                            ORDER BY 
                                p.operations;""")
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
                planets[planet].append((unit[1],"".join(unit[2])))

        if len(planets[planet]) > 0:
            message += f'{planet}\n{relic_words}\n'
            for pair in planets[planet]:
                message+=f'Operation: {pair[0]} {pair[1]}\n'

        relics += 1
        message +="\n"
    return message