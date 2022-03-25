from yaml_helper import YAML


def get_config():
    return YAML('config.yml').load()
