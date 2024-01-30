import pygame
import sys
from load_image import load_image
from itemCreator import Button, Object
from itemChecker import fullscreenChecker, cursorChecker
import game
import menu
import windows

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

    def update(self, screen, repeat_btn, to_lvlmenu_btn):
        if self.cur_frame < 13 * 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if self.cur_frame >= 13 * 10:
            for butt in [repeat_btn, to_lvlmenu_btn]:
                butt.check_hover(pygame.mouse.get_pos())
                butt.draw(screen)


def game_over(whatFrame=0):
    if windows.fullscreen:
        size = WIDTH, HEIGHT = 1920, 1080
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        size = WIDTH, HEIGHT = 1024, 704
        screen = pygame.display.set_mode(size)

    pygame.mixer.music.load(r"data\sounds\game-over-sound.mp3")
    pygame.mixer.music.play(1)

    bg_img = load_image(r"backgrounds\game-over-bg.png")
    bg_tr = pygame.transform.scale(bg_img, (bg_img.get_width() * 2.5, bg_img.get_height() * 2.5))
    game_over_bg = AnimatedGameOver(bg_tr, 14, 1, WIDTH // 2 - 640, HEIGHT // 2 - 180)

    repeat_btn = Button(WIDTH // 2 + 57, HEIGHT // 2 - 55, 94, 104, r"buttons\default-repeat-btn.png",
                        r"buttons\hover-repeat-btn.png",
                        r"buttons\press-repeat-btn.png", r"data\sounds\menu-button-sound.mp3")
    to_lvlmenu_btn = Button(WIDTH // 2 - 94 - 48, HEIGHT // 2 - 55, 94, 104, r"buttons\default-tolvlmenu-btn.png",
                            r"buttons\hover-tolvlmenu-btn.png",
                            r"buttons\press-tolvlmenu-btn.png", r"data\sounds\menu-button-sound.mp3")

    if not windows.fullscreen:
        field = Object(WIDTH - WIDTH, HEIGHT - HEIGHT, 1024, 704, r"objects\windows-field-obj.png")
    else:
        field = Object(windows.otstupx, HEIGHT - HEIGHT, WIDTH - 2 * windows.otstupx, 1080,
                       r"objects\windows-field-obj.png")

    running = True
    fps = 60
    errorSound = pygame.mixer.Sound(r"data\sounds\error-sound.mp3")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fullscreenChecker(windows.fullscreen)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if game_over_bg.cur_frame >= 130:
                    if windows.fullscreen:
                        running = False
                        bg_group_over.empty()
                        windows.fullscreen = 0
                        game_over(1)
                    else:
                        running = False
                        bg_group_over.empty()
                        windows.fullscreen = 1
                        game_over(1)
                else:
                    pygame.mixer.Sound.set_volume(errorSound, menu.volS)
                    errorSound.play()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                running = False
                bg_group_over.empty()
                menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                running = False
                bg_group_over.empty()
                game.game_def(menu.lvlNow)

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event, menu.volS)

        field.draw(screen)
        if whatFrame:
            game_over_bg.cur_frame = 129
            pygame.mixer.music.stop()
        game_over_bg.update(screen, repeat_btn, to_lvlmenu_btn)
        clock.tick(fps)
        bg_group_over.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        cursorChecker(x_c, y_c, cursor, screen)

        pygame.display.flip()

# game_over()
