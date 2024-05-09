# import itertools
import random


def change_index(stroka: str, index, a):
    stroka = stroka[:index] + a + stroka[index + 1:]
    return stroka


def new_lvl():
    for i in range(1, 2):
        name = f'endless_{i}'
        fst = '#' + ''.join([('0', '&', '=')[random.randint(0, 2)] for _ in range(14)]) + '#\n'
        last = '#' + ''.join([('0', '&', '=')[random.randint(0, 2)] for _ in range(14)]) + '#\n'
        lvl = ['.' * 14] * 10
        x, y = random.randint(1, 12), random.randint(1, 9)
        lvl[y] = change_index(lvl[y], x, '@')
        for j in range(0, 3):
            if y + 1 <= 9:
                lvl[y + 1] = change_index(lvl[y + 1], x - 1 + j, ('0', '&', '=')[random.randint(0, 2)])
            if y - 1 >= 0:
                lvl[y - 1] = change_index(lvl[y - 1], x - 1 + j, 'x')
            if j in [0, 2]:
                lvl[y] = change_index(lvl[y], x - 1 + j, 'x')
        # for sl in range(1, random.randint(2, 6)):
        #     # slonchoice = list(range(0, 13)).remove(x), list(range(0, 13)).remove(y)
        #     sx, sy = random.choice(list(range(0, 13))), random.choice(list(range(0, 9)))
        #     lvl[sy] = change_index(lvl[sy], sx, 'e')

        print('\n'.join(lvl))
        lvl = fst + '#' + '#\n#'.join(lvl) + '#\n' + last
        lvl.replace('x', '.')
        with open(fr'data/levels/{name}.txt', 'w') as endres:
            endres.writelines(lvl)


new_lvl()
