
"""
helpers.py — provides helper functions used in primary modules

- highlight(text: str, color: str) -> str: returns a formatted color coded string.
- check_provider(provider: str) -> bool: returns if prompted provider is valid.
- list_providers() -> str: returns a list of valid AI providers.
- raise_exception(text: str) -> exception: raises Typer exception with text message.
- mask_api(api_key: str) -> str: masks an API key value by only revealing the first four and last 6 characters.
"""

PROVIDERS = {
    "openai": [
        "gpt-4.1-nano",
        "gpt-4.1-mini",
        "gpt-4.1",
        "gpt-4o-mini",
        "gpt-4o",
        "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo-0301",
    ],
    "google": [
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.0-flash-exp",
        "gemini-2.5-pro",
    ],
    "anthropic": [
        "claude-haiku-4-5",
        "claude-haiku-4-3",
        "claude-sonnet-4-5",
        "claude-sonnet-4-3",
        "claude-opus-4-5",
        "claude-opus-4-3",
        "claude-haiku-3-5",
        "claude-sonnet-3-5",
    ],
}


def highlight(text: str, color: str) -> str:
    """
    returns a formatted color coded string.

    :param text: text to be color coded.
    :param color: color to highlight text with.
    :return: a formatted string that highlights the text argument.
    """

    from src.util.ansi import Colors
    return f"{getattr(Colors, color)}{text}{Colors.ENDC}"


def check_provider(provider: str) -> bool:
    """
    returns if prompted provider is valid.

    :param provider: a provider of the user's choosing.
    :return: returns True if the provider is valid for Terma, False if otherwise
    """

    return provider in PROVIDERS.keys()


def list_providers() -> str:
    """
    returns a list of valid AI providers.

    :return: a string list of valid providers
    """

    providers_list = ""
    for provider in PROVIDERS.keys():
        providers_list += "- " + provider + "\n"
    return providers_list


def raise_exception(text: str) -> Exception:
    """
    raises Typer exception with text message.
    
    :param text: string to be returned from raised exception
    :raises typer.Exit: raises typer.Exit with provided text message
    """

    from typer import Exit
    print(text)
    raise Exit(1)


def mask_api(api_key: str) -> str:
    """
    masks an API key value by only revealing the first four and last 6 characters.

    :param api_key: the value of the API key value
    :return: a masked version of the original API key value
    """

    return api_key[:4] + "..." + api_key[-6:]
