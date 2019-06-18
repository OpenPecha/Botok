import yaml
from .splittingmatcher import SplittingMatcher
from .mergingmatcher import MergingMatcher
from .replacingmatcher import ReplacingMatcher


class AdjustTokens:
    def __init__(self, rules_folder=None):
        self.paths = []
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
        paths = [p for path in self.paths for p in path.glob('*.*')]
        for rule_file in sorted(paths):
            self.rules.extend(yaml.load(rule_file.read_text(encoding='utf-8-sig')))
