import pygame
import windows
import consts
import starsRecorder
import fileManager
import spriteGroups
from processHelper import load_image
from boss import AnimatedHealthBar
from hero import AnimatedHeroHealth
from itemAnimator import AnimatedHero
from itemCreator import Object, Button


# game and menu changers
def fullscreenChanger(fullscreen, ft=False):
    fileManager.fullscreenExport(windows.fullscreen)
    if fullscreen:
        if not ft:
            windows.width, windows.height = windows.fullsize
            windows.screen = pygame.display.set_mode(windows.fullsize, pygame.FULLSCREEN)
        consts.menu_bg = pygame.transform.scale(consts.img_fs, (consts.img_fs.get_width(), consts.img_fs.get_height()))
        consts.pause_field = Object(windows.otstupx + 8, 8, windows.width - windows.otstupx * 2 - 16, 1064,
                                    r"objects\without text\pause-window-obj.png")
        consts.game_state_field = Object(windows.otstupx + 8, windows.height - 1072,
                                         windows.width - windows.otstupx * 2 - 16, 1064,
                                         r"objects\without text\games-window-obj.png")
    else:
        if not ft:
            windows.width, windows.height = windows.size
            windows.screen = pygame.display.set_mode(windows.size)
        consts.menu_bg = pygame.transform.scale(consts.img, (consts.img.get_width() * 2, consts.img.get_height() * 2))
        consts.pause_field = Object(windows.width - 1016, windows.height - 696, 1008, 688,
                                    r"objects\without text\pause-window-obj.png")
        consts.game_state_field = Object(windows.width - 1016, windows.height - 696, 1008, 688,
                                         r"objects\without text\games-window-obj.png")


# game changers
def pauseButtonChanger():
    if not windows.fullscreen:
        pause_btn = Button(windows.width - 54, 6, 46, 48,
                           fr"buttons\without text\default-pause-btn.png",
                           fr"buttons\without text\hover-pause-btn.png",
                           fr"buttons\without text\press-pause-btn.png",
                           r"data\sounds\menu-button-sound.mp3")
    else:
        pause_btn = Button(windows.width - windows.otstupx - 54 * windows.k,
                           6 * windows.k, 46 * windows.k, 48 * windows.k,
                           fr"buttons\without text\default-pause-fs-btn.png",
                           fr"buttons\without text\hover-pause-fs-btn.png",
                           fr"buttons\without text\press-pause-fs-btn.png",
                           r"data\sounds\menu-button-sound.mp3")
    return pause_btn


def heroHeartsChanger():
    spriteGroups.hero_health.empty()
    if not windows.fullscreen:
        img_tmp = load_image(r"objects\animated\hearts-obj.png")
        heroHealth = AnimatedHeroHealth(img_tmp, 5, 1,
                                        7, 11)
    else:
        img_tmp = load_image(r"objects\animated\hearts-obj.png")
        tr_tmp = pygame.transform.scale(img_tmp,
                                        (img_tmp.get_width() * windows.k, img_tmp.get_height() * windows.k))
        heroHealth = AnimatedHeroHealth(tr_tmp, 5, 1,
                                        windows.otstupx + 7 * windows.k, 11 * windows.k)
    return heroHealth


