# import itertools
import random


def change_index(stroka: str, index, a):
    stroka = stroka[:index] + a + stroka[index + 1:]
    return stroka


def new_lvl(slozhnost=0):
    for i in range(1, 4):
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
                    lvl[finy - 1] = change_index(lvl[finy - 1], finx - 1, '_')
                else:
                    lvl[finy - 1] = change_index(lvl[finy - 1], finx - 1, '.')
                    lvl[finy] = change_index(lvl[finy], finx - 1, '.')
                if finy < 9:
                    lvl[finy + 1] = change_index(lvl[finy + 1], finx - 1, '_')
                    lvl[finy] = change_index(lvl[finy], finx - 1, '_')
                    if str(finx - 1) in dostupnie[finy]:
                        lvl[finy] = change_index(lvl[finy], finx - 1, '_')
                    if str(finx - 1) in dostupnie[finy + 1]:
                        dostupnie[finy + 1].remove(str(finx - 1))
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
                if finy < 9:
                    lvl[finy + 1] = change_index(lvl[finy + 1], finx + 1, '_')
                    lvl[finy] = change_index(lvl[finy], finx + 1, '_')
                    if str(finx + 1) in dostupnie[finy + 1]:
                        dostupnie[finy + 1].remove(str(finx + 1))
                if str(finx - 1) in dostupnie[finy - 1]:
                    dostupnie[finy - 1].remove(str(finx - 1))
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
                                    lvl[liney + 2][linex]]) in ['_._', '__.', '_=.']:
                            lvl[liney] = change_index(lvl[liney], linex, '_')
                            lvl[liney + 1] = change_index(lvl[liney + 1], linex, '_')
                            lvl[liney + 2] = change_index(lvl[liney + 2], linex, '_')

                square = []
        for wally2 in range(height):
            if '___' in lvl[wally2]:
                lvl[wally2] = lvl[wally2].replace('___', '._.')

        for wally2 in range(height):
            if '__' in lvl[wally2]:
                lvl[wally2] = lvl[wally2].replace('__', random.choice(['_.', '._']))

        for wally in range(height):
            if '.=.' in lvl[wally]:
                if wally != 9:
                    if (lvl[wally + 1][lvl[wally].index('.=.'): lvl[wally].index('.=.') + 3]
                            in ['===', '.==', '==.', '..=', '=..'] + ['===', '_==', '==_', '__=', '=__']):
                        lvl[wally] = lvl[wally].replace('.=.', '...')
                else:
                    lvl[wally] = lvl[wally].replace('.=.', '...')
            if '_=.' in lvl[wally]:
                if wally != 9:
                    if (lvl[wally + 1][lvl[wally].index('_=.'): lvl[wally].index('_=.') + 3]
                            in ['===', '.==', '==.', '..=', '=..'] + ['===', '_==', '==_', '__=', '=__']):
                        lvl[wally] = lvl[wally].replace('_=.', '_..')
                else:
                    lvl[wally] = lvl[wally].replace('_=.', '_..')
            if '.=_' in lvl[wally]:
                if wally != 9:
                    if (lvl[wally + 1][lvl[wally].index('.=_'): lvl[wally].index('.=_') + 3]
                            in ['===', '.==', '==.', '..=', '=..', '_==', '==_', '__=', '=__']):
                        lvl[wally] = lvl[wally].replace('.=_', '.._')
                else:
                    lvl[wally] = lvl[wally].replace('.=_', '.._')
            if '_=_' in lvl[wally]:
                if wally != 9:
                    if (lvl[wally + 1][lvl[wally].index('_=_'): lvl[wally].index('_=_') + 3]
                            in ['===', '.==', '==.', '..=', '=..', '===', '_==', '==_', '__=', '=__']):
                        lvl[wally] = lvl[wally].replace('_=_', '_._')
                else:
                    lvl[wally] = lvl[wally].replace('_=_', '_._')
            if '.==.' in lvl[wally]:
                ind = lvl[wally].index('.==.')
                if wally != 9:
                    if (lvl[wally + 1][lvl[wally].index('.==.'): lvl[wally].index('.==.') + 4]
                            in ['====', '.===', '===.', '..==', '==..', '=..=']):
                        lvl[wally] = change_index(lvl[wally], ind + 1, '.')
                        lvl[wally] = change_index(lvl[wally], ind + 2, '.')
                else:
                    lvl[wally] = change_index(lvl[wally], ind + 1, '.')
                    lvl[wally] = change_index(lvl[wally], ind + 2, '.')

        if finy < height - 1:
            lvl[finy + 1] = change_index(lvl[finy + 1], finx, '=')
            if str(finx) in dostupnie[finy + 1]:
                dostupnie[finy + 1].remove(str(finx))

        # slons
        xcounter = 0
        for slony in range(1, height):
            if '==_' in lvl[slony] or '_==' in lvl[slony] or '==.' in lvl[slony] or '.==' in lvl[slony] or '===' in lvl[slony]:
                for slonx in range(width - 2):
                    fullhouse = ''.join([lvl[slony][slonx], lvl[slony][slonx + 1], lvl[slony][slonx + 2]])
                    if (fullhouse == '_==' and lvl[slony - 1][slonx + 2] == '.'
                            and not (plx in [slonx + 3, slonx + 1] and ply == slony - 1)
                            and '=' not in lvl[slony - 1][slonx:slonx + 3]):
                        lvl[slony - 1] = change_index(lvl[slony - 1], slonx + 2, 'x')
                        xcounter += 1
                    elif (fullhouse == '==_' and lvl[slony - 1][slonx] == '.'
                            and not (plx in [slonx - 1, slonx + 1] and ply == slony - 1)
                            and '=' not in lvl[slony - 1][slonx:slonx + 3]):
                        lvl[slony - 1] = change_index(lvl[slony - 1], slonx, 'x')
                        xcounter += 1
                    elif (fullhouse == '==.' and lvl[slony - 1][slonx] == '.'
                            and not (plx in [slonx - 1, slonx + 1] and ply == slony - 1)
                            and '=' not in lvl[slony - 1][slonx:slonx + 3]):
                        lvl[slony - 1] = change_index(lvl[slony - 1], slonx, 'x')
                        xcounter += 1
                    elif (fullhouse == '==.' and lvl[slony - 1][slonx] == '.'
                            and not (plx in [slonx - 1, slonx + 1] and ply == slony - 1)
                            and '=' not in lvl[slony - 1][slonx:slonx + 3]):
                        lvl[slony - 1] = change_index(lvl[slony - 1], slonx, 'x')
                        xcounter += 1
                    elif fullhouse == '===':
                        if (lvl[slony - 1][slonx + 2] == '.'
                                and not (plx in [slonx + 3, slonx + 1] and ply == slony - 1)
                                and '=' not in lvl[slony - 1][slonx:slonx + 3]):
                            lvl[slony - 1] = change_index(lvl[slony - 1], slonx + 2, 'x')
                            xcounter += 1
                        if (lvl[slony - 1][slonx] == '.'
                              and not (plx in [slonx - 1, slonx + 1] and ply == slony - 1)
                              and '=' not in lvl[slony - 1][slonx:slonx + 3]):
                            lvl[slony - 1] = change_index(lvl[slony - 1], slonx, 'x')
                            xcounter += 1
            if slony == height - 1:
                for pereslonche in range(width - 2):
                    fullhouse = ''.join([lvl[slony][pereslonche], lvl[slony][pereslonche + 1], lvl[slony][pereslonche + 2]])
                    if fullhouse == '...':
                        lvl[slony] = change_index(lvl[slony], pereslonche + random.choice([0, 2]), 'x')
                        xcounter += 1

        for slony2 in range(height):
            if '@' in lvl[slony2] and 'x' in lvl[slony2]:
                for slonremover in range(width):
                    if lvl[slony2][slonremover] == 'x':
                        lvl[slony2] = change_index(lvl[slony2], slonremover, '.')
                        xcounter -= 1
            else:
                if 'xx' in lvl[slony2]:
                    for slonx2 in range(width - 1):
                        fullhouse = ''.join([lvl[slony2][slonx2], lvl[slony2][slonx2 + 1]])
                        if fullhouse == 'xx':
                            lvl[slony2] = change_index(lvl[slony2], slonx2 + random.randint(0, 1), '.')
                            xcounter -= 1

        if min(4 + 1 * slozhnost, min(10, xcounter)) != 0:
            if min(4 + 1 * slozhnost, min(10, xcounter)) >= 3:
                kolvo = random.randint(2, min(4 + 1 * slozhnost, min(10, xcounter)))
            else:
                a = min(4 + 1 * slozhnost, min(10, xcounter))
                kolvo = random.randint(a - 1, a)
            choices = sorted(random.choices(range(1, xcounter + 1), k=kolvo))
            xcounter = 0
            for endy in range(height):
                for endx in range(width):
                    if lvl[endy][endx] == 'x':
                        xcounter += 1
                        if xcounter in choices:
                            lvl[endy] = change_index(lvl[endy], endx, 'e')
                        else:
                            lvl[endy] = change_index(lvl[endy], endx, '.')
        for hei in range(height):
            for wid in range(width):
                if lvl[hei][wid] == '=':
                    lvl[hei] = change_index(lvl[hei], wid, ['0', '&', '='][random.randint(0, 2)])

        # print('\n'.join(lvl))
        lvl = fst + '#' + '#\n#'.join(lvl) + '#\n' + last
        lvl.replace('x', '.')
        with open(fr'data/levels/{name}.txt', 'w') as endres:
            endres.writelines(lvl)


# new_lvl()
