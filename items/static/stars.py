import pygame

from misc import load_image


class Stars:
    def __init__(self, x, y, width, height, zeroStars_path, oneStar_path, twoStar_path, threeStar_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.zeroStar_image = load_image(zeroStars_path)
        self.zeroStar_image = pygame.transform.scale(self.zeroStar_image, (width, height))

        self.oneStar_image = load_image(oneStar_path)
        self.oneStar_image = pygame.transform.scale(self.oneStar_image, (width, height))

        self.twoStar_image = load_image(twoStar_path)
        self.twoStar_image = pygame.transform.scale(self.twoStar_image, (width, height))

        self.threeStar_image = load_image(threeStar_path)
        self.threeStar_image = pygame.transform.scale(self.threeStar_image, (width, height))

        self.rect = self.zeroStar_image.get_rect(topleft=(x, y))

    def draw(self, screen, record):
        current_image = load_image(r"objects\without text\stars-none-obj.png")
        if record == 0:
            current_image = self.zeroStar_image
        if record == 1:
            current_image = self.oneStar_image
        if record == 2:
            current_image = self.twoStar_image
        if record == 3:
            current_image = self.threeStar_image
        screen.blit(current_image, self.rect.topleft)
