import logging
import yaml

with open("src/config/cfg.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

def get_logger(name):
    logging.basicConfig(level=config['logging']['level'], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(name)