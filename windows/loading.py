import pygame
from managing import sounds_managing
import spriteGroups
from config import consts
import menu
import threading
from windows.items.item_creating import Object
from windows.items.item_animation import AnimatedDots
from misc.specfunctions import load_image, terminate


def loading_items():
    consts.WaiHleb = load_image(fr"cutscenes\hleb-greeting\hleb-greeting-wai-dialogue.png")
    consts.StrongestHleb = load_image(fr"cutscenes\hleb-greeting\hleb-greeting-thest-dialogue.png")
    consts.WaiBossGreeting = load_image(fr"cutscenes\boss-greeting\boss-greeting-wai-dialogue.png")
    consts.StrongestBossGreeting = load_image(fr"cutscenes\boss-greeting\boss-greeting-thest-dialogue.png")
    consts.WaiBossEnding = load_image(fr"cutscenes\boss-lose\boss-lose-wai-dialogue.png")
    consts.StrongestBossEnding = load_image(fr"cutscenes\boss-lose\boss-lose-thest-dialogue.png")
    consts.WaiHleb_FS = pygame.transform.scale(consts.WaiHleb, (consts.WaiHleb.get_width() * 1.5,
                                                                consts.WaiHleb.get_height() * 1.5))
    consts.StrongestHleb_FS = pygame.transform.scale(consts.StrongestHleb, (consts.StrongestHleb.get_width() * 1.5,
                                                                            consts.StrongestHleb.get_height() * 1.5))
    consts.WaiBossGreeting_FS = pygame.transform.scale(consts.WaiBossGreeting,
                                                       (consts.WaiBossGreeting.get_width() * 1.5,
                                                        consts.WaiBossGreeting.get_height() * 1.5))
    consts.StrongestBossGreeting_FS = pygame.transform.scale(consts.StrongestBossGreeting,
                                                             (consts.StrongestBossGreeting.get_width() * 1.5,
                                                              consts.StrongestBossGreeting.get_height() * 1.5))
    consts.WaiBossEnding_FS = pygame.transform.scale(consts.WaiBossEnding, (consts.WaiBossEnding.get_width() * 1.5,
                                                                            consts.WaiBossEnding.get_height() * 1.5))
    consts.StrongestBossEnding_FS = pygame.transform.scale(consts.StrongestBossEnding,
                                                           (consts.StrongestBossEnding.get_width() * 1.5,
                                                            consts.StrongestBossEnding.get_height() * 1.5))


def loading_menu():
    loadingItems = threading.Thread(target=loading_items)
    loadingItems.start()

    soundManager.menu_theme()

    field = Object(windows.width // 2 - 350 // 2, windows.height // 2 - 170 // 2, 350, 170,
                   fr"objects\without text\loading-field-obj.png")
    title = Object(
        field.x + field.width // 2 - 286 / 2 if consts.languageNow == 'rus' else field.x + field.width // 2 - 254 / 2,
        field.y + 30, 286 if consts.languageNow == 'rus' else 254, 58,
        fr"objects\{consts.languageNow}\loading-title-obj.png")
    dots = AnimatedDots(load_image(r"objects\animated\dots-obj.png"), 4, 1, field.x + field.width // 2 - 544 / 4 / 2,
                        field.y + field.height - 40 - 30)

    running = True
    while running:

        windows.screen.blit(consts.menu_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if not loadingItems.is_alive():
            menu.main_menu()

        field.draw(windows.screen)
        title.draw(windows.screen)
        dots.update()
        spriteGroups.animatedDots.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
