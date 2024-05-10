# import itertools
import random


def change_index(stroka: str, index, a):
    stroka = stroka[:index] + a + stroka[index + 1:]
    return stroka


def new_lvl(slozhnost=0):
    for i in range(1, 2):
        width, height = 14, 10
        name = f'endless_{i}'
        fst = '#' + ''.join([('0', '&', '=')[random.randint(0, 2)] for _ in range(14)]) + '#\n'
        last = '#' + ''.join([('0', '&', '=')[random.randint(0, 2)] for _ in range(14)]) + '#\n'
        lvl = ['.' * 14] * 10
        dostupnie = [[f'{x}' for x in range(width)] for _ in range(height)]
        # player
        plx, ply = random.randint(1, width - 2), random.randint(1, height - 1)
        lvl[ply] = change_index(lvl[ply], plx, '@')
        dostupnie[ply].remove(f'{plx}')
        for j in range(0, 3):
            if ply + 1 <= height - 1:
                lvl[ply + 1] = change_index(lvl[ply + 1], plx - 1 + j, '=')
                dostupnie[ply + 1].remove(f'{plx - 1 + j}')
            if ply - 1 >= 0:
                if j == 1:
                    lvl[ply - 1] = change_index(lvl[ply - 1], plx - 1 + j, '.')
                    dostupnie[ply - 1].remove(f'{plx - 1 + j}')
            if j in [0, 2]:
                lvl[ply] = change_index(lvl[ply], plx - 1 + j, '.')
                dostupnie[ply].remove(f'{plx - 1 + j}')
        # finish
        finy = random.randint(0, height - 1)
        finx = int(random.choice(dostupnie[finy]))
        dostupnie[finy].remove(str(finx))
        if i == 3:
            lvl[finy] = change_index(lvl[finy], finx, 'f')
        else:
            lvl[finy] = change_index(lvl[finy], finx, 'c')
        if finy < height - 1:
            lvl[finy + 1] = change_index(lvl[finy + 1], finx, '=')
            if str(finx) in dostupnie[finy + 1]:
                dostupnie[finy + 1].remove(str(finx))
        placedFin = False
        if finy > 0:
            if str(finx) in dostupnie[finy - 1]:
                lvl[finy - 1] = change_index(lvl[finy - 1], finx, '.')
                dostupnie[finy - 1].remove(str(finx))
            else:
                lvl[finy - 1] = change_index(lvl[finy - 1], finx, '_')
                placedFin = True

        if finx > 0:
            if str(finx - 1) in dostupnie[finy]:
                if placedFin:
                    lvl[finy] = change_index(lvl[finy], finx - 1, '_')
                    lvl[finy - 1] = change_index(lvl[finy], finx - 1, '_')
                else:
                    lvl[finy - 1] = change_index(lvl[finy - 1], finx - 1, '.')
                    lvl[finy] = change_index(lvl[finy], finx - 1, '.')
                if str(finx - 1) in dostupnie[finy - 1]:
                    dostupnie[finy - 1].remove(str(finx - 1))
                dostupnie[finy].remove(str(finx - 1))

        if finx < width:
            if str(finx + 1) in dostupnie[finy]:
                if placedFin:
                    lvl[finy] = change_index(lvl[finy], finx + 1, '_')
                    lvl[finy - 1] = change_index(lvl[finy - 1], finx + 1, '_')
                else:
                    lvl[finy] = change_index(lvl[finy], finx + 1, '.')
                    lvl[finy - 1] = change_index(lvl[finy - 1], finx + 1, '.')
                if str(finx - 1) in dostupnie[finy - 1]:
                    dostupnie[finy - 1].remove(str(finx + 1))
                dostupnie[finy - 1].remove(str(finx + 1))
                dostupnie[finy].remove(str(finx + 1))

        # map
        otstupx = plx - finx
        otstupy = ply - finy
        if otstupx > 0:
            runnumx = random.randint(1, min(otstupx, 4))
        elif otstupx < 0:
            runnumx = random.randint(max(otstupx, -4), -1)
        else:
            runnumx = 0
        if otstupy > 0:
            runnumy = random.randint(1, min(otstupy, 3))
        elif otstupy < 0:
            runnumy = random.randint(max(otstupy, -3), -1)
        else:
            runnumy = 0
        stenax = finx + runnumx
        stenay = finy + runnumy

        if otstupx == 0 and otstupy != 0:
            for x in range(width):
                if str(x) in dostupnie[stenay]:
                    lvl[stenay] = change_index(lvl[stenay], x, '=')
                    dostupnie[stenay].remove(str(x))
        elif otstupy == 0 and otstupx != 0:
            for y in range(height):
                if str(stenax) in dostupnie[y]:
                    lvl[y] = change_index(lvl[y], stenax, '=')
                    dostupnie[y].remove(str(stenax))
        else:
            if otstupy > 0:
                for y in range(stenay + 1):
                    if str(stenax) in dostupnie[y]:
                        lvl[y] = change_index(lvl[y], stenax, '=')
                        dostupnie[y].remove(str(stenax))
            elif otstupy < 0:
                for y in range(stenay, height):
                    if str(stenax) in dostupnie[y]:
                        lvl[y] = change_index(lvl[y], stenax, '=')
                        dostupnie[y].remove(str(stenax))
            if otstupx > 0:
                for x in range(stenax + 1):
                    if str(x) in dostupnie[stenay]:
                        lvl[stenay] = change_index(lvl[stenay], x, '=')
                        dostupnie[stenay].remove(str(x))
            elif otstupx < 0:
                for x in range(stenax, width):
                    if str(x) in dostupnie[stenay]:
                        lvl[stenay] = change_index(lvl[stenay], x, '=')
                        dostupnie[stenay].remove(str(x))

        floors = (random.choice(range(1, 5)),
                  random.choice(range(5, 7)),
                  random.choice(range(7, 10)))
        for y in floors:
            side = random.randint(0, 1)
            if side:
                for x in range(width):
                    if str(x) in dostupnie[y]:
                        lvl[y] = change_index(lvl[y], x, '=')
                        dostupnie[y].remove(str(x))
                    else:
                        break
            else:
                for x in range(width - 1, -1, -1):
                    if str(x) in dostupnie[y]:
                        lvl[y] = change_index(lvl[y], x, '=')
                        dostupnie[y].remove(str(x))
                    else:
                        break
        walls = (random.choice(range(1, 8)),
                 random.choice(range(8, 14)))
        for x in walls:
            side = random.randint(0, 1)
            if side:
                for y in range(height):
                    if str(x) in dostupnie[y]:
                        lvl[y] = change_index(lvl[y], x, '=')
                        dostupnie[y].remove(str(x))
                    else:
                        break
            else:
                for y in range(height - 1, -1, -1):
                    if str(x) in dostupnie[y]:
                        lvl[y] = change_index(lvl[y], x, '=')
                        dostupnie[y].remove(str(x))
                    else:
                        break

        square = []
        for x in range(width):
            line = []
            for y in range(height):
                line.append(lvl[y][x])
            square.append((line, x))
            if (x + 1) % 5 == 0 or x == 13:
                round = int((x + 1) / 5 + .5).__round__(0)
                odnastena = ['.=.' in ''.join(elem[0]) for elem in square]
                dvesteni = ['.==.' in ''.join(elem[0]) for elem in square]
                if any(odnastena):
                    choice = random.choice([el for el in range(len(square)) if odnastena[el]])
                    for changey in range(height - 2):
                        if ''.join([lvl[changey][choice + 5 * (round - 1)], lvl[changey + 1][choice + 5 * (round - 1)],
                                    lvl[changey + 2][choice + 5 * (round - 1)]]) == '.=.':
                            lvl[changey + 1] = change_index(lvl[changey + 1], choice + 5 * (round - 1), '_')
                            lvl[changey + 2] = change_index(lvl[changey + 2], choice + 5 * (round - 1), '_')
                if any(dvesteni):
                    choice = random.choice([el for el in range(len(square)) if dvesteni[el]])
                    for changey in range(height - 3):
                        if ''.join([lvl[changey][choice + 5 * (round - 1)], lvl[changey + 1][choice + 5 * (round - 1)],
                                    lvl[changey + 2][choice + 5 * (round - 1)],
                                    lvl[changey + 3][choice + 5 * (round - 1)]]) == '.==.':
                            lvl[changey + 1] = change_index(lvl[changey + 1], choice + 5 * (round - 1), '_')
                            lvl[changey + 2] = change_index(lvl[changey + 2], choice + 5 * (round - 1), '_')
                            lvl[changey + 3] = change_index(lvl[changey + 3], choice + 5 * (round - 1), '_')
                for linex in range(width):
                    for liney in range(height - 2):
                        if ''.join([lvl[liney][linex], lvl[liney + 1][linex],
                                    lvl[liney + 2][linex]]) in ['_._', '__.', '_..']:
                            lvl[liney] = change_index(lvl[liney], linex, '_')
                            lvl[liney + 1] = change_index(lvl[liney + 1], linex, '_')
                            lvl[liney + 2] = change_index(lvl[liney + 2], linex, '_')

                square = []

        # kolvoslonikov = random.randint(1, min(2 + slozhnost, 5))
        # lvl[y] = change_index(lvl[y], x, ('0', '&', '=')[random.randint(0, 2)])
        # for slon in range(kolvoslonikov):
        #     sx, sy = random.ra
        #     sx, sy = random.choice(list(range(0, 13))), random.choice(list(range(0, 9)))
        #     lvl[sy] = change_index(lvl[sy], sx, 'e')
        # print(*dostupnie, sep='\n')
        print('\n'.join(lvl))
        lvl = fst + '#' + '#\n#'.join(lvl) + '#\n' + last
        lvl.replace('x', '.')
        with open(fr'data/levels/{name}.txt', 'w') as endres:
            endres.writelines(lvl)


new_lvl()
