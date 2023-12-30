import os, sys

test = 'pp_test_level.txt'


def generate_level(txt_file):
    fullname = os.path.join('data\levels', txt_file)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    level = fullname
    level_load = list(map(lambda x: x.rstrip('\n'), open(level).readlines()))
    for y in range(len(level_load)):                # y
        for x in range(len(level_load[y])):         # x
            print(level_load[y][x])


generate_level(test)