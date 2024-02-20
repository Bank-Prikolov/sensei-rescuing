import pygame
import spriteGroups
import soundManager


class AnimatedObject(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(spriteGroups.animatedObjects)
        self.frames = []
        self.columns_number = columns
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

    def update_start_screen(self, screen, da_btn, net_btn, ln):
        if ln == 'rus':
            numFrame = 41
        else:
            numFrame = 44

        if self.cur_frame == 1:
            soundManager.typing_sound()

        if self.cur_frame < numFrame * 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if 18 * 10 < self.cur_frame < 26 * 10:
            soundManager.volume_zero()
        else:
            soundManager.volume_on()

        if self.cur_frame >= numFrame * 10:
            soundManager.stop_playback()
            da_btn.check_hover(pygame.mouse.get_pos())
            da_btn.draw(screen)
            net_btn.check_hover(pygame.mouse.get_pos())
            net_btn.draw(screen)

    def update_game_over(self, screen, repeat_btn, to_lvlmenu_btn, ln):
        if ln == 'rus':
            numFrames = 13
        else:
            numFrames = 9

        if self.cur_frame < numFrames * 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if self.cur_frame >= numFrames * 10:
            for butt in [repeat_btn, to_lvlmenu_btn]:
                butt.check_hover(pygame.mouse.get_pos())
                butt.draw(screen)

    def update_game_complete(self, screen, record, stars, repeat_btn, to_lvlmenu_btn, levelTime, levelTimeRect, ln):
        if ln == 'rus':
            numFrames = 15
        else:
            numFrames = 12
        if self.cur_frame < numFrames * 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if self.cur_frame >= numFrames * 10:
            stars.draw(screen, record)
            screen.blit(levelTime, levelTimeRect)
            for butt in [repeat_btn, to_lvlmenu_btn]:
                butt.check_hover(pygame.mouse.get_pos())
                butt.draw(screen)


class AnimatedIntro(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(spriteGroups.introGroup)
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
