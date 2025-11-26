
"""
io.py — contains file IO helper functions that relate to the configuration of Terma.

This module provides utilities to load, save, and validate Terma's configuration stored in
JSON format at `~/.config/terma/config.json`.

- load_config() -> dict | None: loads Terma's current configuration from the configuration file.
- save_config(configuration: dict) -> None: saves a new configuration to the configuration file.
- has_config() -> bool: returns true if configuration is complete and valid. 
"""

import json
import traceback
from pathlib import Path
from typing import Dict, Optional

CONFIG_PATH = Path.home() / ".config" / "terma" / "config.json"


def load_config() -> Optional[Dict]:
    """
    loads Terma's current configuration from the configuration file.

    :return: dict containing configuration if file exists, otherwise None
    """

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as configuration_file:
            return json.load(configuration_file)
    return None


def save_config(configuration: dict) -> None:
    """
    saves a new configuration to the configuration file.

    :param configuration: a dictionary with configuration keys (provider, model, & API key)
    :return: None
    """

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as configuration_file:
        json.dump(configuration, configuration_file, indent=2)


def has_config() -> bool:
    """
    returns true if configuration is complete and valid.

    :return: returns boolean value of configuration's validity (contains provider, model, & API key)
    """

    configuration = load_config()
    if not configuration:
        return False

    # check if all required keys exist in configuration file
    required_keys = ["provider", "model", "api-key"]

    for key in required_keys:
        if key not in configuration.keys():
            return False
    return True
