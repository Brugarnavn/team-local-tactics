from base64 import decode
from dataclasses import dataclass
from os import environ
from pydoc import cli
from random import random, shuffle
from socket import create_server, socket, AF_INET, SOCK_STREAM

import TeamnetworkTactics as TNT
import threading
from core import Variables, Champion
# Recieves champions from database (in encoded form)
# TODO: Finish this intermediary connection,
# Temporarily, a direct connection db to client is used.


class Game:
    def __init__(this, players):
        this._players = players
        this._player1Champs = []
        this._player2Champs = []
        this._checklist = []
        this._inputs = {
            "player": "",
            "color": "",
            "Champions": dict[Champion],
            "player1": this._player1Champs,
            "player2": this._player2Champs
        }

    def sendChampions(this, connection):

        while True:
            msg = connection.recv(1024).decode()
            if msg == "GIVECHAMP":
                pass

    # Først få input fra player1 & player2 for champions
    # TNT.input_champion()

    def _createPlayers(this):
        print("Creating Player")
        for conn in this._players:
            conn.send("PRINTCHAMPS".encode())
            data = conn.recv(1024).decode()
            if data == "GIVECHAMP":
                champion = conn.recv(1024).decode()
                while champion != "DONECHAMPSELECTION" and champion in TNT.champions:
                    this._checklist.append(champion)
                    if champion not in this._checklist:
                        continue
                    else:
                        conn.send("CHAMPTAKEN".encode())

        this._player2.send("INPUTCHAMPS".encode())


class ClientThread:
    def __init__(this, host: str, port: int):
        this._host = host
        this._port = port
        this._connections = []

    def clientHandler(conn, addr):
        with conn:
            print(conn, addr)
            while True:
                data = conn.recv(1024)
                print(data)

                if not data:
                    break
            conn.sendall(data)

    def messageToClient(client, codename):  # Uten data som skal sendes
        if codename == "printChamps":

            client.send(codename.encode())
            print(f"[CODENAME] printChampion has been sent to {client}")

        elif codename == "inputChamps":
            client.send(codename.encode())
            print(f"[CODENAME] inputChamps has been sent to {client}")

    def messageToClient(client, codename, data):  # Med data som skal sendes
        if codename == "printChamps":

            client.send(codename.encode())
            print(f"[CODENAME] printChampion has been sent to {client}")
            client.send(data.encode())

        elif codename == "inputChamps":
            count = 0
            client.send(codename.encode())
            response = client.recv(1024)

            if response == "First?":
                count += 1
                if count == 1:
                    client.send("You are first!".encode())
                else:
                    client.send("You are not first!".encode())

            print(f"[CODENAME] inputChamps has been sent to {client}")

    def _threadingClients(this) -> None:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind((this._host, this._port))
            s.listen()

            while True:
                conn, addr = s.accept()
                print(f"[CONNECTION] {addr}")
                this._connections.append(conn)
                threading.Thread(args=(conn, addr)).start()

                if (len(this._connections) == 2):
                    print(
                        "[CONNECTION] Two player has connected, game can begin..")
                    game = Game(this._connections)
                    game._createPlayers()


class Server:
    def __init__(this):
        this._connections = []

    def _messageToClient(conn, data) -> None:
        socket.sendto(data.encode('utf-8'), conn)

    def _getMessageFromClient(conn):
        while True:
            data = conn.recv(1024)
            if data:
                msg = data.decode()
                return msg


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5002
    mainServer = ClientThread(HOST, PORT)
    mainServer._threadingClients()
