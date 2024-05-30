#!/usr/bin/env python3
# This is a simple logging example using the logging module
# based on this:
# https://www.youtube.com/watch?v=9L77QExPmI0
import logging.config
import logging.handlers
import pathlib
import json
import traceback


logger = logging.getLogger("modern_logging")


def setup_logging():
    config_file = pathlib.Path(__file__).parent / "modern_logging.json"
    with open(config_file, "r") as file:
        logging_config = json.load(file)
    logging.config.dictConfig(logging_config)


def main() -> None:
    setup_logging()
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Division by zero", exc_info=True)
    print("Hello World!")



if __name__ == '__main__':
    main()
