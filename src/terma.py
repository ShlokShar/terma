"""
agent.py — defines the Agent class and server functionality for the CLI tool
that converts natural language prompts into safe shell commands.

- cache_client() -> None: reinitiates the Terma agent object if there is a change in its configuration. Otherwise, the
object will be cached for future execution commands.
- main() -> None: sets up the server and listens for client (CLI) prompts. Then, forwards the prompt to the Terma agent
object and returns the proposed shell command to the client.
"""

import socket
import time

import click.exceptions

from src.util.exceptions import AuthenticationException, ConfigurationException, ProviderException
from src.util.helpers import highlight, raise_exception
from src.util.io import has_config, load_config, save_config

HOST = "127.0.0.1"
PORT = 7313
CACHE_DURATION = 10

file_structure = None
terma = None
last_client_update = None


class Terma:
    """
    Represents an AI agent that will convert natural language into shell commands.

    Attributes:
         - provider (str): the configured AI provider (i.e. "openai", "provider", or "google")
         - model (str): the specific model for the AI client (e.g. "gpt-4.1-nano", "claude-haiku-4-5",
         "gemini-2.0-flash-exp")
         - api_key (str): the API key for authenticating the AI client

    Methods:
        - process_prompt(self, prompt: str) -> str: processes the original natural language prompt and returns a
        proposed shell command using the configured provider and model.
        - _call_provider(self, provider: str, message: str) -> str: private method to query the AI client.
        - compare_config(self, configuration: dict) -> bool: returns True if the parameter configuration is equivalent
        to the Terma object's configuration.
        - @static get_file_structure(start_path: str=".", max_depth: str=3, max_entries: str=30) -> str: returns the
        file tree structure of the current working directory.
    """

    def __init__(self):
        # check if configuration is invalid
        if not has_config():
            raise ConfigurationException()

        configuration = load_config()
        self.provider = configuration.get("provider")
        self.model = configuration.get("model")
        self.api_key = configuration.get("api-key")

        self.client = None

        if self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        elif self.provider == "google":
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
        else:
            raise ProviderException

    def process_prompt(self, prompt: str) -> str:
        """
        processes the original natural language prompt and returns a proposed shell command using the configured
        provider and model.

        :param prompt: the natural language command prompt from the client
        :return: a string of the proposed shell command(s)
        """

        cwd_file_structure = Terma.get_file_structure()
        prompt_message = f"""
        You are a CLI tool that converts natural language into shell commands. 
        Respond with a one line valid shell command that fits the prompt's goal. 
        Do not generate commands that harm the system. 
        Do not provide explanations.
        Do not format.
        Here is the user's current file tree of the current directory:
        {cwd_file_structure}
        
        Here is the prompt:
        {prompt}
        """

        response = self._call_provider(self.provider, prompt_message)
        return response

    def _call_provider(self, provider: str, message: str) -> str:
        """
        private method to query the AI client.

        :param provider: the configured AI provider
        :param message: the instructions to be sent to the AI client including the prompt
        :return: the proposed shell command(s)
        """

        try:
            if provider == "openai":
                from openai import OpenAI
                response = self.client.responses.create(
                    model=self.model,
                    input=message,
                    max_output_tokens=100
                )
                response = response.output_text
            elif provider == "anthropic":
                from anthropic import Anthropic
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=100,
                    messages=[{
                        "role": "user",
                        "content": message
                    }]
                )
                response = response.content[0].text.strip()
            elif provider == "google":
                from google import genai
                from google.genai.errors import APIError
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=message
                )
                response = response.text.strip()
            else:
                raise ConfigurationException
            return response
        except:
            raise AuthenticationException

    def compare_config(self, configuration: dict) -> bool:
        """
        returns True if the parameter configuration is equivalent to the Terma object's configuration.

        :param configuration: the current configuration map from .config
        :return: True if the current .config matches the Terma agent's configuration
        """

        try:
            if (
                    configuration.get("provider") == self.provider and
                    configuration.get("model") == self.model and
                    configuration.get("api-key") == self.api_key
            ):
                return True
            return False
        except:
            return False

    @staticmethod
    def get_file_structure(start_path: str = ".", max_depth: int = 3, max_entries: int = 30) -> str:
        """
        returns the file tree structure of the current working directory.

        :param start_path: the path to start building the tree from; defaults to the CWD
        :param max_depth: the maximum depth for the file tree; defaults to 3
        :param max_entries: the maximum enteries for the file tree; defaults to 30
        :return: the file tree structure of the current working directory
        """

        import os
        tree_lines = []
        entry_count = 0

        def walk(dir_path, prefix="", depth=0):
            nonlocal entry_count
            if depth > max_depth or entry_count >= max_entries:
                return

            try:
                items = sorted(os.listdir(dir_path))
            except Exception:
                return

            for i, item in enumerate(items):
                if entry_count >= max_entries:
                    return

                full = os.path.join(dir_path, item)
                connector = "├── " if i < len(items) - 1 else "└── "
                tree_lines.append(f"{prefix}{connector}{item}")
                entry_count += 1

                if os.path.isdir(full):
                    new_prefix = prefix + ("│   " if i < len(items) - 1 else "    ")
                    walk(full, new_prefix, depth + 1)

        tree_lines.append(start_path)
        walk(start_path)
        return "\n".join(tree_lines)


def cache_client() -> None:
    """
    reinitiates the Terma agent object if there is a change in its configuration. Otherwise, the object will be cached
    for future execution commands.

    :return: None
    """

    global terma, last_client_update
    if last_client_update is None:
        last_client_update = time.time()
        terma = Terma()
    elif time.time() - last_client_update > CACHE_DURATION:
        last_client_update = time.time()
        configuration = load_config()
        if not terma.compare_config(configuration):
            terma = Terma()


def main() -> None:
    """
    sets up the server and listens for client (CLI) prompts. Then, forwards the prompt to the Terma agent object and
    returns the proposed shell command to the client.

    :return: None
    """

    global terma
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server_socket.settimeout(240)
    try:
        while True:
            cache_client()
            connection, address = server_socket.accept()
            data = connection.recv(1024).decode()
            response = terma.process_prompt(data)
            connection.send(response.encode())
            connection.close()

    except socket.timeout:
        server_socket.close()
    except ConfigurationException:
        exception_message = "Invalid configuration.\n" \
                            f"> run \"{highlight('terma config provider <configuration>', 'OKCYAN')}\""
        raise_exception(exception_message)
        server_socket.close()
    except AuthenticationException:
        exception_message = "Invalid API key.\n" \
                            f"> run \"{highlight('terma config api-key', 'OKCYAN')}\""
        raise_exception(exception_message)
        server_socket.close()
    except Exception:
        server_socket.close()


if __name__ == "__main__":
    try:
        main()
    except click.exceptions.Exit:
        pass
