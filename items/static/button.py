class Button:
    def __init__(self, x, y, width, height, image_path, hover_image_path=None, press_image_path=None, sound_path=None,
                 no_active_image_path=None, hero=None, image_get_path=None, hover_image_get_path=None,
                 press_image_get_path=None, hover_2_image_path=None, no_normal_fs_image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = load_image(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))

        self.hover_image_2 = self.image
        if hover_2_image_path:
            self.hover_image_2 = load_image(hover_2_image_path)
            self.hover_image_2 = pygame.transform.scale(self.hover_image_2, (width, height))

        self.press_image = self.image
        if press_image_path:
            self.press_image = load_image(press_image_path)
            self.press_image = pygame.transform.scale(self.press_image, (width, height))

        self.no_active_image = self.image
        if no_active_image_path:
            self.is_no_active = True
            self.no_active_image = load_image(no_active_image_path)
            self.no_active_image = pygame.transform.scale(self.no_active_image, (width, height))
        else:
            self.is_no_active = False

        self.no_normal_fs_image = self.image
        if no_normal_fs_image_path:
            self.no_normal_fs_image = load_image(no_normal_fs_image_path)
            self.no_normal_fs_image = pygame.transform.scale(self.no_normal_fs_image, (width, height))

        if image_get_path:
            self.get_image = load_image(image_get_path)
            self.get_image = pygame.transform.scale(self.get_image, (width, height))

            self.hover_get_image = load_image(hover_image_get_path)
            self.hover_get_image = pygame.transform.scale(self.hover_get_image, (width, height))

            self.press_get_image = load_image(press_image_get_path)
            self.press_get_image = pygame.transform.scale(self.press_get_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

        self.is_hovered = False
        self.is_pressed = False
        self.is_slider = False

        self.hero = hero

    def check_passing(self, isActive=False):
        if isActive:
            self.is_no_active = False

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw_f11(self, screen, fs=None):
        if not windows.screenChecker:
            current_image = self.no_normal_fs_image
        else:
            if fs:
                if self.is_hovered:
                    current_image = self.hover_image_2
                else:
                    current_image = self.press_image
            else:
                if self.is_hovered:
                    current_image = self.hover_image
                else:
                    current_image = self.image
        screen.blit(current_image, self.rect.topleft)

    def draw_heroBtn(self, screen, hero, heroNow, isGetHero2):
        if heroNow == hero:
            current_image = self.press_image
        else:
            if isGetHero2:
                current_image = self.image
                if self.is_hovered:
                    current_image = self.hover_image
            else:
                current_image = self.get_image
                if self.is_hovered:
                    current_image = self.hover_get_image
                if self.is_pressed:
                    current_image = self.press_get_image
        screen.blit(current_image, self.rect.topleft)

    def draw(self, screen):
        current_image = self.image
        if self.is_no_active:
            current_image = self.no_active_image
        else:
            if self.is_hovered:
                current_image = self.hover_image
            if self.is_pressed:
                current_image = self.press_image
        screen.blit(current_image, self.rect.topleft)

    def drawPauseBtn(self, screen, hitNow):
        current_image = self.image
        if self.is_hovered:
            current_image = self.hover_image
        if hitNow:
            current_image = self.press_image
        screen.blit(current_image, self.rect.topleft)

    def handle_event(self, event, volS=1):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered and not self.is_no_active:
            self.is_pressed = True
            if self.sound:
                pygame.mixer.Sound.set_volume(self.sound, volS)
                self.sound.play()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_pressed:
            self.is_pressed = False
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def handle_event_slider(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered and not self.is_no_active:
            self.is_pressed = True
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=self))
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_pressed:
            self.is_pressed = False
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, button=self))
