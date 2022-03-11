from concurrent.futures import thread
from dataclasses import dataclass
from socket import create_server, socket, AF_INET, SOCK_STREAM, timeout
from threading import Thread
import TeamnetworkTactics as TNT
from core import Match, Team
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
        data = {"TODO": "PrintChamps",
                "Champions": this._champions}

        this.messageToAll(data)

        t1 = Thread(target=this.getChampions, args=(this._player1,))
        t2 = Thread(target=this.getChampions, args=(this._player2, ))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        match = this.createMatch()
        match.play()

        dataResult = {
            "TODO": "MatchSummary",
            "match": match
        }
        this._sendMessage(dataResult, this._player1[0])
        this._sendMessage(dataResult, this._player2[0])

    def getChampions(this, playerList):
        if playerList[1] == 1:

            color = "red"
            playernum = 1

        if playerList[1] == 2:

            color = "blue"
            playernum = 2
        data = {"TODO": "InputChamps",
                "info": {"playername": "Player" + str(playernum),
                         "color": color,
                         "champions": this._champions,
                         "player1": this._player1Champs,
                         "player2": this._player2Champs,
                         "playernum": playernum}
                }

        this._sendMessage(data, playerList[0])
        playerdata = playerList[0].recv(4096)

        message = pickle.loads(playerdata)
        if playerList[1] == 1:
            this._player1Champs = message
        else:
            this._player2Champs = message

    def championCheck(this, player, champ):
        while True:
            champ = player[0].recv(2048).decode()
            if player[1] == 1:
                this._player1Champs.append(champ)

            else:
                this._player2Champs.append(champ)
            break

    def createMatch(this):
        match = Match(
            Team([this._champions[name] for name in this._player1Champs]),
            Team([this._champions[name] for name in this._player2Champs])
        )
        return match


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
