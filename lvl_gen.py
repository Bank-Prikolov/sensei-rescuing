import pygame, os, sys


class Board:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = [[0] * w for _ in range(h)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, sc):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(sc, '#F1F1F1', (
                    self.left + (self.cell_size * x), self.top + (self.cell_size * y), self.cell_size, self.cell_size),
                                 1)

    def get_cell(self, mouse_pos):
        if self.left < mouse_pos[0] < self.left + (self.cell_size * self.width) and \
                self.top < mouse_pos[1] < self.top + (self.cell_size * self.height):
            return int((mouse_pos[0] - 10) / 30), int((mouse_pos[1] - 10) / 30)
        else:
            return None

    def get_size(self):
        return self.cell_size


def generate_level(txt_file):
    fullname = os.path.join('data\levels', txt_file)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    level = fullname
    level_load = list(map(lambda x: x.rstrip('\n'), open(level).readlines()))
    for y in range(len(level_load)):
        for x in range(len(level_load[y])):
            print(level_load[y][x])
