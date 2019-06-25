from pybo import *

tok = WordTokenizer('GMD')
# tok.tok.trie.rebuild_trie()


def test_missing_token1():
    input_str = "འཐུང་བུད་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['འཐུང་', 'བུད་']


def test_missing_token2():
    input_str = "ཨ་དྷྱིད་ཤུ་ཀ་ར་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ཨ་', 'དྷྱིད་', 'ཤུ་ཀ་', 'ར་']


def test_missing_token3():
    input_str = "ཀི་བི་ཏི་སྭཱ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ཀི་', 'བི་ཏི་', 'སྭཱ་']


def test_missing_token4():
    input_str = "ལང་ཏང་ཙེ་དང་བྱེ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ལང་', 'ཏང་', 'ཙེ་', 'དང་', 'བྱེ་']


def test_missing_token5():
    input_str = "ད་མེད་བྷ་གར་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ད་', 'མེད་', 'བྷ་གར་']


def test_missing_token6():
    input_str = "རབ་བསྐུས་ནས།"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['རབ་', 'བསྐུས་', 'ནས', '།']


def test_missing_token7():
    input_str = "གདབ། །ཨོཾ་ན་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['གདབ', '། །', 'ཨོཾ་', 'ན་']


def test_missing_token8():
    input_str = "བི་སི་ནི་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བི་', 'སི་', 'ནི་']


def test_missing_token9():
    input_str = "བསྐོལ། །རྡོ་རྗེ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བསྐོལ', '། །', 'རྡོ་རྗེ་']


def test_missing_token10():
    input_str = "བསྐུས་ཤིང་མཉེས་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བསྐུས་', 'ཤིང་', 'མཉེས་']


def test_missing_token11():
    input_str = "སྦོམ་ཞིང་ཆེ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['སྦོམ་', 'ཞིང་', 'ཆེ་']


def test_missing_token12():
    input_str = "བྷ་ག་ཁ་ཆེ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བྷ་ག་', 'ཁ་ཆེ་']


def test_missing_token13():
    input_str = "།ཨོཾ་གི་རི་ཧི་རི་ཙི་རི། །ཨཱ་ཨཱ་ཤུ་མ་ཤ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['།', 'ཨོཾ་', 'གི་རི་', 'ཧི་', 'རི་', 'ཙི་', 'རི', '། །', 'ཨཱ་', 'ཨཱ་ཤུ་', 'མ་', 'ཤ་']


def test_missing_token14():
    input_str = "བཟླས་བྱས་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བཟླས་', 'བྱས་']


def test_missing_token15():
    input_str = "བསྣམས། །རྩི་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བསྣམས', '། །', 'རྩི་']


def test_missing_token16():
    input_str = "ནཱ་ཤ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ནཱ་ཤ་']


def test_missing_token17():
    input_str = "གནོས་སྨྱོ་བྱེད་བརྗེད་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['གནོས་', 'སྨྱོ་བྱེད་', 'བརྗེད་']


def test_missing_token18():
    input_str = "གདོད་ཟིན་པ"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['གདོད་', 'ཟིན་པ']


def test_missing_token19():
    input_str = "བསྲེས་དམར་ནག་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བསྲེས་', 'དམར་ནག་']


def test_missing_token20():
    input_str = "བརྗེ་ཞིང་བསྐྱར་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བརྗེ་', 'ཞིང་', 'བསྐྱར་']


def test_missing_token21():
    input_str = "འཆང་མའི།"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['འཆང་', 'མའི', '།']


def test_missing_token22():
    input_str = "དམོད་གཟུག་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['དམོད་', 'གཟུག་']


def test_missing_token23():
    input_str = "བཤགས་ན་བུ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བཤགས་', 'ན་', 'བུ་']


def test_missing_token24():
    input_str = "མཐོལ་མགོ་ལ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['མཐོལ་', 'མགོ་', 'ལ་']


def test_missing_token25():
    input_str = "ཧུ་ཧཾ།"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ཧུ་', 'ཧཾ', '།']


def test_missing_token26():
    input_str = "སྲི་མོ་བཛྲ་ནོ་ཏི་སྟ་ཀཱི་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['སྲི་', 'མོ་', 'བཛྲ་', 'ནོ་', 'ཏི་', 'སྟ་', 'ཀཱི་']


def test_missing_token27():
    input_str = "གུམ་དང་།"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['གུམ་', 'དང་', '།']


def test_missing_token28():
    input_str = "ཡོལ་གྱིས"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ཡོལ་', 'གྱིས']


