import re

# Characters that continue a stack after a base (vowels, marks, subjoined letters).
# Keep in sync with the intent of standard_tibetan._keepinstack, with these
# deliberate differences / notes:
#   * U+0F7F (rnam bcad / visarga) is *not* included here so it stays a
#     separate token (see tests below and historical behavior).
#   * U+0F39 (tsa-phru) *is* included: it is a mark on the preceding base.
#     Omitting it made botok split e.g. ra+tsa-phru+i into [ra, tsa-phru+i],
#     which then looked like a vowel-bearing tsa-phru with no base.
#   * U+0F3E / U+0F3F (yar/mar tshes) and U+0FC6 (padma gdan) are included
#     as nonspacing / spacing marks that belong on the preceding stack.
_STACK_CONTINUATION = (
    "\u0f18\u0f19"  # astrological
    "\u0f35\u0f37"  # honorific marks
    "\u0f39"  # tsa-phru
    "\u0f3e\u0f3f"  # yar / mar tshes
    "\u0f71-\u0f7e"  # vowels + anusvara (excludes U+0F7F visarga)
    "\u0f80-\u0f84"  # reversed vowels, nyi zla, halanta
    "\u0f86\u0f87"  # lci / yang rtags
    "\u0f8d-\u0fbc"  # subjoined signs/letters
    "\u0fc6"  # padma gdan
)

# Base = anything not a continuation mark, then greedy continuation marks.
# The second alternative keeps a leading run of continuation marks (malformed
# / isolated mark sequences) instead of silently dropping them.
STACK_PARTS = re.compile(
    rf"(?:[^{_STACK_CONTINUATION}][{_STACK_CONTINUATION}]*|^[{_STACK_CONTINUATION}]+)"
)


def tokenize_in_stacks(str):
	return STACK_PARTS.findall(str)


def test_stack_tokenizer():
	assert tokenize_in_stacks("\u0f40\u0f7f\u0f50\u0f7c\u0f42\u0f0b\u0f60\u0f56\u0fb1\u0f58\u0f0b\u0f54\u0f60\u0f71\u0f72\u0f0b\u0f62\u0f7c\u0f0d") == [
		"\u0f40", "\u0f7f", "\u0f50\u0f7c", "\u0f42", "\u0f0b", "\u0f60", "\u0f56\u0fb1",
		"\u0f58", "\u0f0b", "\u0f54", "\u0f60\u0f71\u0f72", "\u0f0b", "\u0f62\u0f7c", "\u0f0d",
	]
	assert tokenize_in_stacks("\u0f7f\u0f40\u0f7f") == ["\u0f7f", "\u0f40", "\u0f7f"]
	assert tokenize_in_stacks("\u0f62\u0f39\u0f72") == ["\u0f62\u0f39\u0f72"]
	assert tokenize_in_stacks("\u0f66\u0fa1\u0f39\u0f74\u0f72") == ["\u0f66\u0fa1\u0f39\u0f74\u0f72"]
	assert tokenize_in_stacks("\u0f56\u0f66\u0fa1\u0f39\u0f74\u0f72\u0f56\u0f51") == [
		"\u0f56", "\u0f66\u0fa1\u0f39\u0f74\u0f72", "\u0f56", "\u0f51",
	]


if __name__ == "__main__":
	test_stack_tokenizer()