def healthBossBarChanger():
    spriteGroups.health_bar.empty()
    if not windows.fullscreen:
        img_tmp = load_image(r"objects\animated\boss-health-bar-obj.png")
        tr_tmp = pygame.transform.scale(img_tmp,
                                        (img_tmp.get_width() * 1.5, img_tmp.get_height() * 1.5))
        healthBossBar = AnimatedHealthBar(tr_tmp, 52, 1,
                                          windows.width // 2 - 18720 * 1.5 / 52 / 2, 18)
    else:
        img_tmp = load_image(r"objects\animated\boss-health-bar-obj.png")
        tr_tmp = pygame.transform.scale(img_tmp,
                                        (img_tmp.get_width() * 2, img_tmp.get_height() * 2))
        healthBossBar = AnimatedHealthBar(tr_tmp, 52, 1,
                                          windows.width // 2 - 18720 * 2 / 52 / 2, 18 * windows.k)
    return healthBossBar


# menu changers
def volumeChanger(event, music_slider_btn, music_slider_obj, sound_slider_btn, sound_slider_obj):
    if consts.isSliderMusic:
        xM = music_slider_btn.rect[0]
        if (music_slider_obj.x + music_slider_obj.width / 30.2 < event.pos[0] < music_slider_obj.x +
                music_slider_obj.width - (music_slider_obj.width / 30.2)):
            x_cube_M = event.pos[0] - xM
        else:
            x_cube_M = music_slider_btn.width // 2
        music_slider_btn.rect = music_slider_btn.rect.move(x_cube_M - music_slider_btn.width // 2, 0)
        consts.wM = round((music_slider_btn.rect[0] - music_slider_obj.x) / music_slider_obj.width, 3)
        if consts.wM < 0.0:
            consts.wM = 0.0
        pygame.mixer.music.set_volume(consts.wM)
    elif consts.isSliderSound:
        xS = sound_slider_btn.rect[0]
        if (sound_slider_obj.x + sound_slider_obj.width / 30.2 < event.pos[0] < sound_slider_obj.x
                + sound_slider_obj.width - (sound_slider_obj.width / 30.2)):
            x_cube_S = event.pos[0] - xS
        else:
            x_cube_S = sound_slider_btn.width // 2
        sound_slider_btn.rect = sound_slider_btn.rect.move(x_cube_S - sound_slider_btn.width // 2, 0)
        consts.wS = round((sound_slider_btn.rect[0] - sound_slider_obj.x) / sound_slider_obj.width, 3)
        if consts.wS < 0.0:
            consts.wS = 0.0
        consts.volS = consts.wS
    fileManager.volumeExport(consts.wM, consts.wS)


def starsChanger(whatLevel, time):
    if whatLevel == 1:
        if 0 <= time <= 30:
            return 3
        elif 30 < time <= 40:
            return 2
        elif 40 < time <= 50:
            return 1
        elif time > 50:
            return 0
    if whatLevel == 2:
        if 0 <= time <= 120:
            return 3
        elif 120 < time <= 135:
            return 2
        elif 135 < time <= 150:
            return 1
        elif time > 150:
            return 0
    if whatLevel == 3:
        if 0 <= time <= 200:
            return 3
        elif 200 < time <= 225:
            return 2
        elif 225 < time <= 250:
            return 1
        elif time > 250:
            return 0


def timeChanger(whatLevel, ButtonsFont, w, h, screen):
    time = starsRecorder.get_seconds(whatLevel)
    time_sorted = f"{time // 60:02}:{time % 60:02}"
    if whatLevel == 1:
        levelTime = ButtonsFont.render(time_sorted, True, "#ffffff")
        levelTimeRect = levelTime.get_rect(center=(w + 186 // 2, h + 80))
        return screen.blit(levelTime, levelTimeRect)
    if whatLevel == 2:
        levelTime = ButtonsFont.render(time_sorted, True, "#ffffff")
        levelTimeRect = levelTime.get_rect(center=(w + 186 // 2, h + 80))
        return screen.blit(levelTime, levelTimeRect)
    if whatLevel == 3:
        levelTime = ButtonsFont.render(time_sorted, True, "#ffffff")
        levelTimeRect = levelTime.get_rect(center=(w + 186 // 2, h + 80))
        return screen.blit(levelTime, levelTimeRect)


def heroOnScreenChanger(hero, title, hero_field):
    current_hero = None
    if hero == 1:
        spriteGroups.animatedHero.empty()
        heroWai = AnimatedHero(load_image(r"objects\animated\hero-wai-obj.png"), 1, 8,
                               hero_field.x + hero_field.width // 2 - 116 // 2,
                               title.y + 188)
        current_hero = heroWai
    elif hero == 2:
        spriteGroups.animatedHero.empty()
        heroTheStrongest = AnimatedHero(load_image(r"objects\animated\hero-the-strongest-obj.png"), 1, 8,
                                        hero_field.x + hero_field.width // 2 - 104 // 2,
                                        title.y + 188)
        current_hero = heroTheStrongest
    return current_hero
