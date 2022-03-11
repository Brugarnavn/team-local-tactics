from concurrent.futures import thread
from dataclasses import dataclass
from socket import create_server, socket, AF_INET, SOCK_STREAM, timeout
from threading import Thread
from core import Match, Team, Champion
import pickle

# PICKLE https://stackoverflow.com/questions/6341823/python-sending-dictionary-through-tcp


# Turns the stringn
def string_to_dict(string):
    ch_string = string.replace("'", "").split(")")[:-1]
    ch_dict = {}
    for champion in ch_string:
        name, rock, paper, scissors = champion.split(sep=',')
        ch_dict[name] = Champion(name, float(
            rock), float(paper), float(scissors))
    return ch_dict

# Recieves champions from database
def getChamps():
    sock = socket()
    sock.connect(("localhost", 6000))
    chString = sock.recv(2048).decode()
    sock.close()
    return chString


class Game:
    def __init__(this, players):
        this._players = players
        this._player1 = [players[0], 1]
        this._player2 = [players[1], 2]
        this._player1Champs = []
        this._player2Champs = []
        this._champions = string_to_dict(getChamps())

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