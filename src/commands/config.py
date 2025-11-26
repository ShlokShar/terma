
"""
config.py — provides the functions used for the config command.

- set_provider(provider: Annotated[str, typer.Argument()] = None, api_key: str = None) -> None:
sets the provider, model, and API key for Terma's configuration.
- set_api_key(api_key: str = None) -> None: sets the API key for the current configuration.
- set_model(model: str = None) -> None: sets the AI model for the current configuration.
- peek() -> None: prints Terma's current configuration
"""

import typer
from typing_extensions import Annotated, Optional

from src.util.helpers import check_provider, highlight, list_providers, mask_api, raise_exception, PROVIDERS
from src.util.io import has_config, load_config, save_config

app = typer.Typer()


@app.command(name="provider", help="sets the provider, model, and API key for Terma's configuration.")
def set_provider(provider: Annotated[str, typer.Argument()] = None, api_key: str = None) -> None:
    """
    sets the provider, model, and API key for Terma's configuration.
    :param provider: name of provider
    :param api_key: value of provider's API key
    :return: None
    """

    if not provider:
        provider = typer.prompt("Provider")

    # check if provider is invalid
    if not check_provider(provider):
        exception_message = "Invalid provider.\n" \
                            f"> Choose from one of the following providers:\n" + list_providers()
        raise_exception(exception_message)

    # set the rest of the configuration
    if not api_key:
        api_key = typer.prompt("API Key")

    configuration = {
        "provider": provider,
        "model": PROVIDERS[provider][0],
        "api-key": api_key
    }
    save_config(configuration)

    print(f"Provider set to: {highlight(provider, 'GREEN')}")
    print(f"Model set to: {highlight(PROVIDERS[provider][0], 'GREEN')} (default)")
    print(f"API Key set to: {highlight(mask_api(api_key), 'GREEN')}\n")


@app.command(name="api-key", help="sets the API key for the current configuration.")
def set_api_key(api_key: str = None) -> None:
    """
    sets the API key for the current configuration.

    :param api_key: the API key to be updated in the configuration
    :return: None
    """
    # check if valid configuration is enabled
    if not has_config():
        exception_message = "Invalid configuration." \
                            f"> run \"{highlight('terma config provider <configuration>', 'OKCYAN')}\""
        raise_exception(exception_message)

    if not api_key:
        api_key = typer.prompt("API Key")

    # modify configuration's API key
    configuration = load_config()
    configuration["api-key"] = api_key
    save_config(configuration)

    print(f"API Key set to: {highlight(mask_api(api_key), 'GREEN')}\n")


@app.command(name="model", help="sets the AI model for the current configuration")
def set_model(model: Annotated[str, typer.Argument()] = None) -> None:
    """
    sets the AI model for the current configuration.

    :param model: name of the AI model
    :return: None
    """

    if not model:
        model = typer.prompt("Model")

    # check if model is invalid
    configuration = load_config()
    if model not in PROVIDERS[configuration.get("provider")]:
        message = "Invalid model name."
        raise_exception(message)

    configuration["model"] = model
    save_config(configuration)
    print(f"Model set to: {highlight(model, 'GREEN')}\n")


@app.command(name="peek", help="prints Terma's current configuration")
def peek() -> None:
    """
    prints Terma's current configuration.
    :return: None
    """

    configuration = load_config()
    print(f"Provider: {highlight(configuration['provider'], 'GREEN')}")
    print(f"Model: {highlight(configuration['model'], 'GREEN')}")
    print(f"API Key: {highlight(mask_api(configuration['api-key']), 'GREEN')}\n")
