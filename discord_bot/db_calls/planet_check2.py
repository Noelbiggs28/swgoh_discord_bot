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
            cursor.execute("""WITH aggregated_platoons AS (
    SELECT 
        p.character_name, 
        p.phase, 
        COUNT(*) AS needed
    FROM 
        platoons p
    WHERE 
        p.planet ILIKE %s
    GROUP BY 
        p.character_name, 
        p.phase  
)
SELECT 
    ap.character_name, 
    ap.needed, 
    COUNT(CASE WHEN pu.relic > ap.phase + 3 THEN 1 ELSE NULL END) AS character_count
FROM 
    aggregated_platoons ap
LEFT JOIN 
    playerunits pu ON ap.character_name = pu.character_name
GROUP BY 
    ap.character_name, 
    ap.needed
ORDER BY ap.needed;""",(planet_name,))
            units = cursor.fetchall()
        
    conn.close()
    planet_info = {'units': units if units else "No one's home..."}

    message = f'\nThe units for the whole planet\nunit, how many we have, how many we need\n'

    for unit in planet_info['units']:
        if all==True:
            if int(unit[2]) < int(unit[1]):
                message += f'{unit[0]}, {unit[2]}, {unit[1]}\n'
        else:
            message += f'{unit[0]}, {unit[2]}, {unit[1]}\n'
  
    return message
                                    