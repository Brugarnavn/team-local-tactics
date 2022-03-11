import socket
import TeamnetworkTactics as TNT
from core import Variables
import json


class Client:
    def __init__(this, host, port):
        this._host = host
        this._port = port

    def connectToServer(this):
        this._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this._server.connect((this._host, this._port))
        print("[CONNECTED] Connected to server")
        while True:
            this._recieveMessage()

    def disconnectServer(this) -> None:
        this._server.close((this._host, this._port))

    def _recieveMessage(this):

        while True:
            msg = this._server.recv(1024).decode()

            if not msg:
                continue
            else:
                if msg == "PRINTCHAMPS":
                    TNT.print_available_champs(TNT.champions)
                    continue
                elif msg == "INPUTCHAMPS":
                    this._server.send("GIVECHAMP".encode)
                    for _ in range(3):
                        while msg != "CHAMPTAKEN":
                            try:
                                champion = input("Choose a champion: ")
                                this._server.send(champion)
                            except:
                                continue
                            else:
                                print("POOPSIEDAISY")
                                break

                elif msg == "printMatchSummary":
                    TNT.print_match_summary()


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 5002
    TnT = Client(HOST, PORT)
    TnT.connectToServer()
