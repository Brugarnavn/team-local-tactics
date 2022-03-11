from concurrent.futures import thread
from dataclasses import dataclass
from socket import create_server, socket, AF_INET, SOCK_STREAM, timeout
import TeamnetworkTactics as TNT
from core import Champion
import pickle
# Recieves champions from database (in encoded form)
# TODO: Finish this intermediary connection,
# Temporarily, a direct connection db to client is used.

# PICKLE https://stackoverflow.com/questions/6341823/python-sending-dictionary-through-tcp


class Game:
    def __init__(this, players):
        this._players = [players[0], players[1]]
        this._player1 = players[0]
        this._player2 = players[1]
        this._player1Champs = []
        this._player2Champs = []
        this._checklist = []
        this._champions = TNT.champions

    def messageToAll(this, data):
        for conn in this._players:
            message = pickle.dumps(data)
            conn.send(message)

    def _sendMessage(this, data, connection):
        message = pickle.dumps(data)
        connection.send(message)

    def startGame(this) -> None:
        print("starting game")
        print(f"PLAYER 1: {this._player1} PLAYER 2 {this._player2}")
        data = {"TODO": "PrintChamps",
                "Champions": this._champions}

        this.messageToAll(data)

    # def getChampions(this, players):

    #     if this._players["players"] == players[0]:
    #         connectionOrder = 0
    #         sendTo = 1
    #         color = "red"
    #         playernum = 1
    #     else:
    #         connectionOrder = 1
    #         sendTo = 0
    #         color = "blue"
    #         playernum = 2

    #     data = {"TODO": "INPUTCHAMPS",
    #             "info": {"playername": "Player" + str(playernum),
    #                      "color": color,
    #                      "champions": this._champions,
    #                      "player1": this._player1Champs,
    #                      "player2": this._player2Champs}

    #     this._sendMessage(
    #         this._players[connectionOrder], serialized, sendTo)

    # Først få input fra player1 & player2 for champions
    # TNT.input_champion()


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
