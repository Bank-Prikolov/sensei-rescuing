import pygame
import windows
import consts
import menu
import levels_menu
from itemCreator import Object, Button
from processHelper import terminate, transition


def modeSelection():
    field = Object(windows.width // 2 - 714 / 2, windows.height // 2 - 430 // 2, 714, 430,
                   fr"objects\without text\mode-field-obj.png")

    campaign_btn = Button(field.x + field.width / 2 - 288 - 28, field.y + 27, 288, 312,
                          fr"buttons\without text\default-campaign-btn.png",
                          fr"buttons\without text\hover-campaign-btn.png",
                          fr"buttons\without text\press-campaign-btn.png", r"data\sounds\menu-button-sound.mp3")
    phpStorm_btn = Button(field.x + field.width / 2 + 28, field.y + 27, 288, 312,
                          fr"buttons\without text\default-phpstorm-btn.png",
                          fr"buttons\without text\hover-phpstorm-btn.png",
                          fr"buttons\without text\press-phpstorm-btn.png", r"data\sounds\menu-button-sound.mp3",
                          "")

    campaign_name = Object(campaign_btn.x + campaign_btn.width / 2 - 238 / 2, campaign_btn.y + campaign_btn.height + 16,
                           238, 45,
                           fr"objects\rus\campaign-obj.png")
    phpStorm_name = Object(phpStorm_btn.x + phpStorm_btn.width / 2 - 250 / 2, phpStorm_btn.y + phpStorm_btn.height + 16,
                           250, 45,
                           fr"objects\rus\phpstorm-obj.png")

    running = True
    while running:

        windows.screen.blit(consts.menu_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    menu.main_menu()

            if event.type == pygame.USEREVENT and event.button == campaign_btn:
                transition()
                levels_menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == phpStorm_btn:
                transition()

            for button in [campaign_btn, phpStorm_btn]:
                button.handle_event(event, consts.volS)

        for obj in [field, campaign_name, phpStorm_name]:
            obj.draw(windows.screen)

        for button in [campaign_btn, phpStorm_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
