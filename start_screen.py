import pygame
from load_image import load_image
from itemCreator import Button
from itemChecker import cursorMenuChecker, languageImportChecker
import menu
import windows

pygame.init()

clock = pygame.time.Clock()
pygame.display.set_caption('Sensei Rescuing')

bg_group = pygame.sprite.Group()
bg_group_intro = pygame.sprite.Group()

cursor = load_image(r'objects\without text\cursor-obj.png')
pygame.mouse.set_visible(False)

languageNow = languageImportChecker()


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
                for _ in range(10):
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

    def update(self, screen, da_btn, net_btn):
        if self.cur_frame == 1:
            pygame.mixer.music.load(r"data\sounds\start-screen-sound.mp3")
            pygame.mixer.music.play(-1)

        if self.cur_frame < 41 * 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if 18 * 10 < self.cur_frame < 26 * 10:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(1)

        if self.cur_frame >= 40 * 10:
            pygame.mixer.music.stop()
            da_btn.check_hover(pygame.mouse.get_pos())
            da_btn.draw(screen)
            net_btn.check_hover(pygame.mouse.get_pos())
            net_btn.draw(screen)


def start_screen():
    if windows.fullscreen:
        size = WIDTH, HEIGHT = 1920, 1080
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        size = WIDTH, HEIGHT = 1024, 704
        screen = pygame.display.set_mode(size)

    skalaSound = pygame.mixer.Sound(r"data\sounds\skala-sound.mp3")

    bg_img = load_image(r"backgrounds\start-screen-bg.png")
    start_bg = AnimatedStartScreen(bg_img, 46, 1, WIDTH // 2 - 320,
                                   HEIGHT // 2 - 145)

    bg_img_intro = load_image(r"backgrounds\intro-bg.png")
    bg_tr = pygame.transform.scale(bg_img_intro, (bg_img_intro.get_width() * 2, bg_img_intro.get_height() * 2))
    intro_bg = AnimatedIntro(bg_tr, 31, 1, WIDTH // 2 - 512,
                             HEIGHT // 2 - 145)

    da_btn = Button(WIDTH // 2 - 165, HEIGHT // 2 - 10, 67, 60, fr"buttons\{languageNow}\default-da-btn.png",
                    fr"buttons\{languageNow}\hover-da-btn.png",
                    fr"buttons\{languageNow}\hover-da-btn.png", r"data\sounds\da-sound.mp3")
    net_btn = Button(WIDTH // 2 + 40, HEIGHT // 2 - 10, 86, 58, fr"buttons\{languageNow}\default-net-btn.png",
                     fr"buttons\without text\hover-net-btn.png",
                     fr"buttons\without text\hover-net-btn.png", r"data\sounds\hi-hi-hi-ha-sound.mp3")

    intro_finish = False
    running = True
    fps = 60
    while running:

        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                skalaSound.play()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                skalaSound.play()

            if event.type == pygame.USEREVENT and event.button == da_btn:
                menu.main_menu()

            for button in [da_btn, net_btn]:
                button.handle_event(event)

        intro_bg.update()
        bg_group_intro.draw(screen)
        if intro_bg.cur_frame >= 30 * 8:
            bg_group_intro.empty()
            intro_finish = True

        if intro_finish:
            start_bg.update(screen, da_btn, net_btn)
            bg_group.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        cursorMenuChecker(x_c, y_c, cursor, screen)

        clock.tick(fps)
        pygame.display.flip()


start_screen()
