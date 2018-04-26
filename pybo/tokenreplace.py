# coding: utf-8
from .third_party import Query, parse_cql_query


class TokenReplace:
    def __init__(self, token_changes):
        self.changes = parse_cql_query(token_changes)

    def replace(self, token):
        for attr, value in self.changes.items():
            setattr(self.first, attr, value)

