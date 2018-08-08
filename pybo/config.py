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
        """Initialize the class

        Converting the configuration file into a Python dictionnary object which
        contains all the necesary parameters to set up Pybo properly.

        The text file has to respect the YAML writing rules.
        For more information: 'https://pyyaml.org/wiki/PyYAML'

            :param filename: Filename of the file with its extension
        """
        file, extension = os.path.splitext(filename)
        if extension != ".yaml":
            raise Exception("Unrecognised file extension. It only supports .yaml files")

        self.filename = filename
        self.full_path_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", self.filename)

        with open(self.full_path_name, mode="r", encoding="utf-8") as f:
            self.config = yaml.load(f.read())

    def get_profile(self, profile):
        """Get the profile configuration list

        Each profile has a list of files which can be collected by this function.

        :param profile: the profile name
        :return: the list of files of the selected profile
        """
        return self.config["POS"]["Profile"][profile]


if __name__ == '__main__':
    config = Config("config.yaml")
    config.parse_config_file()
    print(config.config)