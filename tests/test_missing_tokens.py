from pybo import *

tok = BoTokenizer('POS')


def test_missing_token1():
    input_str = "འཐུང་བུད་"
    tokens = tok.tokenize(input_str)
    assert ['འཐུང་', 'བུད་'] == [t.content for t in tokens]


def test_missing_token2():
    input_str = "ཨ་དྷྱིད་ཤུ་ཀ་ར་"
    tokens = tok.tokenize(input_str)
    assert ['ཨ་', 'དྷྱིད་', 'ཤུ་', 'ཀ་ར་'] == [t.content for t in tokens]


def test_missing_token3():
    input_str = "ཀི་བི་ཏི་སྭཱ་"
    tokens = tok.tokenize(input_str)
    assert ['ཀི་', 'བི་', 'ཏི་', 'སྭཱ་'] == [t.content for t in tokens]


def test_missing_token4():
    input_str = "ལང་ཏང་ཙེ་དང་བྱེ་"
    tokens = tok.tokenize(input_str)
    assert ['ལང་', 'ཏང་', 'ཙེ་', 'དང་', 'བྱེ་'] == [t.content for t in tokens]


def test_missing_token5():
    input_str = "ད་མེད་བྷ་གར་"
    tokens = tok.tokenize(input_str)
    assert ['ད་', 'མེད་', 'བྷ་', 'གར་'] == [t.content for t in tokens]


def test_missing_token6():
    input_str = "རབ་བསྐུས་ནས།"
    tokens = tok.tokenize(input_str)
    assert ['རབ་', 'བསྐུས་', 'ནས', '།'] == [t.content for t in tokens]


def test_missing_token7():
    input_str = "གདབ། །ཨོཾ་ན་"
    tokens = tok.tokenize(input_str)
    assert ['གདབ', '། ', '།', 'ཨོཾ་', 'ན་'] == [t.content for t in tokens]


def test_missing_token8():
    input_str = "བི་སི་ནི་"
    tokens = tok.tokenize(input_str)
    assert ['བི་', 'སི་', 'ནི་'] == [t.content for t in tokens]


def test_missing_token9():
    input_str = "བསྐོལ། །རྡོ་རྗེ་"
    tokens = tok.tokenize(input_str)
    assert ['བསྐོལ', '། ', '།', 'རྡོ་རྗེ་'] == [t.content for t in tokens]


def test_missing_token10():
    input_str = "བསྐུས་ཤིང་མཉེས་"
    tokens = tok.tokenize(input_str)
    assert ['བསྐུས་', 'ཤིང་', 'མཉེས་'] == [t.content for t in tokens]


def test_missing_token11():
    input_str = "སྦོམ་ཞིང་ཆེ་"
    tokens = tok.tokenize(input_str)
    assert ['སྦོམ་', 'ཞིང་', 'ཆེ་'] == [t.content for t in tokens]


def test_missing_token12():
    input_str = "བྷ་ག་ཁ་ཆེ་"
    tokens = tok.tokenize(input_str)
    assert ['བྷ་', 'ག་', 'ཁ་ཆེ་'] == [t.content for t in tokens]


def test_missing_token13():
    input_str = "།ཨོཾ་གི་རི་ཧི་རི་ཙི་རི། །ཨཱ་ཨཱ་ཤུ་མ་ཤ་"
    tokens = tok.tokenize(input_str)
    assert ['།', 'ཨོཾ་', 'གི་', 'རི་', 'ཧི་', 'རི་', 'ཙི་', 'རི', '། ', '།', 'ཨཱ་', 'ཨཱ་', 'ཤུ་', 'མ་', 'ཤ་'] == [t.content for t in tokens]


def test_missing_token14():
    input_str = "བཟླས་བྱས་"
    tokens = tok.tokenize(input_str)
    assert ['བཟླས་', 'བྱས་'] == [t.content for t in tokens]


def test_missing_token15():
    input_str = "བསྣམས། །རྩི་"
    tokens = tok.tokenize(input_str)
    assert ['བསྣམས', '། ', '།', 'རྩི་'] == [t.content for t in tokens]


def test_missing_token16():
    input_str = "ནཱ་ཤ་"
    tokens = tok.tokenize(input_str)
    assert ['ནཱ་', 'ཤ་'] == [t.content for t in tokens]


def test_missing_token17():
    input_str = "གནོས་སྨྱོ་བྱེད་བརྗེད་"
    tokens = tok.tokenize(input_str)
    assert ['གནོས་', 'སྨྱོ་', 'བྱེད་', 'བརྗེད་'] == [t.content for t in tokens]


def test_missing_token18():
    input_str = "གདོད་ཟིན་པ"
    tokens = tok.tokenize(input_str)
    assert ['གདོད་', 'ཟིན་པ'] == [t.content for t in tokens]


