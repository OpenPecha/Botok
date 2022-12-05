import re

#STACK_PARTS = re.compile(r"(?:[^\u0f18\u0f19\u0f35\u0f37\u0f71-\u0f7e\u0f80-\u0f84\u0f86\u0f87\u0f8d-\u0fbc][\u0f18\u0f19\u0f35\u0f37\u0f71-\u0f7e\u0f80-\u0f84\u0f86\u0f87\u0f8d-\u0fbc]*|^[\u0f18\u0f19\u0f35\u0f37\u0f71-\u0f7e\u0f80-\u0f84\u0f86\u0f87\u0f8d-\u0fbc]+)")
STACK_PARTS = re.compile(r"[^\u0f18\u0f19\u0f35\u0f37\u0f71-\u0f7e\u0f80-\u0f84\u0f86\u0f87\u0f8d-\u0fbc][\u0f18\u0f19\u0f35\u0f37\u0f71-\u0f7e\u0f80-\u0f84\u0f86\u0f87\u0f8d-\u0fbc]*")

def tokenize_in_stacks(str):
	return STACK_PARTS.findall(str)

def test_stack_tokenizer():
	assert(tokenize_in_stacks("ཀཿཐོག་འབྱམ་པའཱི་རོ།") == ["ཀ", "\u0f7f", "ཐོ", "ག", "་", "འ", "བྱ", "མ", "་", "པ", "འཱི", "་", "རོ", "།"])
	assert(tokenize_in_stacks("\u0f7fཀཿ") == ["\u0f7f", "ཀ", "\u0f7f"])

if __name__ == "__main__":
	test_stack_tokenizer()