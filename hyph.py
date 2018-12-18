import re
import json


def hyphenate_word(tree, word, exceptions={}):
    if len(word) <= 4:
        return [word]

    if word.lower() in exceptions:
        points = exceptions[word.lower()]
    else:
        work = '.' + word.lower() + '.'
        points = [0] * (len(work)+1)
        for i in range(len(work)):
            t = self.tree
            for c in work[i:]:
                if c in t:
                    t = t[c]
                    if None in t:
                        p = t[None]
                        for j in range(len(p)):
                            points[i+j] = max(points[i+j], p[j])
                else:
                    break
        # No hyphens in the first two chars or the last two.
        points[1] = points[2] = points[-2] = points[-3] = 0

    # Examine the points to build the pieces list.
    pieces = ['']
    for c, p in zip(word, points[2:]):
        pieces[-1] += c
        if p % 2:
            pieces.append('')
    return pieces


hyphenator = Hyphenator(patterns, exceptions)
hyphenate_word = hyphenator.hyphenate_word


tree = hyphenator.tree

# with open('tree.json', 'w') as f:
# 	json.dump(tree, f, ensure_ascii=False, indent=4)


del patterns
del exceptions

if __name__ == '__main__':

    sentence = 'დედაქალაქის'

    print('-'.join(hyphenate_word(sentence)))
