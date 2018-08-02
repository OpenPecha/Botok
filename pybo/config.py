# coding: utf-8

"""Configuration file to set up Pybo
"""

import os

import yaml


class Config:
    """Configuration class

    Attributs :
        filename: Complete filename of the configuration file
        config : Dictionary object containing all the configuration elements
    """
    def __init__(self, filename):
        """Initialise the class configuration

            :param filename: Filename of the file with its extension
        """
        file, extension = os.path.splitext(filename)
        if extension != ".yaml":
            raise Exception("Unrecognised file extension. it only supports .yaml files")

        self.filename = filename

    def parse_config_file(self):
        """Parsing the configuration file

        Converting the configuration file into a Python dictionnaire object which
        contains all the necesary parameters to set up Pybo properly.

        The text file has to respect the YAML writing rules.
        For more information: 'https://pyyaml.org/wiki/PyYAML'

        :return: The Python dictionary object containing the configuration
        """
        config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", self.filename)

        with open(config_file, mode="r", encoding="utf-8") as f:
            self.config = yaml.load(f.read())
        return self.config


if __name__ == '__main__':
    config = Config("config.yaml")
    config.parse_config_file()
    print(config.config)