import logging


def get_logger(script_name: str, config: dict) -> logging.Logger:
    logging.basicConfig(
        level=config["logging"]["level"],
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(script_name)
