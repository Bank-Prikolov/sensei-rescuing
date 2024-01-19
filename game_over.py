import pygame
import sys
from load_image import load_image
from itemCreator import Button, Object
import game
import menu

pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('Sensei Rescuing')

bg_group_over = pygame.sprite.Group()

cursor = load_image(r'objects\cursor-obj.png')
pygame.mouse.set_visible(False)


class AnimatedGameOver(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(bg_group_over)
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
        if self.cur_frame < 13 * 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if self.cur_frame >= 13 * 10:
            for button in [repeat_btn, to_lvlmenu_btn]:
                button.check_hover(pygame.mouse.get_pos())
                button.draw(screen)


bg_img = load_image(r"backgrounds\game-over-bg.png")
bg_tr = pygame.transform.scale(bg_img, (bg_img.get_width() * 2.5, bg_img.get_height() * 2.5))
game_over_bg = AnimatedGameOver(bg_tr, 14, 1, WIDTH // 2 - 640, HEIGHT // 2 - 180)

repeat_btn = Button(WIDTH // 2 + 57, HEIGHT // 2 - 55, 94, 104, r"buttons\default-repeat-btn.png", r"buttons\hover-repeat-btn.png",
                r"buttons\press-repeat-btn.png", r"data\sounds\menu-button-sound.mp3")
to_lvlmenu_btn = Button(WIDTH // 2 - 94 - 48, HEIGHT // 2 - 55, 94, 104, r"buttons\default-tolvlmenu-btn.png",
                 r"buttons\hover-tolvlmenu-btn.png",
                 r"buttons\press-tolvlmenu-btn.png", r"data\sounds\menu-button-sound.mp3")

field = Object(WIDTH - 1016, HEIGHT - 696, 1008, 688, r"objects\windows-field-obj.png")


def game_over():
    pygame.mixer.music.load(r"data\sounds\game-over-sound.mp3")
    pygame.mixer.music.play(1)

    running = True
    fps = 60
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                game.game_def(menu.lvlNow)

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event)

        field.draw(screen)

        game_over_bg.update()
        clock.tick(fps)
        bg_group_over.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


# game_over()
