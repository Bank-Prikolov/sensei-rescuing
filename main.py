import pygame
from menu import main_menu
from start_screen import start_screen
from load_image import load_image

pygame.init()
pygame.display.set_caption('Sensei Rescuing')
pygame.display.set_icon(load_image(r"objects\without text\ico-obj.png"))
pygame.mouse.set_visible(False)

if __name__ == '__main__':
    main_menu()
    # start_screen()
