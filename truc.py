from pybo import BoString

bo_str = 'བཀྲ་ཤིས་  tr  就到 郊外玩བདེ་ལེགས།'
bs = BoString(bo_str)

print(bs.base_structure)  # key: character index, value: character group
print(bs.get_categories())
