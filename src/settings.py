import json
from os.path import join
from typing import Tuple

import src.log

logger = src.log.get_logger(__name__)
logger.setLevel(10)


def create_settings_file():
    with open(join("data", "settings.json"), "w") as file:
        file.write("""{\n"enable_sounds": true,\n "spectator_scale": 1.0\n}""")


def get_settings() -> Tuple[float, bool]:
    try:
        with open(join("data", "settings.json"), "r") as file:
            raw_data = file.read()
            settings: dict = json.loads(raw_data)
            scale = settings["spectator_scale"]
            sounds = settings["enable_sounds"]
    except FileNotFoundError:
        logger.info("No settings file found")
        create_settings_file()
        scale = 1.0
        sounds = True

    return scale, sounds
