import psycopg2
import os
def jedi_plan():
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
            cursor.execute("""SELECT a.planet, a.character_name, operations, a.phase, a.r_value, a.count
                            FROM(
                            SELECT p.planet, p.character_name, STRING_AGG(p.operations::VARCHAR, ', ') AS operations, p.phase, u.r5, u.r6, u.r7,
                                    COUNT(*) AS count,
                                    CASE 
                                        WHEN p.phase = 1 THEN u.r5
                                        WHEN p.phase = 2 THEN u.r6
                                        WHEN p.phase = 3 THEN u.r7
                                        ELSE u.r8
                                    END AS r_value
                            FROM platoons p 
                            LEFT JOIN units u ON p.character_name = u.character_name
                            WHERE p.phase < 4  
                            AND NOT EXISTS (
                                SELECT 1
                                FROM platoons p2 
                                LEFT JOIN units u2 ON p2.character_name = u2.character_name
                                WHERE p2.phase < 4
                                    AND (
                                    (p.phase = 1 AND (u2.r5 IS NULL OR u2.r5 = 0))
                                    OR (p.phase = 2 AND (u2.r6 IS NULL OR u2.r6 = 0))
                                    OR (p.phase = 3 AND (u2.r7 IS NULL OR u2.r7 = 0))
                                    OR (p.phase = 4 AND (u2.r8 IS NULL OR u2.r8 = 0))
                                    OR (p.phase > 4 AND (u2.r9 IS NULL OR u2.r9 = 0))
                                )
                                AND p2.operations = p.operations
                                AND p2.planet = p.planet
                            )
                            GROUP BY p.planet,p.character_name,p.phase, u.r5, u.r6, u.r7, u.r8
                            ) as a
                            WHERE a.r_value < a.count
                            ORDER BY a.planet
                            ;""")
            units = cursor.fetchall()
    conn.close()
    needed_units = {'needed_units': units if units else "doable"}
    if needed_units['needed_units']== "doable":
        return "all misions doable"
    message = f"Units where we have less than needed after subtracting impossible missions\n"
    planets = set()
    for unit in needed_units['needed_units']:
        relic_words = "Relic 5+" if unit[3] == 1 else "Relic 6+" if unit[3] == 2 else "Relic 7+" if unit[3] == 3 else "Relic 8+" if unit[3] == 4 else "relic 9"
        planets.add((unit[0],relic_words))
    planet_names = ['Mustafar', 'Corellia', 'Coruscant', 'Geonosis', 'Felucia', 'Bracca', 'Dathomir', 'Tatooine', 'Kashyyyk', 'Zeffo']# 'Haven-class Medical Station', 'Kessel', 'Lothal', 'Malachor', 'Vandor', 'Ring of Kafrene', 'Death Star', 'Hoth', 'Scarif']
    order_index = {planet: index for index, planet in enumerate(planet_names)}
    sorted_planets = sorted(planets, key=lambda x: order_index[x[0]])

    for planet in sorted_planets:
        message += f'{planet[0]}\n{planet[1]}\n'
        for unit in needed_units['needed_units']:
            if unit[0] == planet[0]:
                message += f"Unit: {unit[1]}, Have: {unit[4]} Need: {unit[5]} Operations: {''.join(unit[2])}\n"
        message +="\n"
        
    return message