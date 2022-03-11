import socket
import pickle
from core import Champion, Match, Shape
from rich import print
from rich.prompt import Prompt
from rich.table import Table

def print_available_champs(champions: dict[Champion]) -> None:

    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)

    print(available_champs)


def input_champion(prompt: str,
                   color: str,
                   champions: dict[Champion],
                   player1: list[str],
                   player2: list[str]):

    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    while True:
        match Prompt.ask(f'[{color}]{prompt}'):
            case name if name not in champions:
                print(f'The champion {name} is not available. Try again.')
            case name if name in player1:
                print(f'{name} is already in your team. Try again.')
            case name if name in player2:
                print(f'{name} is in the enemy team. Try again.')
            case _:
                return name


def print_match_summary(match: Match) -> None:
    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        print(round_summary)
        print('\n')

    # Print the score
    red_score, blue_score = match.score
    print(f'Red: {red_score}\n'
          f'Blue: {blue_score}')
    f'Blue: {blue_score}'
    # Print the winner
    if red_score > blue_score:
        print('\n[red]Red victory! :grin:')
    elif red_score < blue_score:
        print('\n[blue]Blue victory! :grin:')
    else:
        print('\nDraw :expressionless:')


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
        this._server.close()

    def _sendMessage(this, data, connection):
        message = pickle.dumps(data)
        connection.send(message)

    def _recieveMessage(this):

        while True:
            data = this._server.recv(4096)

            if not data:
                continue

            message = pickle.loads(data)
            if message["TODO"] == "PrintChamps":
                print_available_champs(message["Champions"])
            if message["TODO"] == "InputChamps":
                for _ in range(3):

                    champion = input_champion(
                        str(message["info"]["playername"]), str(message["info"]["color"]), dict(message["info"]["champions"]), list[str](message["info"]["player1"]), list[str](message["info"]["player2"]))
                    this._champlist.append(champion)

                this._sendMessage(this._champlist, this._server)

            elif message["TODO"] == "MatchSummary":
                print_match_summary(message["match"])
                return


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 5002
    TnT = Client(HOST, PORT)
    TnT.connectToServer()
    TnT.disconnectServer()