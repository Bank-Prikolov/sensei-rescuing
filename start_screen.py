import pygame
import menu
import windows
import consts
import starsRecorder
import spriteGroups
import soundManager
from processHelper import load_image
from itemChanger import fullscreenChanger
from itemCreator import Button, Object
from itemAnimator import AnimatedIntro, AnimatedTypedText


def start_screen():
    starsRecorder.firstTime()
    fullscreenChanger(windows.fullscreen, True)

    if consts.languageNow == 'rus':
        img_start = load_image(r"objects\animated\start-screen-rus-obj.png")
        start_screen_obj = AnimatedTypedText(img_start, 42, 1, windows.width / 2 - 26880 / 42 / 2,
                                             windows.height // 2 - 145)
        question_finish = 41 * 10
    else:
        img_start = load_image(r"objects\animated\start-screen-eng-obj.png")
        start_screen_obj = AnimatedTypedText(img_start, 45, 1, windows.width / 2 - 28800 / 45 / 2,
                                             windows.height // 2 - 145)
        question_finish = 44 * 10

    img_intro = load_image(r"objects\animated\intro-obj.png")
    tr_intro = pygame.transform.scale(img_intro, (img_intro.get_width() * 2, img_intro.get_height() * 2))
    intro_obj = AnimatedIntro(tr_intro, 112, 1, windows.width // 2 - 512,
                              windows.height // 2 - 145)

    da_btn = Button(windows.width // 2 - 50 - 92,
                    windows.height // 2 - 10, 92, 60,
                    fr"buttons\{consts.languageNow}\default-da-btn.png",
                    fr"buttons\{consts.languageNow}\hover-da-btn.png",
                    fr"buttons\{consts.languageNow}\hover-da-btn.png", r"data\sounds\da-sound.mp3")
    net_btn = Button(windows.width // 2 + 50, windows.height // 2 - 10, 92, 60,
                     fr"buttons\{consts.languageNow}\default-net-btn.png",
                     fr"buttons\without text\hover-net-btn.png",
                     fr"buttons\without text\hover-net-btn.png", r"data\sounds\hi-hi-hi-ha-sound.mp3")

    to_skip = Object(windows.width // 2 - 472 // 2, da_btn.y + da_btn.height + 100, 472, 38,
                     fr"objects\{consts.languageNow}\to-skip-obj.png")

    intro_finish = False
    wanna_skip = False
    time_wanna_skip = 0
    running = True
    while running:

        windows.screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                soundManager.skala_sound()

            if event.type == pygame.USEREVENT and event.button == da_btn:
                spriteGroups.animatedTypedText.empty()
                menu.main_menu()

            if event.type == pygame.KEYDOWN and intro_finish:
                wanna_skip = True

            if (event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and intro_finish):
                consts.fps = 300
                wanna_skip = False

            for button in [da_btn, net_btn]:
                button.handle_event(event, consts.wS)

        intro_obj.update()
        spriteGroups.animatedIntro.draw(windows.screen)
        if intro_obj.cur_frame >= 111 * 3:
            spriteGroups.animatedIntro.empty()
            intro_finish = True

        if intro_finish:
            start_screen_obj.update_start_screen(windows.screen, da_btn, net_btn, consts.languageNow)
            spriteGroups.animatedTypedText.draw(windows.screen)
            if wanna_skip:
                if time_wanna_skip >= 4800 or start_screen_obj.cur_frame == question_finish:
                    wanna_skip = False
                    time_wanna_skip = 0
                else:
                    to_skip.draw(windows.screen)
                    time_wanna_skip += 60

        if start_screen_obj.cur_frame == start_screen_obj.columns_number * 10 - 10:
            consts.fps = 60

        consts.clock.tick(consts.fps)
        pygame.display.flip()
