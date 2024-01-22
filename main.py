from start_screen import start_screen
from menu import main_menu
from load_image import load_image
import pygame

pygame.display.set_icon(load_image("objects\ico-obj.png"))

if __name__ == '__main__':
    main_menu()
