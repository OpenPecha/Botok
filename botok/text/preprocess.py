# coding: utf-8
import re


def basic_cleanup(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def basic_keeps_lines(text: str) -> str:
    text = text.strip()
    # text = re.sub(r'\s+', ' ', text)
    return text
