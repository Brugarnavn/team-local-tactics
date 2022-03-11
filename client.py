import socket
import TeamnetworkTactics as TNT
import pickle


class Client:
    def __init__(this, host, port):
        this._host = host
        this._port = port
        this._champlist = []

    def connectToServer(this):
        this._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this._server.connect((this._host, this._port))
        print("[CONNECTED] Connected to server")

        this._recieveMessage()

    def disconnectServer(this) -> None:
        this._server.close((this._host, this._port))

    def _sendMessage(this, data, connection):
        message = pickle.dumps(data)
        connection.send(message)

    def _recieveMessage(this):

        while True:
            data = this._server.recv(4096)

            if not data:
                continue

            message = pickle.loads(data)
            print(message)
            if message["TODO"] == "PrintChamps":
                print(TNT.print_available_champs(message["Champions"]))
            if message["TODO"] == "InputChamps":
                for _ in range(3):

                    champion = TNT.input_champion(
                        str(message["info"]["playername"]), str(message["info"]["color"]), dict(message["info"]["champions"]), list[str](message["info"]["player1"]), list[str](message["info"]["player2"]))
                    this._champlist.append(champion)
                print(this._champlist)
                this._sendMessage(this._champlist, this._server)

            elif message["TODO"] == "MatchSummary":
                print("matchsummary")


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 5002
    TnT = Client(HOST, PORT)
    TnT.connectToServer()
