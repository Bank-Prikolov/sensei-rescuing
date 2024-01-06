import pygame, sys, screeninfo
from load_image import *
from buttons import Button
from const import *

pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('Sensei Rescuing')

bg_group = pygame.sprite.Group()


class AnimatedStartScreen(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(bg_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


bg_img = load_image("start-screen-bg.png")
start_bg = AnimatedStartScreen(bg_img, 46, 1, WIDTH // 2 - 320,
                               HEIGHT // 2 - 145)


def start_screen():
    running = True
    fps = 5
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    start_bg.update()
    clock.tick(fps)
    bg_group.draw(screen)
    pygame.display.flip()


start_screen()
