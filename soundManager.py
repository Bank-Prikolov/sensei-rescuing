import pygame
import consts
import random


def menu_theme():
    if consts.playingMenuMusic:
        pygame.mixer.music.load(r"data\sounds\menu-theme-sound.mp3")
        pygame.mixer.music.set_volume(consts.wM)
        pygame.mixer.music.play(-1)
        consts.playingMenuMusic = False


def game_theme():
    pygame.mixer.music.load(r"data\sounds\game-theme-sound.mp3")
    pygame.mixer.music.set_volume(consts.wM)
    pygame.mixer.music.play(-1)


def boss_theme():
    pygame.mixer.music.load(r"data\sounds\boss-theme-sound.mp3")
    pygame.mixer.music.set_volume(consts.wM)
    pygame.mixer.music.play(-1)


def typing_theme():
    pygame.mixer.music.load(r"data\sounds\start-screen-sound.mp3")
    pygame.mixer.music.set_volume(consts.wS)
    pygame.mixer.music.play(-1)


def game_over_theme(ln):
    if ln == 'rus':
        pygame.mixer.music.load(r"data\sounds\game-over-rus-sound.mp3")
    elif ln == 'eng':
        pygame.mixer.music.load(r"data\sounds\game-over-eng-sound.mp3")
    pygame.mixer.music.set_volume(consts.wM)
    pygame.mixer.music.play(1)


def game_complete_theme():
    pygame.mixer.music.load(r"data\sounds\game-complete-sound.mp3")
    pygame.mixer.music.set_volume(consts.wM)
    pygame.mixer.music.play(1)


def skala_sound():
    skalaSound = pygame.mixer.Sound(r"data\sounds\skala-sound.mp3")
    skalaSound.set_volume(consts.volS)
    skalaSound.play()


def hero_take_hit_sound():
    heroHit = pygame.mixer.Sound(r"data\sounds\hero-hit-sound.mp3")
    heroHit.set_volume(consts.volS)
    heroHit.play()


def slonik_take_hit_sound():
    slonikHit = pygame.mixer.Sound(r"data\sounds\slonik-hit-sound.mp3")
    slonikHit.set_volume(consts.volS)
    slonikHit.play()


def hero_lose_boss_sound():
    bossWin = pygame.mixer.Sound(r"data\sounds\boss-win-sound.mp3")
    bossWin.set_volume(consts.volS)
    bossWin.play()


def boss_take_hit_sound():
    sounds = [pygame.mixer.Sound(r"data\sounds\pamagiti-sound.mp3"),
              pygame.mixer.Sound(r"data\sounds\oioioi-sound.mp3"),
              pygame.mixer.Sound(r"data\sounds\ya-cho-to-ne-ponyal-sound.mp3")]
    randomSound = sounds[random.randint(0, 2)]
    randomSound.set_volume(consts.volS)
    randomSound.play()


def boss_next_attack_sound():
    sounds = [pygame.mixer.Sound(r"data\sounds\hvatit_nit-sound.mp3"),
              pygame.mixer.Sound(r"data\sounds\nadayu-po-jope-sound.mp3"),
              pygame.mixer.Sound(r"data\sounds\pozhaluysta-otchislyaytes-sound.mp3"),
              pygame.mixer.Sound(r"data\sounds\ya-vas-otchislyu-sound.mp3"),
              pygame.mixer.Sound(r"data\sounds\ya-vas-ubiu-sound.mp3")]
    randomSound = sounds[random.randint(0, 4)]
    randomSound.set_volume(consts.volS)
    randomSound.play()


def star_sound():
    starSound = pygame.mixer.Sound(r"data\sounds\star-sound.mp3")
    # starSound.set_volume(consts.volS)
    # starSound.play()


def talking_sound():
    talkingSound = pygame.mixer.Sound(r"data\sounds\talking-sound.mp3")
    # talkingSound.set_volume(0.2)
    # talkingSound.play()


def boss_lose_sound():
    bossLoseSound = pygame.mixer.Sound(r"data\sounds\boss-lose-sound.mp3")
    # bossLoseSound.set_volume(consts.wM)
    # bossLoseSound.play()


def door_open_sound():
    doorSound = pygame.mixer.Sound(r"data\sounds\door-open-sound.mp3")
    # doorSound.set_volume(consts.volS)
    # doorSound.play(0)


def teleport_sound():
    teleportSound = pygame.mixer.Sound(r"data\sounds\teleport-sound.mp3")
    # teleportSound.set_volume(consts.volS)
    # teleportSound.play(0)


def get_key_sound():
    getKeySound = pygame.mixer.Sound(r"data\sounds\get-key-sound.mp3")
    # getKeySound.set_volume(consts.volS)
    # getKeySound.play()


def tp_activated():
    tpActivated = pygame.mixer.Sound(r"data\sounds\tp-activated-sound.mp3")
    tpActivated.set_volume(consts.volS)
    tpActivated.play()


def stop_playback():
    pygame.mixer.music.stop()


def volume_zero():
    pygame.mixer.music.set_volume(0)


def volume_on():
    pygame.mixer.music.set_volume(consts.wS)
