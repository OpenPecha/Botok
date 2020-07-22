from botok import *


def test_missing_token1(wt):
    input_str = "འཐུང་བུད་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["འཐུང་", "བུད་"]


def test_missing_token2(wt):
    input_str = "ཨ་དྷྱིད་ཤུ་ཀ་ར་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ཨ་", "དྷྱིད་", "ཤུ་", "ཀ་ར་"]


def test_missing_token3(wt):
    input_str = "ཀི་བི་ཏི་སྭཱ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ཀི་", "བི་", "ཏི་", "སྭཱ་"]


def test_missing_token4(wt):
    input_str = "ལང་ཏང་ཙེ་དང་བྱེ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ལང་", "ཏང་", "ཙེ་", "དང་", "བྱེ་"]


def test_missing_token5(wt):
    input_str = "ད་མེད་བྷ་གར་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ད་", "མེད་", "བྷ་", "གར་"]


def test_missing_token6(wt):
    input_str = "རབ་བསྐུས་ནས།"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["རབ་", "བསྐུས་", "ནས", "།"]


def test_missing_token7(wt):
    input_str = "གདབ། །ཨོཾ་ན་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["གདབ", "། །", "ཨོཾ་", "ན་"]


def test_missing_token8(wt):
    input_str = "བི་སི་ནི་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བི་", "སི་", "ནི་"]


def test_missing_token9(wt):
    input_str = "བསྐོལ། །རྡོ་རྗེ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བསྐོལ", "། །", "རྡོ་རྗེ་"]


def test_missing_token10(wt):
    input_str = "བསྐུས་ཤིང་མཉེས་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བསྐུས་", "ཤིང་", "མཉེས་"]


def test_missing_token11(wt):
    input_str = "སྦོམ་ཞིང་ཆེ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["སྦོམ་", "ཞིང་", "ཆེ་"]


def test_missing_token12(wt):
    input_str = "བྷ་ག་ཁ་ཆེ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བྷ་", "ག་", "ཁ་ཆེ་"]


def test_missing_token13(wt):
    input_str = "།ཨོཾ་གི་རི་ཧི་རི་ཙི་རི། །ཨཱ་ཨཱ་ཤུ་མ་ཤ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == [
        "།",
        "ཨོཾ་",
        "གི་",
        "རི་",
        "ཧི་",
        "རི་",
        "ཙི་",
        "རི",
        "། །",
        "ཨཱ་",
        "ཨཱ་",
        "ཤུ་",
        "མ་",
        "ཤ་",
    ]


def test_missing_token14(wt):
    input_str = "བཟླས་བྱས་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བཟླས་", "བྱས་"]


def test_missing_token15(wt):
    input_str = "བསྣམས། །རྩི་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བསྣམས", "། །", "རྩི་"]


def test_missing_token16(wt):
    input_str = "ནཱ་ཤ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ནཱ་", "ཤ་"]


def test_missing_token17(wt):
    input_str = "གནོས་སྨྱོ་བྱེད་བརྗེད་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["གནོས་", "སྨྱོ་", "བྱེད་", "བརྗེད་"]


def test_missing_token18(wt):
    input_str = "གདོད་ཟིན་པ"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["གདོད་", "ཟིན་པ"]


def test_missing_token19(wt):
    input_str = "བསྲེས་དམར་ནག་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བསྲེས་", "དམར་ནག་"]


def test_missing_token20(wt):
    input_str = "བརྗེ་ཞིང་བསྐྱར་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བརྗེ་", "ཞིང་", "བསྐྱར་"]


def test_missing_token21(wt):
    input_str = "འཆང་མའི།"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["འཆང་", "མའི", "།"]


def test_missing_token22(wt):
    input_str = "དམོད་གཟུག་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["དམོད་", "གཟུག་"]


def test_missing_token23(wt):
    input_str = "བཤགས་ན་བུ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བཤགས་", "ན་", "བུ་"]


def test_missing_token24(wt):
    input_str = "མཐོལ་མགོ་ལ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["མཐོལ་", "མགོ་", "ལ་"]


def test_missing_token25(wt):
    input_str = "ཧུ་ཧཾ།"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ཧུ་", "ཧཾ", "།"]


def test_missing_token26(wt):
    input_str = "སྲི་མོ་བཛྲ་ནོ་ཏི་སྟ་ཀཱི་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == [
        "སྲི་",
        "མོ་",
        "བཛྲ་",
        "ནོ་",
        "ཏི་",
        "སྟ་",
        "ཀཱི་",
    ]


def test_missing_token27(wt):
    input_str = "གུམ་དང་།"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["གུམ་", "དང་", "།"]


def test_missing_token28(wt):
    input_str = "ཡོལ་གྱིས"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ཡོལ་", "གྱིས"]


