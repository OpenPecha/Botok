# coding: utf-8


def decomment_file(file):
    for row in file:
        raw = row.split("#")[0].strip()
        if raw:
            yield raw
