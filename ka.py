import json
import re

with open('tree.json', 'r') as fp:
    tree = json.load(fp)


def hyphenate_word(word):
    if len(word) <= 4:
        return [word]

    work = '.' + word + '.'
    points = [0] * (len(work)+1)
    for i in range(len(work)):
        t = tree
        for c in work[i:]:
            if c in t:
                t = t[c]
                if 'null' in t:
                    p = t['null']
                    for j in range(len(p)):
                        points[i+j] = max(points[i+j], p[j])
            else:
                break
    # No hyphens in the first two chars or the last two.
    points[1] = points[2] = points[-2] = points[-3] = 0

    # print(points)

    # Examine the points to build the pieces list.
    pieces = ['']
    for c, p in zip(word, points[2:]):
        pieces[-1] += c
        if p % 2:
            pieces.append('')
    return pieces


if __name__ == '__main__':

    # sentence = 'დედაქალაქის'

    # print('-'.join(hyphenate_word(sentence)))

    with open('/home/gio/Documents/Books/NumericalGames/Schwarz-Christoffel/reperati/gk_article.tex', 'r') as f:
        text = f.read()

    words = re.findall(r'[ა-ჰ]+', text)

    hyphed_words = ['-'.join(hyphenate_word(w)) for w in words]

    with open('hyphenation.tex', 'w') as f:

        f.write('\\hyphenation{%s}' % ' '.join(hyphed_words))
