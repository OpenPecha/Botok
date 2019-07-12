def find_all_matches(in_str, pos, vocab):
    sub_str = in_str[pos:]
    matches = []
    for word in vocab:
        if sub_str.startswith(word):
            matches.append([word])
    return matches


# should not be used/useful anymore since the parse with most frequent words is kept
def flatten(arr):
    for i in arr:
        if isinstance(i, list):
            yield from flatten(i)
        else:
            yield i


def find_least_advanced(paths, closed):
    sizes = [(len(''.join(flatten(p))), n) for n, p in enumerate(paths) if not closed[n]]
    smaller = sorted(sizes)
    return smaller[0][1]


def get_path_lens(paths):
    flat = [flatten(path) for path in paths]
    return [len(''.join(p)) for p in flat]


def is_equal_path_end_idx(paths):
    return len(set(get_path_lens(paths))) == 1


def walk_all_paths(paths, pos, closed=None):
    if closed is None:
        closed = {n: False for n in range(len(paths))}
    if set(closed.values()) == {True} or is_equal_path_end_idx(paths):
        return

    least_advanced = find_least_advanced(paths, closed)
    start = pos + len(paths[least_advanced])
    matches = find_all_matches(in_str, start, vocab)

    if not matches:
        closed[least_advanced] = True
        walk_all_paths(paths, pos, closed)

    elif len(matches) == 1:
        paths[least_advanced] += matches[0]
        lens = get_path_lens(matches)
        pos_incr = sorted(list(set(lens)))[0] - 1
        walk_all_paths(paths, pos + pos_incr, closed)

    elif len(matches) > 1:
        chosen_path = matches[most_frequent_path(matches)]
        paths[least_advanced] += chosen_path
        walk_all_paths(paths, start, closed)

    if is_equal_path_end_idx(paths):
        walk_all_paths(paths, pos, closed)


def most_frequent_path(paths):
    frequencies = [(sum([freqs[word] for word in path]), n) for n, path in enumerate(paths)]
    return sorted(frequencies, reverse=True)[0][1]
    # make it so that in case of equal freq, defaults to maxmatch


in_str = 'abcdefghi'
vocab = ['a', 'ab', 'b', 'd', 'def', 'efg', 'fg', 'gh', 'ghi', 'i']
freqs = {'a': 0,
         'ab': 50,
         'b': 10,
         'd': 0,
         'def': 50,
         'efg': 7,
         'fg': 15,
         'gh': 50,
         'ghi': 3,
         'i': 20
         }

results = []
pos = 0
while pos < len(in_str):
    matches = find_all_matches(in_str, pos, vocab)
    if not matches:
        results.append(f'_{in_str[pos]}_')
    elif len(matches) == 1:
        results.append(matches[0][0])
        pos += len(matches[0]) - 1
    elif len(matches) > 1:
        walk_all_paths(matches, pos)
        chosen_path = matches[most_frequent_path(matches)]
        results += chosen_path

        pos_incr = sum(get_path_lens(chosen_path))
        pos += pos_incr - 1

    pos += 1

print(results)