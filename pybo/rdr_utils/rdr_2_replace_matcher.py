from collections import defaultdict

# variables
tag = "object.tag"
word = "object.word"
prev_tag = "object.prevTag"
next_tag = "object.nextTag"
prev_word = "object.prevWord"
next_word = "object.nextWord"
conclusion = "object.conclusion"
op = " == "
ccl_op = " = "
cond_sep = " and "
rule_sep = " : "
cql_rule_sep = " & "
level_sep = "\t"

positive = [tag, word, next_tag, next_word, conclusion]
negative = [prev_tag, prev_word]
eq_table = {
    tag: "pos",
    prev_tag: "pos",
    next_tag: "pos",
    conclusion: "pos",
    word: "text",
    prev_word: "text",
    next_word: "text",
}


def rdr_2_replace_matcher(string):
    cql = format_rules(find_rules(find_levels(string)))
    repl = " - repla: ['{match_cql}', {replace_index}, '{replace_cql}']"
    repls = [
        repl.format(match_cql=a, replace_index=b, replace_cql=c) for a, b, c in cql
    ]
    return "\n".join(repls)


def format_rules(rules):
    def generate_cql(test):
        if len(test) > 2:
            s, *_, e = sorted(test)
        elif len(test) == 2:
            s, e = sorted(test)
        else:
            s, e = 0, 0

        slots = []
        slot_zero_idx = None
        for num, t in enumerate(range(s, e + 1)):
            if t == 0:
                slot_zero_idx = num + 1

            if t in test:
                conds = [f"{eq_table[tag]}={pos}" for tag, pos in test[t]]
                slots.append("[" + cql_rule_sep.join(conds) + "]")
            else:
                slots.append("[]")
        assert slot_zero_idx is not None
        return " ".join(slots), slot_zero_idx

    cql = []
    for rule in rules:
        test_cql, idx = generate_cql(rule["test"])
        ccl_cql, _ = generate_cql(rule["ccl"])
        cql.append((test_cql, idx, ccl_cql))
    return cql


def find_levels(string):
    out = []
    for line in string.split("\n"):
        count = 0
        while line[0] == level_sep:
            count += 1
            line = line[1:]
        out.append((count, line))
    return out


def find_rules(lines):
    rules = []

    # state == {<level/int>: <test>, ...}
    # test == {<position/int>: (<tag>, <POS>), ...}
    state = {}
    for level, line in lines:
        tests, ccl = parse_line(line)
        ordered_tests = defaultdict(list)
        for t in tests:
            for pos, test in t.items():
                ordered_tests[pos].append(test)

        # save current rule in state to use in indented rules
        state[level] = ordered_tests

        # if level 0, pass. there is no rule to implement
        if level == 0:
            continue

        test = defaultdict(list)
        for l in range(level + 1):
            for pos, t in state[l].items():
                for u in t:
                    if u not in test[pos]:  # avoid duplicates
                        test[pos].append(u)
        rules.append({"test": test, "ccl": ccl})
    return rules


def parse_line(line):
    rule, ccl = line.split(rule_sep)
    tests = rule.split(cond_sep)
    ccl = parse_test(ccl)
    ccl[0] = [ccl[0]]
    tests = [parse_test(t) for t in tests]
    return tests, ccl


def parse_test(test):
    def parser(test, op):
        pos = 0
        attr, tag = test.split(op)
        for p in positive:
            if p in attr and len(attr) > len(p):
                pos = int(attr[-1])
                attr = attr[:-1]
        for n in negative:
            if n in attr and len(attr) > len(n):
                pos = -int(attr[-1])
                attr = attr[:-1]
        return attr, pos, tag

    if op in test:
        attr, pos, tag = parser(test, op)
    elif ccl_op in test:
        attr, pos, tag = parser(test, ccl_op)
    else:
        raise SyntaxError
    return {pos: (attr, tag)}
