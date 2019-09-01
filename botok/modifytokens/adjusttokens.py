# coding: utf-8
import yaml

from .splittingmatcher import SplittingMatcher
from .mergingmatcher import MergingMatcher
from .replacingmatcher import ReplacingMatcher


class AdjustTokens:
    def __init__(self, main=None, custom=None):
        self.paths = []
        if main:
            self.paths.extend(main)
        if custom:
            self.paths.extend(custom)
        self.rules = []
        self.parse_rules()

    def adjust(self, token_list):
        for rule in self.rules:
            operation = list(rule.keys())[0]
            if operation == "split":
                match_query, replace_idx, split_idx, replace_query = rule[operation]
                sm = SplittingMatcher(
                    match_query, replace_idx, split_idx, token_list, replace_query
                )
                token_list = sm.split_on_matches()
            elif operation == "merge":
                match_query, replace_idx, replace_query = rule[operation]
                mm = MergingMatcher(match_query, replace_idx, token_list, replace_query)
                token_list = mm.merge_on_matches()
            elif operation == "repla":
                match_query, replace_idx, replace_query = rule[operation]
                rm = ReplacingMatcher(
                    match_query, replace_idx, token_list, replace_query
                )
                rm.replace_on_matches()
            else:
                print("rule problem: " + rule)
        return token_list

    def parse_rules(self):
        """
        Files are sorted before being applied. Thus, filenames
        :return:
        """
        for rule_file in sorted(self.paths):
            self.rules.extend(yaml.safe_load(rule_file.read_text(encoding="utf-8-sig")))
