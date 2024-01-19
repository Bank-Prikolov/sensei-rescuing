import pygame
import sys
from load_image import load_image
from itemCreator import Button, Object, Stars
import menu
from consts import *

pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('Sensei Rescuing')

bg_group_complete = pygame.sprite.Group()

cursor = load_image(r'objects\cursor-obj.png')
pygame.mouse.set_visible(False)

record = 1
zeroStars, oneStar, twoStars, threeStars = (r"objects\stars-zero-obj.png", r"objects\stars-one-obj.png",
                                            r"objects\stars-two-obj.png", r"objects\stars-three-obj.png")
stars = Stars(WIDTH // 2 - 236, HEIGHT // 2 - 55, 470, 78, zeroStars, oneStar, twoStars, threeStars)


class AnimatedGameComplete(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(bg_group_complete)
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
                for _ in range(10):
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

    def update(self):
        if self.cur_frame < 15 * 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if self.cur_frame >= 15 * 10:
            stars.draw(screen, record)
            for button in [repeat_btn, to_lvlmenu_btn]:
                button.check_hover(pygame.mouse.get_pos())
                button.draw(screen)


bg_img = load_image(r"backgrounds\game-complete-bg.png")
bg_tr = pygame.transform.scale(bg_img, (bg_img.get_width() * 2.5, bg_img.get_height() * 2.5))
game_complete_bg = AnimatedGameComplete(bg_tr, 16, 1, WIDTH // 2 - 265, HEIGHT // 2 - 180)

repeat_btn = Button(WIDTH // 2 + 172, HEIGHT // 2 - 65, 94, 104, r"buttons\default-repeat-btn.png", r"buttons\hover-repeat-btn.png",
                r"buttons\press-repeat-btn.png", r"data\sounds\menu-button-sound.mp3")
to_lvlmenu_btn = Button(WIDTH // 2 - 265, HEIGHT // 2 - 65, 94, 104, r"buttons\default-tolvlmenu-btn.png",
                 r"buttons\hover-tolvlmenu-btn.png",
                 r"buttons\press-tolvlmenu-btn.png", r"data\sounds\menu-button-sound.mp3")

field = Object(WIDTH - 1016, HEIGHT - 696, 1008, 688, r"objects\windows-field-obj.png")


def game_complete():
    pygame.mixer.music.load(r"data\sounds\game-complete-sound.mp3")
    pygame.mixer.music.play(1)

    running = True
    fps = 60
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                menu.levels_menu()

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event)
                button.handle_event(event)

        field.draw(screen)

        game_complete_bg.update()
        clock.tick(fps)
        bg_group_complete.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


game_complete()
