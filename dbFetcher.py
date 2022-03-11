import mysql.connector
from socket import socket


def load_some_champs():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="champions"
    )

    db = db_connection.cursor()
    get_names = "SELECT champion_names, rock_chance, paper_chance, scissor_chance FROM champions"
    db.execute(get_names)
    champions = str("".join(str(e)[1:] for e in db.fetchall()))
    return champions

champlist_encoded = load_some_champs().encode()

sock = socket()
sock.bind(("localhost", 6000))
sock.listen()

while True:
        conn, _ = sock.accept()
        conn.send(champlist_encoded)