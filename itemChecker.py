import pygame
import windows
import starsRecorder


def cursorGameChecker(x_c, y_c, cursor, screen):
    if not windows.fullscreen:
        if 11 <= x_c <= 987 and 11 <= y_c <= 664:
            screen.blit(cursor, (x_c, y_c))
    else:
        if windows.otstupx <= x_c <= 1890 - windows.otstupx:
            screen.blit(cursor, (x_c, y_c))


def cursorMenuChecker(x_c, y_c, cursor, screen):
    if not windows.fullscreen:
        if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
            screen.blit(cursor, (x_c, y_c))
    else:
        screen.blit(cursor, (x_c, y_c))


def fullscreenWindowsChecker(fullscreen):
    if fullscreen:
        size = WIDTH, HEIGHT = 1920, 1080
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        size = WIDTH, HEIGHT = 1024, 704
        screen = pygame.display.set_mode(size)
    return screen, WIDTH, HEIGHT


def starsCountChecker(whatLevel, time):
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


def timeChecker(whatLevel, ButtonsFont, all_w, all_h, screen):
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
