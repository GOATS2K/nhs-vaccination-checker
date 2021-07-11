__version__ = "0.1.0"

from nhs_vaccination_checker.config import (
    DATA_DIR,
    CONFIG_PATH,
    read_config,
    write_config,
)

if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)
    write_config()
else:
    if not CONFIG_PATH.exists():
        write_config()

config = read_config()
