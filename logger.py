"""Logger configuration"""

import os
import logging
import sys


def get_logger(name: str, default_level: str = "INFO") -> logging.Logger:

    log_level = os.getenv("LOG_LEVEL", default_level).upper()

    use_colors = sys.stdout.isatty()
    color_start = "\033[96m" if use_colors else ""
    color_end = "\033[0m" if use_colors else ""

    format_string = (
        f"{color_start}[%(levelname)s]{color_end} %(asctime)s.%(msecs)03d "
        "%(name)s %(module)s:%(lineno)d - %(funcName)s() - %(message)s"
    )

    time_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        format=format_string,
        datefmt=time_format,
        level=log_level,
        force=True
    )

    return logging.getLogger(name)
