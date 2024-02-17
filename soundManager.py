import pygame
import consts


def menu_theme():
    if consts.firstTime:
        pygame.mixer.music.load(r"data\sounds\menu-theme-sound.mp3")
        pygame.mixer.music.play(-1)
        consts.firstTime = False
        pygame.mixer.music.set_volume(consts.wM)


def game_theme():
    pygame.mixer.music.load(r"data\sounds\game-theme-sound.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(consts.wM)


def boss_theme():
    pass


def game_over_sound():
    pygame.mixer.music.load(r"data\sounds\game-over-sound.mp3")
    pygame.mixer.music.play(1)


def game_complete_sound():
    pygame.mixer.music.load(r"data\sounds\game-complete-sound.mp3")
    pygame.mixer.music.play(1)
