import psycopg2
import os
def planet_check2(planet_name, all):
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
            cursor.execute("""SELECT  p.character_name, CASE 
                                        WHEN p.phase = 1 THEN COALESCE(u.r5,0)
                                        WHEN p.phase = 2 THEN COALESCE(u.r6,0)
                                        WHEN p.phase = 3 THEN COALESCE(u.r7,0)
                                        ELSE COALESCE(u.r8,0)
                                    END AS relic, COUNT(*) AS character_count
                            FROM platoons p
                            LEFT JOIN units u 
                            ON p.character_name = u.character_name
                            WHERE planet ILIKE %s
                            GROUP BY p.character_name, relic
                            ORDER BY CASE 
                                        WHEN p.phase = 1 THEN COALESCE(u.r5,0)
                                        WHEN p.phase = 2 THEN COALESCE(u.r6,0)
                                        WHEN p.phase = 3 THEN COALESCE(u.r7,0)
                                        ELSE COALESCE(u.r8,0)
                                    END;""",(planet_name,))
            units = cursor.fetchall()
        
    conn.close()
    planet_info = {'units': units if units else "No one's home..."}

    message = f'\nThe units for the whole planet\nunit, how many we have, how many we need\n'

    for unit in planet_info['units']:
        if all==True:
            if int(unit[1]) < int(unit[2]):
                message += f'{unit[0]}, {unit[1]}, {unit[2]}\n'
        else:
            message += f'{unit[0]}, {unit[1]}, {unit[2]}\n'
  
    return message
                                    