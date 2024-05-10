# import itertools
import random


def change_index(stroka: str, index, a):
    stroka = stroka[:index] + a + stroka[index + 1:]
    return stroka


def new_lvl():
    for i in range(1, 2):
        kletki =[range(0, )]
        name = f'endless_{i}'
        fst = '#' + ''.join([('0', '&', '=')[random.randint(0, 2)] for _ in range(14)]) + '#\n'
        last = '#' + ''.join([('0', '&', '=')[random.randint(0, 2)] for _ in range(14)]) + '#\n'
        lvl = ['.' * 14] * 10
        dostupnie = [[f'{x}' for x in range(14)] for y in range(10)]
        # dostupnie = [list(range(0, 14))] * 10
        # player
        plx, ply = random.randint(1, 12), random.randint(1, 9)
        lvl[ply] = change_index(lvl[ply], plx, '@')
        dostupnie[ply].remove(f'{plx}')
        for j in range(0, 3):
            if ply + 1 <= 9:
                lvl[ply + 1] = change_index(lvl[ply + 1], plx - 1 + j, ('0', '&', '=')[random.randint(0, 2)])
                dostupnie[ply + 1].remove(f'{plx - 1 + j}')
            if ply - 1 >= 0:
                lvl[ply - 1] = change_index(lvl[ply - 1], plx - 1 + j, 'x')
                dostupnie[ply - 1].remove(f'{plx - 1 + j}')
            if j in [0, 2]:
                lvl[ply] = change_index(lvl[ply], plx - 1 + j, 'x')
                dostupnie[ply].remove(f'{plx - 1 + j}')
        # finish
        finy = random.randint(0, 13)
        print(finy)
        finx = int(random.choice(dostupnie[finy]))
        lvl[finy] = change_index(lvl[finy], finx, 'f')
        if finy < 9:
            lvl[finy + 1] = change_index(lvl[finy + 1], finx, ('0', '&', '=')[random.randint(0, 2)])
        if finx < 13:
            lvl[finy] = change_index(lvl[finy], finx + 1, 'x')
        if finx > 0:
            lvl[finy] = change_index(lvl[finy], finx - 1, 'x')
        # map


        #     # slonchoice = list(range(0, 13)).remove(x), list(range(0, 13)).remove(y)
        #     sx, sy = random.choice(list(range(0, 13))), random.choice(list(range(0, 9)))
        #     lvl[sy] = change_index(lvl[sy], sx, 'e')
        print(*dostupnie, sep='\n')
        print('\n'.join(lvl))
        lvl = fst + '#' + '#\n#'.join(lvl) + '#\n' + last
        lvl.replace('x', '.')
        with open(fr'data/levels/{name}.txt', 'w') as endres:
            endres.writelines(lvl)


new_lvl()
