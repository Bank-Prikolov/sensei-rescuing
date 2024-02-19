import pygame
import menu
import windows
import consts
import starsRecorder
import spriteGroups
from processHelper import load_image
from itemCreator import Button
from itemAnimator import AnimatedIntro, AnimatedObject


def start_screen():
    starsRecorder.firstTime()

    skalaSound = pygame.mixer.Sound(r"data\sounds\skala-sound.mp3")

    if consts.languageNow == 'rus':
        img_start = load_image(r"objects\animated\start-screen-rus-obj.png")
        start_screen_obj = AnimatedObject(img_start, 42, 1, windows.width / 2 - 26880 / 42 / 2,
                                          windows.height // 2 - 145)
    else:
        img_start = load_image(r"objects\animated\start-screen-eng-obj.png")
        start_screen_obj = AnimatedObject(img_start, 45, 1, windows.width / 2 - 28800 / 45 / 2,
                                          windows.height // 2 - 145)

    img_intro = load_image(r"objects\animated\intro-obj.png")
    tr_intro = pygame.transform.scale(img_intro, (img_intro.get_width() * 2, img_intro.get_height() * 2))
    intro_obj = AnimatedIntro(tr_intro, 112, 1, windows.width // 2 - 512,
                             windows.height // 2 - 145)

    da_btn = Button(windows.width // 2 - 50 - 67 if consts.languageNow == 'rus' else windows.width // 2 - 50 - 92,
                    windows.height // 2 - 10, 67 if consts.languageNow == 'rus' else 92, 60,
                    fr"buttons\{consts.languageNow}\default-da-btn.png",
                    fr"buttons\{consts.languageNow}\hover-da-btn.png",
                    fr"buttons\{consts.languageNow}\hover-da-btn.png", r"data\sounds\da-sound.mp3")
    net_btn = Button(windows.width // 2 + 50, windows.height // 2 - 10, 86 if consts.languageNow == 'rus' else 60, 58,
                     fr"buttons\{consts.languageNow}\default-net-btn.png",
                     fr"buttons\without text\hover-net-btn.png",
                     fr"buttons\without text\hover-net-btn.png", r"data\sounds\hi-hi-hi-ha-sound.mp3")

    intro_finish = False
    running = True
    while running:

        windows.screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                skalaSound.play()

            if event.type == pygame.USEREVENT and event.button == da_btn:
                consts.fps = 60
                spriteGroups.animatedObjects.empty()
                menu.main_menu()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and intro_finish:
                consts.fps = 300

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and intro_finish:
                consts.fps = 60

            for button in [da_btn, net_btn]:
                button.handle_event(event, consts.wS)

        intro_obj.update()
        spriteGroups.introGroup.draw(windows.screen)
        if intro_obj.cur_frame >= 111 * 3:
            spriteGroups.introGroup.empty()
            intro_finish = True

        if intro_finish:
            start_screen_obj.update_start_screen(windows.screen, da_btn, net_btn, consts.languageNow)
            spriteGroups.animatedObjects.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
