import yaml


def load_config(relative_path: str) -> dict:
    with open(relative_path, "r") as stream:
        return yaml.safe_load(stream)
