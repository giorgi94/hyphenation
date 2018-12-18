import re
import json


class Hyphenator:
    def __init__(self, patterns, exceptions=''):
        self.tree = {}
        for pattern in patterns.split():
            self._insert_pattern(pattern)

        self.exceptions = {}
        for ex in exceptions.split():
            # Convert the hyphenated pattern into a point array for use later.
            self.exceptions[ex.replace('-', '')] = [0] + [ int(h == '-') for h in re.split(r"[a-z]", ex) ]

    def _insert_pattern(self, pattern):
        # Convert the a pattern like 'a1bc3d4' into a string of chars 'abcd'
        # and a list of points [ 0, 1, 0, 3, 4 ].
        chars = re.sub('[0-9]', '', pattern)
        points = [int(d or 0) for d in re.split("[.ა-ჰ]", pattern)]

        # Insert the pattern into the tree.  Each character finds a dict
        # another level down in the tree, and leaf nodes have the list of
        # points.
        t = self.tree
        for c in chars:
            if c not in t:
                t[c] = {}
            t = t[c]
        t[None] = points

    def hyphenate_word(self, word):
        """ Given a word, returns a list of pieces, broken at the possible
            hyphenation points.
        """
        # Short words aren't hyphenated.
        if len(word) <= 4:
            return [word]
        # If the word is an exception, get the stored points.
        if word.lower() in self.exceptions:
            points = self.exceptions[word.lower()]
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



exceptions = ''

with open('hyph-ka.txt', 'r') as r:
	patterns = r.read()


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