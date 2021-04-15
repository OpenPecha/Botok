# coding: utf-8
import csv
import re

from .splittingmatcher import SplittingMatcher
from .mergingmatcher import MergingMatcher
from .replacingmatcher import ReplacingMatcher
from ..utils.helpers import decomment_file


class AdjustTokens:
    """
    Syntax for the .tsv adjustment rules
    ===================================
    - each rule should be as follows: "<matchcql>\t<index>\t<operation>\t<replacecql>"
    - comments with # and empty lines are allowed
    - CQL rules: "<text>" can be used without specifying that there is "text_cleaned="
    - Index format: either "<matching_index>" or "<matching_index>-<splitting-index>"
    - Adjustment format:
            - "+" for merge
            - ":" for split (default: syllable mode)
            - "::" for split in character mode
            - "=" for replace
    - Constraint: "<matching_index>-<splitting-index>" is only allowed if adjustment is ":" or "::"
    """

    def __init__(self, main=None, custom=None):
        self.paths = []
        if custom:
            self.paths.extend(custom)
        elif main:
            self.paths.extend(main)
        self.rules = []
        self.parse_rules()

    def no_token_matched(self, matchcql):
        matched_tokens = [token for token in re.split(r'(\[.+?\])', matchcql) if token != " " and token != ""]
        return len(matched_tokens)

    def adjust(self, token_list):
        for rule in self.rules:
            if rule["operation"] == "split":
                if rule["matchidx"] <= self.no_token_matched(rule['matchcql']):
                    sm = SplittingMatcher(
                        rule["matchcql"],
                        rule["matchidx"],
                        rule["splitidx"],
                        token_list,
                        rule["replacecql"],
                    )
                    token_list = sm.split_on_matches(mode=rule["splitmode"])
                else:
                    print(f'[ERROR]: No token to spilt with token number {rule["matchidx"]} found in rule {"    ".join(rule)}')
            elif rule["operation"] == "merge":
                if rule["matchidx"] < self.no_token_matched(rule['matchcql']):
                    mm = MergingMatcher(
                        rule["matchcql"], rule["matchidx"], token_list, rule["replacecql"]
                    )
                    token_list = mm.merge_on_matches()
                else:
                    print(f'[ERROR]: No token to merge with token number {rule["matchidx"]} found in rule {"    ".join(rule)}')
            elif rule["operation"] == "repl":
                rm = ReplacingMatcher(
                    rule["matchcql"], rule["matchidx"], token_list, rule["replacecql"]
                )
                rm.replace_on_matches()
        return token_list

    def parse_rules(self):
        """
        Files are sorted before being applied. Thus, filenames
        :return:
        """
        for rule_file in sorted(self.paths):
            for rule in csv.reader(
                decomment_file(rule_file.open(encoding="utf-8-sig")), delimiter="\t"
            ):
                self.rules.append(self.parse_rule(rule))

    @staticmethod
    def parse_rule(rule):
        idx_sep = "-"

        # sanity checks
        if len(rule) != 4:
            raise SyntaxError("There can't be more than three columns per rule.")
        if not rule[1]:
            raise SyntaxError("There needs to be an index for every rule.")
        if idx_sep in rule[1] and rule[2] not in [":", "::"]:
            raise SyntaxError(
                "The double index in only intended for split adjustments."
            )
        if rule[2] not in ["+", "=", ":", "::"]:
            raise SyntaxError(
                'The supported operations are either of ["+", "=", ":", "::"].'
            )

        # parse
        rule_dict = {
            "matchcql": None,
            "matchidx": None,
            "operation": None,
            "splitidx": None,
            "splitmode": None,
            "replacecql": None,
        }
        rule_dict["matchcql"] = rule[0]
        if idx_sep in rule[1]:
            match_idx, split_idx = rule[1].split("-")
            rule_dict["matchidx"] = int(match_idx)
            rule_dict["splitidx"] = int(split_idx)
        else:
            rule_dict["matchidx"] = int(rule[1])
        if rule[2] == "=":
            rule_dict["operation"] = "repl"
        elif rule[2] == "+":
            rule_dict["operation"] = "merge"
        elif rule[2] == ":":
            rule_dict["operation"] = "split"
            rule_dict["splitmode"] = "syl"
        elif rule[2] == "::":
            rule_dict["operation"] = "split"
            rule_dict["splitmode"] = "char"
        rule_dict["replacecql"] = rule[3]

        return rule_dict
