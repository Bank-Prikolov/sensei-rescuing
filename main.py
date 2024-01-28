from menu import main_menu
from intro import intro
from load_image import load_image
import pygame

pygame.display.set_icon(load_image(r"objects\ico-obj.png"))

if __name__ == '__main__':
    intro()
