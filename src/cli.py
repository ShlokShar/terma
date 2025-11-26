
"""
cli.py — provides the command-line interface (CLI) for interacting with the application.

- start_server() -> bool: initiates the server that hosts the Terma agent if the client / server socket is not alive.
- execute_command() -> None: forwards user prompt to Terma agent using a client / server socket, in which the Terma
agent exists within the server.
"""

import socket
import subprocess
import time

import typer
from typing import List
from typing_extensions import Annotated

import src.commands.config as config

HOST = "127.0.0.1"
PORT = 7313


app = typer.Typer()
app.add_typer(config.app, name="config")


def start_server() -> bool:
    """
    initiates the server that hosts the Terma agent if the client / server socket is not alive.

    :return: True if the client / server socket is alive, False if otherwise
    """

    client_socket = socket.socket()
    try:
        client_socket.connect((HOST, PORT))
        return True
    except socket.error:
        subprocess.Popen(["python3", "src/terma.py"])
        for _ in range(50):
            try:
                client_socket.connect((HOST, PORT))
                return True
            except socket.error:
                time.sleep(0.1)
        return False
    finally:
        client_socket.close()
        return False


@app.command(name="exec")
def execute_command(args: List[str]) -> None:
    """
    forwards user prompt to Terma agent using a client / server socket, in which the Terma
    agent exists within the server.

    :param args: the user's prompt in natural language (e.g. reinstall node packages)
    :return: None, prints out suggested shell command
    """

    prompt = " ".join(args)
    start_server()
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    client_socket.send((prompt + "\n").encode())

    response = client_socket.recv(1024).decode()
    client_socket.close()
    print(response)
    run_commands = typer.prompt("\nExecute command(s)? [y/N]")
    run_commands = run_commands.lower()

    # execute command(s) if user confirms prompt
    if run_commands == "y" or run_commands == "yes":
        subprocess.run(response, shell=True, text=True)
    print("")


if __name__ == "__main__":
    app()
