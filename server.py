from concurrent.futures import thread
from dataclasses import dataclass
from socket import create_server, socket, AF_INET, SOCK_STREAM, timeout
from threading import Thread
import TeamnetworkTactics as TNT
from core import Champion
import pickle

# Recieves champions from database (in encoded form)
# TODO: Finish this intermediary connection,
# Temporarily, a direct connection db to client is used.

# PICKLE https://stackoverflow.com/questions/6341823/python-sending-dictionary-through-tcp


class Game:
    def __init__(this, players):
        this._players = players
        this._player1 = [players[0], 1]
        this._player2 = [players[1], 2]
        this._player1Champs = []
        this._player2Champs = []
        this._checklist = []
        this._champions = TNT.champions
        this._count = 1

    def messageToAll(this, data):
        for conn in this._players:
            message = pickle.dumps(data)
            conn.send(message)

    def _sendMessage(this, data, connection):
        message = pickle.dumps(data)
        connection.send(message)

    def startGame(this) -> None:
        print(f"PLAYERS {this._players} ")
        print("starting game")
        print(f"PLAYER 1: {this._player1[0]} PLAYER 2 {this._player2[0]}")
        data = {"TODO": "PrintChamps",
                "Champions": this._champions}

        this.messageToAll(data)

        Thread(target=this.getChampions, args=(this._player1,)).start()
        Thread(target=this.getChampions, args=(this._player2, )).start()

    def getChampions(this, playerList):
        print(f"[GETCHAMPIONS] {playerList}")
        if playerList[1] == 1:

            color = "red"
            playernum = 1
            print(f"{playerList} is player 1 ")

        if playerList[1] == 2:

            color = "blue"
            playernum = 2
            print(f"{playerList} is player 2")
        data = {"TODO": "InputChamps",
                "info": {"playername": "Player" + str(playernum),
                         "color": color,
                         "champions": this._champions,
                         "player1": this._player1Champs,
                         "player2": this._player2Champs,
                         "playernum": playernum}
                }

        while True:
            this._sendMessage(data, playerList[0])

            playerdata = playerList[0].recv(4096)

            if not playerdata:
                continue
            message = pickle.loads(playerdata)
            print(message)

    def championCheck(this, player, champ):
        while True:
            champ = player[0].recv(2048).decode()
            if player[1] == 1:
                this._player1Champs.append(champ)
                print(this._player1Champs)

            else:
                this._player2Champs.append(champ)
                print(this._champions)
            break

        # if champ in this._checklist:
        #     print("Champ is in checklist")
        #     inList = "CHAMPSELECTDONE"

        # else:
        #     this._checklist.append(champ)
        #     if player[1] == 1:
        #         this._player1Champs.append(champ)
        #     if player[1] == 2:
        #         this._player2Champs.append(champ)
        #     print(f"{player} Champion added!")
        #     print(this._checklist)
        #     print(f"Player 1 {this._player1Champs}")
        #     print(f"Player 2 {this._player2Champs}")

        # break


class ClientThread:
    def __init__(this, host: str, port: int):
        this._host = host
        this._port = port
        this._connections = []

    def startUpServer(this):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind((this._host, this._port))
            sock.listen()

            while True:

                conn, _ = sock.accept()
                this._connections.append(conn)

                if (len(this._connections) == 2):
                    print(f"[CONNECTIONS] {this._connections}")
                    game = Game(this._connections)
                    game.startGame()


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5002
    mainServer = ClientThread(HOST, PORT)
    mainServer.startUpServer()
