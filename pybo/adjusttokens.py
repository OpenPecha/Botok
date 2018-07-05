import os
import yaml
from .helpers import open_file
from .splittingmatcher import SplittingMatcher
from .mergingmatcher import MergingMatcher
from .replacingmatcher import ReplacingMatcher


class AdjustTokens:
    def __init__(self, rules_folder=None):
        self.paths = [] # [os.path.join(os.path.split(__file__)[0], 'resources', 'rules')]
        if rules_folder:
            self.paths.append(rules_folder)
        self.rules = []
        self.parse_rules()

    def adjust(self, token_list):
        for rule in self.rules:
            operation = list(rule.keys())[0]
            if operation == 'split':
                match_query, replace_idx, split_idx, replace_query = rule[operation]
                sm = SplittingMatcher(match_query, replace_idx, split_idx, token_list, replace_query)
                token_list = sm.split_on_matches()
            elif operation == 'merge':
                match_query, replace_idx, replace_query = rule[operation]
                mm = MergingMatcher(match_query, replace_idx, token_list, replace_query)
                token_list = mm.merge_on_matches()
            elif operation == 'repla':
                match_query, replace_idx, replace_query = rule[operation]
                rm = ReplacingMatcher(match_query, replace_idx, token_list, replace_query)
                rm.replace_on_matches()
            else:
                print('rule problem: ' + rule)
        return token_list

    def parse_rules(self):
        def gen_file_paths(folders):
            paths = [os.path.join(os.path.split(__file__)[0], folder, f) for folder in folders
                     for f in os.listdir(folder)]
            return sorted(paths)

        for rule_file in gen_file_paths(self.paths):
            self.rules.extend(yaml.load(open_file(rule_file)))
