import pygame
import menu
import windows
import consts
from load_image import load_image
from itemCreator import Button
from itemAnimator import AnimatedIntro, AnimatedStartScreen
from itemChecker import cursorMenuChecker, languageImportChecker, fullscreenWindowsChecker

languageNow = languageImportChecker()


def start_screen():
    screen, WIDTH, HEIGHT = fullscreenWindowsChecker(windows.fullscreen)

    skalaSound = pygame.mixer.Sound(r"data\sounds\skala-sound.mp3")

    bg_img_start = load_image(r"backgrounds\start-screen-bg.png")
    start_bg = AnimatedStartScreen(bg_img_start, 46, 1, WIDTH // 2 - 320,
                                   HEIGHT // 2 - 145)

    bg_img_intro = load_image(r"backgrounds\intro-bg.png")
    bg_tr = pygame.transform.scale(bg_img_intro, (bg_img_intro.get_width() * 2, bg_img_intro.get_height() * 2))
    intro_bg = AnimatedIntro(bg_tr, 112, 1, WIDTH // 2 - 512,
                             HEIGHT // 2 - 145)

    da_btn = Button(WIDTH // 2 - 165, HEIGHT // 2 - 10, 67, 60, fr"buttons\{languageNow}\default-da-btn.png",
                    fr"buttons\{languageNow}\hover-da-btn.png",
                    fr"buttons\{languageNow}\hover-da-btn.png", r"data\sounds\da-sound.mp3")
    net_btn = Button(WIDTH // 2 + 40, HEIGHT // 2 - 10, 86, 58, fr"buttons\{languageNow}\default-net-btn.png",
                     fr"buttons\without text\hover-net-btn.png",
                     fr"buttons\without text\hover-net-btn.png", r"data\sounds\hi-hi-hi-ha-sound.mp3")

    intro_finish = False
    running = True
    while running:

        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                skalaSound.play()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                skalaSound.play()

            if event.type == pygame.USEREVENT and event.button == da_btn:
                menu.main_menu()

            for button in [da_btn, net_btn]:
                button.handle_event(event)

        intro_bg.update()
        consts.bg_group_intro.draw(screen)
        if intro_bg.cur_frame >= 111 * 3:
            consts.bg_group_intro.empty()
            intro_finish = True

        if intro_finish:
            start_bg.update(screen, da_btn, net_btn)
            consts.bg_group_start_screen.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        cursorMenuChecker(x_c, y_c, consts.cursor, screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()


# start_screen()
