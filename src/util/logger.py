import logging


def get_logger(script_name: str, config: dict) -> logging.Logger:
    """
    Creates and returns a logger with the given name and configuration.

    Parameters:
    script_name (str): The name of the script for which the logger is being created.
    config (dict): The configuration dictionary with logging settings.

    Returns:
    logging.Logger: The configured logger.
    """
    logger = logging.getLogger(script_name)

    # Set the logging level based on the config or default to WARNING.
    log_level = config.get("logging", {}).get("level", "WARNING")
    logger.setLevel(getattr(logging, log_level))

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, log_level))

    # Create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.handlers:
        logger.addHandler(ch)

    return logger
