# coding: utf-8
from .cql import Query


__all__ = ['Query', 'parse_cql_query', 'replace_token_attributes']


def parse_cql_query(query, numerals=True, booleans=True):
    """
    CQL parser for replacing the content of Token.attributes.
    From the CQL syntax, only the attribute names and the values
    are taken into account.

    :param query: CQL query string
    :param numerals: if True, gives the Python int instead of the string
    :param booleans: if True, gives the Python bool instead of the string
    :return: a list of dicts, one per token slot, where
                keys == Token.attributes and
                values == content of the expected Token.attributes
    """
    def str2int(string):
        try:
            return int(string)
        except ValueError:
            return string

    def str2bool(string):
        b = {'True': True, 'False': False, 'None': None}
        if string in b:
            return b[string]
        else:
            return string

    def cql2pattern(tokenexpr, numerals, booleans):
        """
        Expects the following syntax:
            '[attribute1="value1" & attribute2="value2" (& ...)]'
        """
        changes = {}
        for attrexprs in tokenexpr:
            key = attrexprs.attribute
            value = attrexprs.valueexpr[0]
            if numerals:
                value = str2int(value)
            if booleans:
                value = str2bool(value)
            changes[key] = value
        return changes

    if query:
        parsed = Query(query)
        pattern = []
        for tokenexpr in parsed.tokenexprs:
            pattern.append(cql2pattern(tokenexpr, numerals, booleans))
        return pattern
    else:
        return None


def replace_token_attributes(tokens, token_changes):
    """
    Applies in place the replacements found in the CQL query (token_changes)
    the number of tokens in the list and the number of token slots in the query
    must be even.

    :param tokens: list of tokens
    :param token_changes: CQL query
    """
    changes = parse_cql_query(token_changes)
    if type(tokens) == list:
        assert len(tokens) == len(changes)
        for i in range(len(tokens)):
            for attr, value in changes[i].items():
                setattr(tokens[i], attr, value)
    else:
        assert len(changes) == 1
        for attr, value in changes[0].items():
            setattr(tokens, attr, value)
