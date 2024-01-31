import pygame
import windows


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


def fullscreenExportChecker(StateFullscreen):
    checkStateFullscreenRewrite = open(r"data/savings/fullscreen-settings.txt", "w")
    checkStateFullscreenRewrite.writelines(str(StateFullscreen))
    checkStateFullscreenRewrite.close()


def fullscreenWindowsChecker(fullscreen):
    if fullscreen:
        size = WIDTH, HEIGHT = 1920, 1080
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        size = WIDTH, HEIGHT = 1024, 704
        screen = pygame.display.set_mode(size)
    return screen, WIDTH, HEIGHT


def languageImportChecker():
    checkWhatLanguage = open(r"data/savings/language-settings.txt", "r")
    whatLanguage = list(map(lambda x: str(x.rstrip('\n')), checkWhatLanguage))
    languageNow = whatLanguage[0]
    return languageNow
