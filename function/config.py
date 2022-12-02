import argparse
import configparser


class MergeConfig:
    def __init__(self, parser_arguments, check_list):
        self.parser_arguments = parser_arguments
        self.check_list = check_list
        self.args = None
        self.config = None

    # deal arg parser
    def __get_parser(self):
        parser = argparse.ArgumentParser()
        for pa in self.parser_arguments:
            parser.add_argument(pa[0], pa[1], help=pa[2], type=pa[3])
        self.args = parser.parse_args()

    # deal config
    def __get_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        return self.config

    def __merge_config(self):
        for c in self.check_list:
            value = self.args.__getattribute__(c["arg"])
            if value:
                self.config.read_dict({c["cfg"][0]: {c["cfg"][1]: value}})

    def get_config(self):
        self.__get_parser()
        self.__get_config()
        self.__merge_config()
        return self.config
