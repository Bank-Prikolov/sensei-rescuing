import pygame
import consts
import random


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
    pygame.mixer.music.load(r"data\sounds\boss-theme-sound.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(consts.wM)


def game_over_sound(ln):
    pygame.mixer.music.load(r"data\sounds\game-over-sound.mp3")
    pygame.mixer.music.play(1)


def game_complete_sound(ln):
    pygame.mixer.music.load(r"data\sounds\game-complete-sound.mp3")
    pygame.mixer.music.play(1)


def skala_sound():
    skalaSound = pygame.mixer.Sound(r"data\sounds\skala-sound.mp3")
    skalaSound.play()


def typing_sound():
    pygame.mixer.music.load(r"data\sounds\start-screen-sound.mp3")
    pygame.mixer.music.set_volume(consts.wS)
    pygame.mixer.music.play(-1)


def hit_sound():
    hit = pygame.mixer.Sound(r"data\sounds\hit-sound.mp3")
    hit.play()


def boss_take_hit():
    sounds = [pygame.mixer.Sound(r"data\sounds\pamagiti-sound.mp3"), pygame.mixer.Sound(r"data\sounds\oioioi-sound.mp3"),
              pygame.mixer.Sound(r"data\sounds\ya-cho-to-ne-ponyal-sound.mp3")]
    randomSound = sounds[random.randint(0, 2)]
    randomSound.play()


def boss_next_attack():
    sounds = [pygame.mixer.Sound(r"data\sounds\pamagiti-sound.mp3"), pygame.mixer.Sound(r"data\sounds\oioioi-sound.mp3"),
              pygame.mixer.Sound(r"data\sounds\ya-cho-to-ne-ponyal-sound.mp3")]
    randomSound = sounds[random.randint(0, 2)]
    randomSound.play()


def stop_playback():
    pygame.mixer.music.stop()


def volume_zero():
    pygame.mixer.music.set_volume(0)


def volume_on():
    pygame.mixer.music.set_volume(consts.wS)
