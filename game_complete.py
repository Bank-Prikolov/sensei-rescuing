import pygame
import sys
from load_image import load_image
from itemCreator import Button
import menu
from transition import transition
from consts import *

pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('Sensei Rescuing')

bg_group_complete = pygame.sprite.Group()

cursor = load_image(r'objects\cursor-obj.png')
pygame.mouse.set_visible(False)


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
            pygame.mixer.music.stop()
            repeat_btn.check_hover(pygame.mouse.get_pos())
            repeat_btn.draw(screen)
            to_lvlmenu_btn.check_hover(pygame.mouse.get_pos())
            to_lvlmenu_btn.draw(screen)


bg_img = load_image(r"backgrounds\game-complete-bg.png")
bg_tr = pygame.transform.scale(bg_img, (bg_img.get_width() * 2.5, bg_img.get_height() * 2.5))
game_complete_bg = AnimatedGameComplete(bg_tr, 16, 1, WIDTH // 2 - 640, HEIGHT // 2 - 180)

repeat_btn = Button(WIDTH // 2 + 50, HEIGHT // 2 - 30, 94, 104, r"buttons\default-repeat-btn.png", r"buttons\hover-repeat-btn.png",
                r"buttons\press-repeat-btn.png", r"data\sounds\menu-button-sound.mp3")
to_lvlmenu_btn = Button(WIDTH // 2 - 150, HEIGHT // 2 - 30, 94, 104, r"buttons\default-tolvlmenu-btn.png",
                 r"buttons\hover-tolvlmenu-btn.png",
                 r"buttons\press-tolvlmenu-btn.png", r"data\sounds\menu-button-sound.mp3")


def game_complete():
    pygame.mixer.music.load(r"data\sounds\start-screen-sound.mp3")
    pygame.mixer.music.play(-1)

    running = True
    fps = 60
    while running:

        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                transition()
                menu.levels_menu()

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event)
                button.handle_event(event)

        game_complete_bg.update()
        clock.tick(fps)
        bg_group_complete.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


# game_complete()
