from typing import List, NewType

from pybo import BoPipeline, Token

PyboToken = NewType('PyboToken', Token)


def test_pipeline():
    pipeline = BoPipeline(profile='pybo_raw_types')
    pipeline.prof = 'POS'  # override the GMD profile from pybo_raw_types
    result = pipeline.pipe_str(' ཤི་བཀྲ་ཤིས་  tr བདེ་ལེགས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ x  བཀྲ་ཤིས་')
    expected = """བཀྲ་ཤིས་	2
ཤི་	1
བཀྲ་ཤིས་ 	1
tr 	1
བདེ་ལེགས	1
། 	1
བདེ་ལེགས་	1
ཀཀ 	1
x 	1"""
    assert expected == result


def test_add_custom_pipes():
    # create custom pipe
    def pybo_pos(tokens: List[PyboToken]) -> List[str]:
        """transforms the pybo tokens into word/POS format
        replaces spaces in the tokens by underscores
        """

        return [f'{t["cleaned_content"].replace(" ", "_")}/{t["pos"]}' for t in tokens]

    # create the pipe to be injected in the pipeline
    pipes = {'proc': {'pybo_pos': pybo_pos}}

    # create a profile using the new pipe to be injected
    profile = {'pybo_pos': {
                            'pre': 'pre_basic',
                            'tok': 'pybo',
                            'pybo_profile': 'POS',
                            'proc': 'pybo_pos',
                            'frm': 'plaintext'}}

    pipeline = BoPipeline(profile=profile, new_pipes=pipes)

    result = pipeline.pipe_str(' ཤི་བཀྲ་ཤིས་  tr བདེ་ལེགས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ x  བཀྲ་ཤིས་')
    expected = 'ཤི་/VERB བཀྲ་ཤིས་/NOUN /non-bo བདེ་ལེགས་/NOUN /punct བཀྲ་ཤིས་/NOUN ' \
               'བདེ་ལེགས་/NOUN ཀཀ་/non-word /non-bo བཀྲ་ཤིས་/NOUN'
    assert expected == result
