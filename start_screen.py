import pygame
import menu
import windows
import consts
import starsRecorder
from processHelper import load_image
from itemCreator import Button
from itemAnimator import AnimatedIntro, AnimatedStartScreen


def start_screen():
    starsRecorder.firstTime()

    skalaSound = pygame.mixer.Sound(r"data\sounds\skala-sound.mp3")

    bg_img_start = load_image(r"objects\animated\start-screen-obj.png")
    start_bg = AnimatedStartScreen(bg_img_start, 46, 1, windows.width // 2 - 320,
                                   windows.height // 2 - 145)

    bg_img_intro = load_image(r"objects\animated\intro-obj.png")
    bg_tr = pygame.transform.scale(bg_img_intro, (bg_img_intro.get_width() * 2, bg_img_intro.get_height() * 2))
    intro_bg = AnimatedIntro(bg_tr, 112, 1, windows.width // 2 - 512,
                             windows.height // 2 - 145)

    da_btn = Button(windows.width // 2 - 165, windows.height // 2 - 10, 67, 60,
                    fr"buttons\{consts.languageNow}\default-da-btn.png",
                    fr"buttons\{consts.languageNow}\hover-da-btn.png",
                    fr"buttons\{consts.languageNow}\hover-da-btn.png", r"data\sounds\da-sound.mp3")
    net_btn = Button(windows.width // 2 + 40, windows.height // 2 - 10, 86, 58,
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
                menu.main_menu()

            for button in [da_btn, net_btn]:
                button.handle_event(event)

        intro_bg.update()
        consts.bg_group_intro.draw(windows.screen)
        if intro_bg.cur_frame >= 111 * 3:
            consts.bg_group_intro.empty()
            intro_finish = True

        if intro_finish:
            start_bg.update(windows.screen, da_btn, net_btn)
            consts.bg_group_start_screen.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