def test_missing_token29(wt):
    input_str = "སྐུད་སྣ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["སྐུད་", "སྣ་"]


def test_missing_token30(wt):
    input_str = "བཀྲ་མ།"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བཀྲ་", "མ", "།"]


def test_missing_token31(wt):
    input_str = "གདོད་པར་བྱ"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["གདོད་", "པར་", "བྱ"]


def test_missing_token32(wt):
    input_str = "བསྒྲིབས་ཡོངས་སུ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བསྒྲིབས་", "ཡོངས་སུ་"]


def test_missing_token33(wt):
    input_str = "དྲངས་ནས།"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["དྲངས་", "ནས", "།"]


def test_missing_token34(wt):
    input_str = "རཱུ་ཏྲ་ཀྵ་གནས་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["རཱུ་", "ཏྲ་", "ཀྵ་", "གནས་"]


def test_missing_token35(wt):
    input_str = "ལྡང་པ་ན།"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ལྡང་པ་", "ན", "།"]


def test_missing_token36(wt):
    input_str = "བསྲུབས་བྱས་པས། །ལྟེ་ལྐོག་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བསྲུབས་", "བྱས་པས", "། །", "ལྟེ་", "ལྐོག་"]


def test_missing_token37(wt):
    input_str = "བསྟུན་ལ་ཉམས་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བསྟུན་", "ལ་", "ཉམས་"]


def test_missing_token38(wt):
    input_str = "ཥ་ཡིག་རྣམ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ཥ་", "ཡིག་", "རྣམ་"]


def test_missing_token39(wt):
    input_str = "འཛོམ། །རྣོ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["འཛོམ", "། །", "རྣོ་"]


def test_missing_token40(wt):
    input_str = "པྲི་ཡིག་དམར་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["པྲི་", "ཡིག་", "དམར་"]


def test_missing_token41(wt):
    input_str = "གཏུམ་བྱེད་དང་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["གཏུམ་", "བྱེད་", "དང་"]


def test_missing_token42(wt):
    input_str = "ཞིབ་བས་སྦལ།"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ཞིབ་", "བས་", "སྦལ", "།"]


def test_missing_token43(wt):
    input_str = "གཅོད་འཁོར་ལོ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["གཅོད་", "འཁོར་ལོ་"]


def test_missing_token44(wt):
    input_str = "བཏུལ་མཚམས་བཅད་པ"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བཏུལ་", "མཚམས་", "བཅད་པ"]


def test_missing_token45(wt):
    input_str = "ཞལ་བྷ་ག་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ཞལ་", "བྷ་", "ག་"]


def test_missing_token46(wt):
    input_str = "བསྐུར་ལས་ཀྱི་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བསྐུར་", "ལས་", "ཀྱི་"]


def test_missing_token47(wt):
    input_str = "འཁོས་དུ། །ཆེ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["འཁོས་", "དུ", "། །", "ཆེ་"]


def test_missing_token48(wt):
    input_str = "ནུ་ཧེ་རུ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ནུ་", "ཧེ་", "རུ་"]


def test_missing_token49(wt):
    input_str = "བརྩེགས་རྣམ་པར་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བརྩེགས་", "རྣམ་པར་"]


def test_missing_token50(wt):
    input_str = "བྷ་གར་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བྷ་", "གར་"]


def test_missing_token51(wt):
    input_str = "ནུ་ཡེ་ཤེས་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ནུ་", "ཡེ་ཤེས་"]


def test_missing_token52(wt):
    input_str = "བརྩེགས་ངེས་པ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བརྩེགས་", "ངེས་པ་"]


def test_missing_token53(wt):
    input_str = "བཟླས་བསྐུལ་གསུང་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བཟླས་", "བསྐུལ་", "གསུང་"]


def test_missing_token54(wt):
    input_str = "བྷ་གར་འཁྱིལ། །ཨོཾ་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བྷ་", "གར་", "འཁྱིལ", "། །", "ཨོཾ་"]


def test_missing_token55(wt):
    input_str = "བྷ་གར་སྦྱོར་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བྷ་", "གར་", "སྦྱོར་"]


def test_missing_token56(wt):
    input_str = "བརྒྱུད་སྐུ་གདུང་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བརྒྱུད་", "སྐུ་གདུང་"]


def test_missing_token57(wt):
    input_str = "སྒལ་བརྒྱུད་ཞབས་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["སྒལ་", "བརྒྱུད་", "ཞབས་"]


def test_missing_token58(wt):
    input_str = "བརྩེགས་ཆེ་མཆོག་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["བརྩེགས་", "ཆེ་མཆོག་"]


def test_missing_token59(wt):
    input_str = "།་གླེན་ལྐུགས་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["།་", "གླེན་ལྐུགས་"]
