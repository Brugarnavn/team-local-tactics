from core import Champion
import mysql.connector

db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="champions"
)

my_database = db_connection.cursor()
sql_statement = "SELECT * FROM champions"
my_database.execute(sql_statement)
output = my_database.fetchall()


def _parse_champ(row):
    return Champion(row[1], float(row[2]), float(row[3]), float(row[4]))


def load_some_champs():
    champions = {}
    
    for row in output:
        champ = _parse_champ(row)
        champions[champ.name] = champ
    return champions