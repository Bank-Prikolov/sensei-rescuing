class Object:
    def __init__(self, x, y, width, height, image_path, no_active_image_path=None, image_path2=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

        if image_path2:
            self.image2 = load_image(image_path2)
            self.image2 = pygame.transform.scale(self.image2, (width, height))

        self.no_active_image = self.image
        if no_active_image_path:
            self.is_no_active = True
            self.no_active_image = load_image(no_active_image_path)
            self.no_active_image = pygame.transform.scale(self.no_active_image, (width, height))
        else:
            self.is_no_active = False

        self.rect = self.image.get_rect(topleft=(x, y))

    def check_passing(self, isActive=False):
        if isActive:
            self.is_no_active = False

    def draw(self, screen):
        current_image = self.image
        if self.is_no_active:
            current_image = self.no_active_image
        screen.blit(current_image, self.rect.topleft)

    def drawLanguage(self, screen, languageNow):
        current_image = self.image
        if languageNow == 'rus':
            current_image = self.image
        elif languageNow == 'eng':
            current_image = self.image2
        screen.blit(current_image, self.rect.topleft)
