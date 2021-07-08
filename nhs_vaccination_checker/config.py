import configparser
from pathlib import Path
from re import S
from typing import Dict
from appdirs import user_data_dir
import click

DATA_DIR = Path(user_data_dir("nhs-vaccination-checker"))
CONFIG_PATH = Path(user_data_dir("nhs-vaccination-checker")) / "config.ini"

config = configparser.ConfigParser()
config["DEFAULT"] = {"nhs_number": "", "date_of_birth": "", "booking_reference": ""}


def write_config() -> None:
    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)
    if click.confirm("Blank config file found, would you like to edit it?"):
        click.edit(filename=CONFIG_PATH)


def read_config() -> configparser.ConfigParser:
    config.read(CONFIG_PATH)
    return config