def test_missing_token19():
    input_str = "བསྲེས་དམར་ནག་"
    tokens = tok.tokenize(input_str)
    assert ['བསྲེས་', 'དམར་ནག་'] == [t.content for t in tokens]


def test_missing_token20():
    input_str = "བརྗེ་ཞིང་བསྐྱར་"
    tokens = tok.tokenize(input_str)
    assert ['བརྗེ་', 'ཞིང་', 'བསྐྱར་'] == [t.content for t in tokens]


def test_missing_token21():
    input_str = "འཆང་མའི།"
    tokens = tok.tokenize(input_str)
    assert ['འཆང་', 'མ', 'འི', '།'] == [t.content for t in tokens]


def test_missing_token22():
    input_str = "དམོད་གཟུག་"
    tokens = tok.tokenize(input_str)
    assert ['དམོད་', 'གཟུག་'] == [t.content for t in tokens]


def test_missing_token23():
    input_str = "བཤགས་ན་བུ་"
    tokens = tok.tokenize(input_str)
    assert ['བཤགས་', 'ན་', 'བུ་'] == [t.content for t in tokens]


def test_missing_token24():
    input_str = "མཐོལ་མགོ་ལ་"
    tokens = tok.tokenize(input_str)
    assert ['མཐོལ་', 'མགོ་', 'ལ་'] == [t.content for t in tokens]


def test_missing_token25():
    input_str = "ཧུ་ཧཾ།"
    tokens = tok.tokenize(input_str)
    assert ['ཧུ་', 'ཧཾ', '།'] == [t.content for t in tokens]


def test_missing_token26():
    input_str = "སྲི་མོ་བཛྲ་ནོ་ཏི་སྟ་ཀཱི་"
    tokens = tok.tokenize(input_str)
    assert ['སྲི་', 'མོ་', 'བཛྲ་', 'ནོ་', 'ཏི་', 'སྟ་', 'ཀཱི་'] == [t.content for t in tokens]


def test_missing_token27():
    input_str = "གུམ་དང་།"
    tokens = tok.tokenize(input_str)
    assert ['གུམ་', 'དང་', '།'] == [t.content for t in tokens]


def test_missing_token28():
    input_str = "ཡོལ་གྱིས"
    tokens = tok.tokenize(input_str)
    assert ['ཡོལ་', 'གྱིས'] == [t.content for t in tokens]


def test_missing_token29():
    input_str = "སྐུད་སྣ་"
    tokens = tok.tokenize(input_str)
    assert ['སྐུད་', 'སྣ་'] == [t.content for t in tokens]


def test_missing_token30():
    input_str = "བཀྲ་མ།"
    tokens = tok.tokenize(input_str)
    assert ['བཀྲ་', 'མ', '།'] == [t.content for t in tokens]


def test_missing_token31():
    # པར
    input_str = "གདོད་པར་བྱ"
    tokens = tok.tokenize(input_str)
    assert ['གདོད་', 'པ', 'ར་', 'བྱ'] == [t.content for t in tokens]


def test_missing_token32():
    input_str = "བསྒྲིབས་ཡོངས་སུ་"
    tokens = tok.tokenize(input_str)
    assert ['བསྒྲིབས་', 'ཡོངས་སུ་'] == [t.content for t in tokens]


def test_missing_token33():
    input_str = "དྲངས་ནས།"
    tokens = tok.tokenize(input_str)
    assert ['དྲངས་', 'ནས', '།'] == [t.content for t in tokens]


def test_missing_token34():
    input_str = "རཱུ་ཏྲ་ཀྵ་གནས་"
    tokens = tok.tokenize(input_str)
    assert ['རཱུ་', 'ཏྲ་', 'ཀྵ་', 'གནས་'] == [t.content for t in tokens]


def test_missing_token35():
    input_str = "ལྡང་པ་ན།"
    tokens = tok.tokenize(input_str)
    assert ['ལྡང་', 'པ་', 'ན', '།'] == [t.content for t in tokens]


def test_missing_token36():
    input_str = "བསྲུབས་བྱས་པས། །ལྟེ་ལྐོག་"
    tokens = tok.tokenize(input_str)
    assert ['བསྲུབས་', 'བྱས་པ', 'ས', '། ', '།', 'ལྟེ་', 'ལྐོག་'] == [t.content for t in tokens]


def test_missing_token37():
    input_str = "བསྟུན་ལ་ཉམས་"
    tokens = tok.tokenize(input_str)
    assert ['བསྟུན་', 'ལ་', 'ཉམས་'] == [t.content for t in tokens]


def test_missing_token38():
    input_str = "ཥ་ཡིག་རྣམ་"
    tokens = tok.tokenize(input_str)
    assert ['ཥ་', 'ཡིག་', 'རྣམ་'] == [t.content for t in tokens]


def test_missing_token39():
    input_str = "འཛོམ། །རྣོ་"
    tokens = tok.tokenize(input_str)
    assert ['འཛོམ', '། ', '།', 'རྣོ་'] == [t.content for t in tokens]


