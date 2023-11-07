import yaml
import os


def load_config(relative_path: str) -> dict:
    """
    Load a configuration file from the given relative path.

    Parameters:
    relative_path (str): The file path to the YAML configuration file.

    Returns:
    dict: The configuration settings loaded from the file.

    Raises:
    FileNotFoundError: If the file does not exist at the specified path.
    yaml.YAMLError: If there is an error parsing the YAML file.
    """
    if not os.path.exists(relative_path):
        raise FileNotFoundError(f"The configuration file {relative_path} does not exist.")
    
    try:
        with open(relative_path, "r") as stream:
            config = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        print(f"Error parsing the YAML file: {e}")
        raise
    except Exception as e:
        print(f"An error occurred while loading the configuration: {e}")
        raise
    return config
