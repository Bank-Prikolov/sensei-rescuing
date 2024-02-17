import pygame

bg_group_start_screen = pygame.sprite.Group()
bg_group_intro = pygame.sprite.Group()
bg_group_over = pygame.sprite.Group()
bg_group_complete = pygame.sprite.Group()


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
                for _ in range(3):
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

    def update(self):
        if self.cur_frame < 111 * 3:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


class AnimatedStartScreen(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(bg_group_start_screen)
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

    def update(self, screen, record, stars, repeat_btn, to_lvlmenu_btn, levelTime, levelTimeRect):
        if self.cur_frame < 15 * 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if self.cur_frame >= 15 * 10:
            stars.draw(screen, record)
            screen.blit(levelTime, levelTimeRect)
            for butt in [repeat_btn, to_lvlmenu_btn]:
                butt.check_hover(pygame.mouse.get_pos())
                butt.draw(screen)
