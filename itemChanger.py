import pygame
import windows
import consts
import starsRecorder


def windowsFullscreenChanger(fullscreen):
    if fullscreen:
        windows.width, windows.height = windows.fullsize
        windows.screen = pygame.display.set_mode(windows.fullsize, pygame.FULLSCREEN)
        consts.menu_bg = pygame.transform.scale(consts.img_fs, (consts.img_fs.get_width(), consts.img_fs.get_height()))
    else:
        windows.width, windows.height = windows.size
        windows.screen = pygame.display.set_mode(windows.size)
        consts.menu_bg = pygame.transform.scale(consts.img, (consts.img.get_width() * 2, consts.img.get_height() * 2))


def starsChanger(whatLevel, time):
    if whatLevel == 1:
        if 0 < time <= 35:
            return 3
        elif 35 < time <= 40:
            return 2
        elif 40 < time <= 60:
            return 1
        elif time > 60:
            return 0
    if whatLevel == 2:
        if 0 < time <= 65:
            return 3
        elif 65 < time <= 70:
            return 2
        elif 70 < time <= 90:
            return 1
        elif time > 90:
            return 0
    if whatLevel == 3:
        if 0 < time <= 125:
            return 3
        elif 125 < time <= 130:
            return 2
        elif 130 < time <= 150:
            return 1
        elif time > 150:
            return 0


def timeChanger(whatLevel, ButtonsFont, all_w, all_h, screen):
    time = starsRecorder.get_seconds(whatLevel)
    time_sorted = f"{time // 60:02}:{time % 60:02}"
    if whatLevel == 1:
        levelTime = ButtonsFont.render(time_sorted, True, "#ffffff")
        levelTimeRect = levelTime.get_rect(center=(all_w - 79 + 186 // 2, all_h + 455))
        return screen.blit(levelTime, levelTimeRect)
    if whatLevel == 2:
        levelTime = ButtonsFont.render(time_sorted, True, "#ffffff")
        levelTimeRect = levelTime.get_rect(center=(all_w + 296 + 186 // 2, all_h + 455))
        return screen.blit(levelTime, levelTimeRect)
    if whatLevel == 3:
        levelTime = ButtonsFont.render(time_sorted, True, "#ffffff")
        levelTimeRect = levelTime.get_rect(center=(all_w + 673 + 186 // 2, all_h + 455))
        return screen.blit(levelTime, levelTimeRect)