def test_missing_token29():
    input_str = "སྐུད་སྣ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['སྐུད་', 'སྣ་']


def test_missing_token30():
    input_str = "བཀྲ་མ།"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བཀྲ་', 'མ', '།']


def test_missing_token31():
    input_str = "གདོད་པར་བྱ"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['གདོད་', 'པར་', 'བྱ']


def test_missing_token32():
    input_str = "བསྒྲིབས་ཡོངས་སུ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བསྒྲིབས་', 'ཡོངས་སུ་']


def test_missing_token33():
    input_str = "དྲངས་ནས།"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['དྲངས་', 'ནས', '།']


def test_missing_token34():
    input_str = "རཱུ་ཏྲ་ཀྵ་གནས་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['རཱུ་', 'ཏྲ་', 'ཀྵ་', 'གནས་']


def test_missing_token35():
    input_str = "ལྡང་པ་ན།"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ལྡང་', 'པ་', 'ན', '།']


def test_missing_token36():
    input_str = "བསྲུབས་བྱས་པས། །ལྟེ་ལྐོག་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བསྲུབས་', 'བྱས་པས', '། །', 'ལྟེ་', 'ལྐོག་']


def test_missing_token37():
    input_str = "བསྟུན་ལ་ཉམས་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བསྟུན་', 'ལ་', 'ཉམས་']


def test_missing_token38():
    input_str = "ཥ་ཡིག་རྣམ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ཥ་', 'ཡིག་', 'རྣམ་']


def test_missing_token39():
    input_str = "འཛོམ། །རྣོ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['འཛོམ', '། །', 'རྣོ་']


def test_missing_token40():
    input_str = "པྲི་ཡིག་དམར་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['པྲི་', 'ཡིག་', 'དམར་']


def test_missing_token41():
    input_str = "གཏུམ་བྱེད་དང་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['གཏུམ་', 'བྱེད་', 'དང་']


def test_missing_token42():
    input_str = "ཞིབ་བས་སྦལ།"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ཞིབ་', 'བས་', 'སྦལ', '།']


def test_missing_token43():
    input_str = "གཅོད་འཁོར་ལོ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['གཅོད་', 'འཁོར་ལོ་']


def test_missing_token44():
    input_str = "བཏུལ་མཚམས་བཅད་པ"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བཏུལ་', 'མཚམས་', 'བཅད་པ']


def test_missing_token45():
    input_str = "ཞལ་བྷ་ག་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ཞལ་', 'བྷ་ག་']


def test_missing_token46():
    input_str = "བསྐུར་ལས་ཀྱི་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བསྐུར་', 'ལས་', 'ཀྱི་']


def test_missing_token47():
    input_str = "འཁོས་དུ། །ཆེ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['འཁོས་', 'དུ', '། །', 'ཆེ་']


def test_missing_token48():
    input_str = "ནུ་ཧེ་རུ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ནུ་', 'ཧེ་རུ་']


def test_missing_token49():
    input_str = "བརྩེགས་རྣམ་པར་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བརྩེགས་', 'རྣམ་པར་']


def test_missing_token50():
    input_str = "བྷ་གར་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བྷ་གར་']


def test_missing_token51():
    input_str = "ནུ་ཡེ་ཤེས་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ནུ་', 'ཡེ་ཤེས་']


def test_missing_token52():
    input_str = "བརྩེགས་ངེས་པ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བརྩེགས་', 'ངེས་པ་']


def test_missing_token53():
    input_str = "བཟླས་བསྐུལ་གསུང་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བཟླས་', 'བསྐུལ་', 'གསུང་']


def test_missing_token54():
    input_str = "བྷ་གར་འཁྱིལ། །ཨོཾ་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བྷ་གར་', 'འཁྱིལ', '། །', 'ཨོཾ་']


def test_missing_token55():
    input_str = "བྷ་གར་སྦྱོར་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བྷ་གར་', 'སྦྱོར་']


def test_missing_token56():
    input_str = "བརྒྱུད་སྐུ་གདུང་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བརྒྱུད་', 'སྐུ་གདུང་']


def test_missing_token57():
    input_str = "སྒལ་བརྒྱུད་ཞབས་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['སྒལ་', 'བརྒྱུད་', 'ཞབས་']


def test_missing_token58():
    input_str = "བརྩེགས་ཆེ་མཆོག་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['བརྩེགས་', 'ཆེ་མཆོག་']


def test_missing_token59():
    input_str = "།་གླེན་ལྐུགས་"
    tokens = tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['།་', 'གླེན་ལྐུགས་']
