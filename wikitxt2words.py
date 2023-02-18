#!/usr/bin/env python

import re


PATH_EO_WIKI_TXT      = 'wiki.txt'
PATH_EO_OTHER_SOURCES = ['eo_other_source.txt']
PATH_EO_CAPITALS      = 'eo_caps.txt'
PATH_EO_WORDS         = 'eo_words.txt'

EO_CAPS         = u'ABCDEFGHIJKLMNOPRSTUVZĈĜĤĴŜŬ'
EO_LOWERS       = u'abcdefghijklmnoprstuvzĉĝĥĵŝŭ'
RE_EO_IS_WORD   = re.compile(u'^[' + EO_LOWERS + EO_CAPS + '-]+\.?$')
RE_EO_HAS_CAP   = re.compile(u'[' + EO_CAPS + ']')
RE_EO_HAS_VOWEL = re.compile(u'[aeiou]')

EO_OTHER_SOURCE_BLOCKED = ["edz'-edzino"
                          , "edz-edzino"
                          , "krucistoj-hundfratoj"
                          , "kvardek-ok-jara"]


def mk_primary_sets(fname_words, fname_caps):
    def remove_final_period(s):
        if s[-1] == '.':
            s = s[0:-1]
        return s

    # Don't remove periods. Avoid "foo.com" ==> "foo com".
    tr_map = str.maketrans('(),:;"\'', ' '*7)

    primary_caps  = set()
    primary_words = set()
    with open('wiki.txt', 'r') as f:
        for line in [line.strip().translate(tr_map)
                        for line in f.readlines()]:
            if len(line) == 0 or (line[-1] == ':' and len(line.split()) <= 10):
                continue  # Likely a page name. Might not be in target language.
            for word in [remove_final_period(w)
                           for w in line.split()
                           if re.search(RE_EO_IS_WORD, w) and len(w) > 1]:
                if (word[0] == '-' or word[-1] == '-'
                    or '--' in word or not re.search(RE_EO_HAS_VOWEL, word)):
                    continue

                if re.search(RE_EO_HAS_CAP, word):
                    primary_caps.add(word)
                else:
                    primary_words.add(word)
    return (primary_words, primary_caps)


def mk_secondary_sets(primary_words, primary_caps, fnames):
    secondary_caps  = set()
    secondary_words = set()
    for fname in fnames:
        with open(fname, 'r') as f_other:
            for word in [line.strip() for line in f_other.readlines()]:
                if word[0] == '#' or word in EO_OTHER_SOURCE_BLOCKED:
                    continue
                if re.search(RE_EO_HAS_CAP, word):
                    if word not in primary_caps:
                        secondary_caps.add(word)
                elif word not in primary_words:
                    secondary_words.add(word)
    return (secondary_words, secondary_caps)


def write_set_to_file(set_, fname, do_sort=True):
    with open(fname, 'w') as f:
        src = sorted(set_) if do_sort else set_
        for word in src:
            print(f'{word}', file=f)


if __name__ == '__main__':
    (eo_words, eo_caps)   = mk_primary_sets(PATH_EO_WORDS, PATH_EO_CAPITALS)
    (eo_words2, eo_caps2) = mk_secondary_sets(
                                eo_words, eo_caps, PATH_EO_OTHER_SOURCES)
    eo_words = eo_words.union(eo_words2)
    eo_caps  = eo_words.union(eo_caps)
    write_set_to_file(eo_words, 'eo_words.txt')
    write_set_to_file(eo_caps,  'eo_caps.txt')
