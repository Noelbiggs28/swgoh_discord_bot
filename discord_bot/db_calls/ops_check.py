import psycopg2
import os
def ops_check(planet_name):
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
            cursor.execute("""SELECT p.operations, STRING_AGG(p.character_name, ', ') AS character_names
                            FROM platoons p
                            LEFT JOIN units u ON p.character_name = u.character_name
                            WHERE p.planet ILIKE %s
                            AND (
                            (p.phase = 1 AND (u.r5 IS NULL OR u.r5 = 0))
                            OR (p.phase = 2 AND (u.r6 IS NULL OR u.r6 = 0))
                            OR (p.phase = 3 AND (u.r7 IS NULL OR u.r7 = 0))
                            OR (p.phase = 4 AND (u.r8 IS NULL OR u.r8 = 0))
                            OR (p.phase > 4 AND (u.r9 IS NULL OR u.r9 = 0))
                            )
                            GROUP BY p.operations
                            ORDER BY p.operations;""",(planet_name,))
            units = cursor.fetchall()
        
    conn.close()
    impossible_ops = {'impossible_ops': units if units else "doable"}

    message = ''
    if impossible_ops['impossible_ops'] == "doable":
        message += "all missions doable\n"
    else:
        message += f'\nOps that are impossible because we have none of these\nop, unit\n'
        for unit in impossible_ops['impossible_ops']:
            message += f"Operation: {unit[0]}, {''.join(unit[1])}\n"
  
    return message