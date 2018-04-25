# coding: utf-8
from .cql import Query


__all__ = ['Query', 'parse_cql_query']


def parse_cql_query(query):
    """
    CQL parser for replacing the content of Token.attributes.
    From the CQL syntax, only the attribute names and the values
    are taken into account.

    :param query: CQL query string
    :return: a list of dicts, one per token slot, where
                keys == Token.attributes and
                values == content of the expected Token.attributes
    """
    def cql2dict(tokenexpr):
        """
        Expects the following syntax:
            '[attribute1="value1" & attribute2="value2" (& ...)]'
        """
        changes = {}
        for attrexprs in tokenexpr:
            key = attrexprs.attribute
            value = attrexprs.valueexpr[0]
            changes[key] = value
        return changes

    if query:
        parsed = Query(query)
        cql_dict = []
        for tokenexpr in parsed.tokenexprs:
            cql_dict.append(cql2dict(tokenexpr))
        return cql_dict
    else:
        return None
