import logging
import yaml

def load_config(relative_path: str) -> dict:
    with open(relative_path, 'r') as stream:
        return yaml.safe_load(stream)

def get_logger(name: str, config_path: str):
    config = load_config(config_path)
    logging.basicConfig(level=config['logging']['level'], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(name)