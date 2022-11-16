import re

def normalize_unicode(s, normalization_type="graphical"):
	# combined characters, using NFD representation:
	s = s.replace("\u0f00", "\u0f68\u0f7c\u0f7e")
	s = s.replace("\u0f43", "\u0f42\u0fb7")
	s = s.replace("\u0f4d", "\u0f4c\u0fb7")
	s = s.replace("\u0f52", "\u0f51\u0fb7")
	s = s.replace("\u0f57", "\u0f56\u0fb7")
	s = s.replace("\u0f5c", "\u0f5b\u0fb7")
	s = s.replace("\u0f69", "\u0f40\u0fb5")
	s = s.replace("\u0f73", "\u0f71\u0f72")
	s = s.replace("\u0f75", "\u0f71\u0f74")
	s = s.replace("\u0f76", "\u0fb2\u0f80")
	s = s.replace("\u0f77", "\u0fb2\u0f71\u0f80")
	s = s.replace("\u0f78", "\u0fb3\u0f80")
	s = s.replace("\u0f79", "\u0fb3\u0f71\u0f80")
	s = s.replace("\u0f81", "\u0f71\u0f80")
	s = s.replace("\u0f93", "\u0f92\u0fb7")
	s = s.replace("\u0f9d", "\u0f9c\u0fb7")
	s = s.replace("\u0fa2", "\u0fa1\u0fb7")
	s = s.replace("\u0fa7", "\u0fa6\u0fb7")
	s = s.replace("\u0fac", "\u0fab\u0fb7")
	s = s.replace("\u0fb9", "\u0f90\u0fb5")
	if normalization_type == "graphical":
		s = s.replace("\u0f0c", "\u0f0b")
		s = s.replace("\u0f0e", "\u0f0d\u0f0d")
	# ra does't transform into a small rago before nya
	s = s.replace("\u0f65\u0f99", "\u0f62\u0f99")
	# no achung in the middle of stacks, only full achung
	s = re.sub(r"[\u0f71]([\u0f8d-\u0fbc])", "\u0fb0\1", s)
	# reorder: subscript before vowels:
	s = re.sub(r"([\u0f71-\u0f87]+)([\u0f8d-\u0fbc]+)", r"\2\1", s)
	# reorder: achung before other vowels
	s = re.sub(r"([\u0f72-\u0f87]+)[\u0f71]", r"ཱ\1", s)
	# reorder: gigus before other vowels except achung
	s = re.sub(r"([\u0f72\u0f7a-\u0f87]+)[\u0f74]", r"ུ\1", s)
	# reorder: vowels before other signs:
	s = re.sub(r"([\u0f7e\u0f7f\u0fb2\u0fb3\u0f86\u0f87]+)([\u0f7a-\u0f7d\u0f80]+)", r"\2\1", s)
	return s

def debug_to_unicode(s):
	res = ""
	for c in s:
		res += "\\u%x " % ord(c)
	return res

def test_normalize_unicode():
	assert(normalize_unicode("\u0f77") == "\u0fb2\u0f71\u0f80")
	assert(normalize_unicode("\u0f40\u0f7e\u0f7c\u0f74\u0f71") == "\u0f40\u0f71\u0f74\u0f7c\u0f7e")

if __name__ == "__main__":
	test_normalize_unicode()