def test_missing_token40():
    input_str = "པྲི་ཡིག་དམར་"
    tokens = tok.tokenize(input_str)
    assert ['པྲི་', 'ཡིག་', 'དམར་'] == [t.content for t in tokens]


def test_missing_token41():
    input_str = "གཏུམ་བྱེད་དང་"
    tokens = tok.tokenize(input_str)
    assert ['གཏུམ་', 'བྱེད་', 'དང་'] == [t.content for t in tokens]


def test_missing_token42():
    # བས
    input_str = "ཞིབ་བས་སྦལ།"
    tokens = tok.tokenize(input_str)
    assert ['ཞིབ་', 'བ', 'ས་', 'སྦལ', '།'] == [t.content for t in tokens]


def test_missing_token43():
    input_str = "གཅོད་འཁོར་ལོ་"
    tokens = tok.tokenize(input_str)
    assert ['གཅོད་', 'འཁོར་ལོ་'] == [t.content for t in tokens]


def test_missing_token44():
    input_str = "བཏུལ་མཚམས་བཅད་པ"
    tokens = tok.tokenize(input_str)
    assert ['བཏུལ་', 'མཚམས་', 'བཅད་པ'] == [t.content for t in tokens]


def test_missing_token45():
    input_str = "ཞལ་བྷ་ག་"
    tokens = tok.tokenize(input_str)
    assert ['ཞལ་', 'བྷ་', 'ག་'] == [t.content for t in tokens]


def test_missing_token46():
    input_str = "བསྐུར་ལས་ཀྱི་"
    tokens = tok.tokenize(input_str)
    assert ['བསྐུར་', 'ལས་', 'ཀྱི་'] == [t.content for t in tokens]


def test_missing_token47():
    input_str = "འཁོས་དུ། །ཆེ་"
    tokens = tok.tokenize(input_str)
    assert ['འཁོས་', 'དུ', '། ', '།', 'ཆེ་'] == [t.content for t in tokens]


def test_missing_token48():
    input_str = "ནུ་ཧེ་རུ་"
    tokens = tok.tokenize(input_str)
    assert ['ནུ་', 'ཧེ་', 'རུ་'] == [t.content for t in tokens]


def test_missing_token49():
    # པར
    input_str = "བརྩེགས་རྣམ་པར་"
    tokens = tok.tokenize(input_str)
    assert ['བརྩེགས་', 'རྣམ་པ', 'ར་'] == [t.content for t in tokens]


def test_missing_token50():
    input_str = "བྷ་གར་"
    tokens = tok.tokenize(input_str)
    assert ['བྷ་', 'གར་'] == [t.content for t in tokens]


def test_missing_token51():
    input_str = "ནུ་ཡེ་ཤེས་"
    tokens = tok.tokenize(input_str)
    assert ['ནུ་', 'ཡེ་ཤེས་'] == [t.content for t in tokens]


def test_missing_token52():
    input_str = "བརྩེགས་ངེས་པ་"
    tokens = tok.tokenize(input_str)
    assert ['བརྩེགས་', 'ངེས་པ་'] == [t.content for t in tokens]


def test_missing_token53():
    input_str = "བཟླས་བསྐུལ་གསུང་"
    tokens = tok.tokenize(input_str)
    assert ['བཟླས་', 'བསྐུལ་', 'གསུང་'] == [t.content for t in tokens]


def test_missing_token54():
    input_str = "བྷ་གར་འཁྱིལ། །ཨོཾ་"
    tokens = tok.tokenize(input_str)
    assert ['བྷ་', 'གར་', 'འཁྱིལ', '། ', '།', 'ཨོཾ་'] == [t.content for t in tokens]


def test_missing_token55():
    input_str = "བྷ་གར་སྦྱོར་"
    tokens = tok.tokenize(input_str)
    assert ['བྷ་', 'གར་', 'སྦྱོར་'] == [t.content for t in tokens]


def test_missing_token56():
    input_str = "བརྒྱུད་སྐུ་གདུང་"
    tokens = tok.tokenize(input_str)
    assert ['བརྒྱུད་', 'སྐུ་གདུང་'] == [t.content for t in tokens]


def test_missing_token57():
    input_str = "སྒལ་བརྒྱུད་ཞབས་"
    tokens = tok.tokenize(input_str)
    assert ['སྒལ་', 'བརྒྱུད་', 'ཞབས་'] == [t.content for t in tokens]


def test_missing_token58():
    input_str = "བརྩེགས་ཆེ་མཆོག་"
    tokens = tok.tokenize(input_str)
    assert ['བརྩེགས་', 'ཆེ་མཆོག་'] == [t.content for t in tokens]


def test_missing_token59():
    input_str = "།་གླེན་ལྐུགས་"
    tokens = tok.tokenize(input_str)
    assert ['།་', 'གླེན་ལྐུགས་'] == [t.content for t in tokens]
