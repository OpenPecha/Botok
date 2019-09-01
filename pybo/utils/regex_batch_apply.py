# coding: utf-8
import re


def batch_apply_regex(string, pairs):
    for find, repl in pairs:
        string = re.sub(find, repl, string, flags=re.MULTILINE)
    return string


def get_regex_pairs(lines, sep="\t-\t"):
    regex_pairs = []
    clean_lines = _parse_lines(lines, sep)

    for line in clean_lines:
        find, replace = line.split(sep)
        regex_pairs.append((r"" + find, r"" + replace))
    return regex_pairs


def _parse_lines(lines, sep):
    cleaned = []
    for num, line in enumerate(lines):
        # remove comment lines and empty lines
        if "#" in line:
            line = line[: line.find("#")]

        # strip line returns while keeping space chars and screen all empty lines
        line = line.strip('\n\r')
        if not line:
            continue

        # ensure there is 1 and only 1 occurrence of sep
        if line.count(sep) != 1:
            print(f"passing line {num + 1}: {line}.")
            continue

        cleaned.append(line)
    return cleaned
