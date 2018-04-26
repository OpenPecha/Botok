# coding: utf-8
from .third_party import parse_cql_query


class TokenReplace:
    """
    Allows to replace any number of attributes
    within any number of tokens
    takes as input a list of tuples: (idx, 'token_changes')
    """
    def __init__(self, token_changes):
        self.changes = parse_cql_query(token_changes)

    def replace(self, token_list):
        for attr, value in self.changes.items():
            setattr(self.first, attr, value)
