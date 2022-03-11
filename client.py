import socket
import TeamnetworkTactics as TNT
import pickle


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
            data = this._server.recv(4096)

            if not data:
                continue

            message = pickle.loads(data)

            if message["TODO"] == "PrintChamps":
                print(TNT.print_available_champs(message["Champions"]))
            elif message["TODO"] == "InputChamps":

                print("Inputchamps")
            elif message["TODO"] == "MatchSummary":
                print("matchsummary")


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 5002
    TnT = Client(HOST, PORT)
    TnT.connectToServer()
