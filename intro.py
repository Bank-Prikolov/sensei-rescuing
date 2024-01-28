import pygame
import sys
import start_screen
from load_image import load_image
from itemCreator import Button
import menu
from consts import *

pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('Sensei Rescuing')

bg_group_intro = pygame.sprite.Group()

cursor = load_image(r'objects\cursor-obj.png')
pygame.mouse.set_visible(False)


class AnimatedIntro(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(bg_group_intro)
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
                for _ in range(8):
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

    def update(self):
        if self.cur_frame < 30 * 8:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


bg_img = load_image(r"backgrounds\intro-bg.png")
bg_tr = pygame.transform.scale(bg_img, (bg_img.get_width() * 2, bg_img.get_height() * 2))
intro_bg = AnimatedIntro(bg_tr, 31, 1, WIDTH // 2 - 512,
                         HEIGHT // 2 - 145)


def intro():
    skalaSound = pygame.mixer.Sound(r"data\sounds\skala-sound.mp3")
    running = True
    fps = 60
    while running:

        screen.fill("#000000")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                skalaSound.play()

        if intro_bg.cur_frame >= 30 * 8:
            start_screen.start_screen()

        intro_bg.update()
        clock.tick(fps)
        bg_group_intro.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


# intro()
