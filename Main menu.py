import pygame, sys
from abc import abstractmethod, ABC


pygame.init()


class Sprites(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/ride_1.jpg").convert())
        self.sprites.append(pygame.image.load("assets/ride_2.jpg").convert())
        self.sprites.append(pygame.image.load("assets/ride_3.jpg").convert())
        self.sprites.append(pygame.image.load("assets/ride_4.jpg").convert())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()

    def update(self):
        self.current_sprite += 1

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]


class Name:
    def __init__(self, x, y, screen):
        self.screen = screen
        self.x = x
        self.y = y
        self.col_spd = 25
        self.maximum = 255
        self.minimum = 0

    def aray(self, col, dir):
        for i in range(len(col)):
            self.game_name(col[i])
            self.color_change(col[i], dir[i])

    def game_name(self,color):
        font = pygame.font.Font("assets/font.ttf", 50)
        name = font.render("D R I V E", True, color)
        name_rect = name.get_rect()
        name_rect.center = (self.x/2, self.y/10)
        self.screen.blit(name, name_rect)

    def color_change(self, col, dir):
        for i in range(3):
            col[i] += self.col_spd * dir[i]
            if col[i] >= self.maximum or col[i] <= self.minimum:
                dir[i] *= -1
                col[i] += self.col_spd * dir[i]


class Button:
    def __init__(self, x, y, fonts, text_input, color, hovering_color):
        self.x = x
        self.y = y
        self.text_input = text_input
        self.color = color
        self.hovering_color = hovering_color
        self.font = fonts
        self.text = self.font.render(self.text_input, True, self.color)
        self.text_rect = self.text.get_rect(center=(self.x/2, self.y/3))

    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.color)


class Clicked(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def button_was_clicked(self, x, y, screen, fonts):
        pass


class Play(Clicked):
    def button_was_clicked(self, x, y, screen, fonts):
        while True:
            play_screen = pygame.image.load("assets/option.jpg")
            play_screen_rect = play_screen.get_rect()
            screen.blit(play_screen, play_screen_rect)

            mouse = pygame.mouse.get_pos()

            play_text = fonts.render("The game is still in development", True, "White")
            play_text_rect = play_text.get_rect(center=(x/2,  y/3))
            screen.blit(play_text, play_text_rect)

            PLAY_BACK = Button(x, y / 0.5, font(50), "BACK", "WHITE", "#dd25c3")
            PLAY_BACK.changeColor(mouse)
            PLAY_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(mouse):
                        select_sound.play()
                        MainClass()

            pygame.display.update()


class Option(Clicked):
    def button_was_clicked(self, x, y, screen, fonts):
        while True:
            play_screen = pygame.image.load("assets/option.jpg")
            play_screen_rect = play_screen.get_rect()
            screen.blit(play_screen, play_screen_rect)

            mouse = pygame.mouse.get_pos()

            option_text = fonts.render("Volume options", True, "White")
            option_text_rect = option_text.get_rect(center=(x/2, y/3.5))
            screen.blit(option_text, option_text_rect)

            volume = Volume(x, y, screen)

            OPTION_BACK = Button(x, y / 0.43, font(50), "BACK", "WHITE", "#dd25c3")
            OPTION_BACK.changeColor(mouse)
            OPTION_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if volume.checkForInput(mouse):
                        pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTION_BACK.checkForInput(mouse):
                        select_sound.play()
                        MainClass()

            pygame.display.update()


class Volume:
    def __init__(self, x, y, screen):
        self.volume = round(pygame.mixer.music.get_volume(), 1)
        self.volume_down = pygame.draw.polygon(screen, "white", ([200, 250], [100, 300], [200, 350]))
        self.volume_up = pygame.draw.polygon(screen, "white", ([600, 250], [700, 300], [600, 350]))
        volume_text = font(50).render(f"{round(self.volume*100,1)}%", True, "White")
        volume_text_rect = volume_text.get_rect(center=(x/2, y/2))
        screen.blit(volume_text, volume_text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.volume_down.left, self.volume_down.right) and position[1] in range(self.volume_down.top, self.volume_down.bottom):
            pygame.mixer.music.set_volume(self.volume-0.1)
        elif position[0] in range(self.volume_up.left, self.volume_up.right) and position[1] in range(self.volume_up.top, self.volume_up.bottom):
            pygame.mixer.music.set_volume(self.volume + 0.1)
        return False


class MainClass:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(pygame.image.load("assets/Logo1.jpg"))
        pygame.display.set_caption("KPZFP'S PROJECT")
        self.x = 800
        self.y = 600
        self.screen = pygame.display.set_mode((self.x, self.y))

        self.sprites = pygame.sprite.Group()
        sprite = Sprites()
        self.sprites.add(sprite)

        NAME = Name(self.x, self.y, self.screen)

        col_dir = [[-1, -1, -1]]
        def_col = [[255, 150, 100]]

        while True:
            PLAY = Button(self.x, self.y, font(60), "PLAY", "#fdb9f4", "#f5ac5d")
            OPTIONS = Button(self.x / 1.6, self.y / 0.365, font(50), "OPTIONS", "WHITE", "#dd25c3")
            QUIT = Button(self.x / 0.637, self.y / 0.365, font(50), "QUIT", "WHITE", "#dd25c3")

            play = Play()
            option = Option()

            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY.checkForInput(mouse):
                        select_sound.play()
                        play.button_was_clicked(self.x, self.y, self.screen, font(20))
                    if OPTIONS.checkForInput(mouse):
                        select_sound.play()
                        option.button_was_clicked(self.x, self.y, self.screen, font(45))
                    if QUIT.checkForInput(mouse):
                        pygame.quit()
                        sys.exit()

            self.sprites.draw(self.screen)
            self.sprites.update()

            NAME.aray(def_col, col_dir)

            for i in [PLAY, OPTIONS, QUIT]:
                i.changeColor(mouse)
                i.update(self.screen)
            pygame.display.update()

            self.clock.tick(8)


def font(size):
    return pygame.font.Font("assets/font.ttf", size)


select_sound = pygame.mixer.Sound("assets/FREE SOUND EFFECTS - Video Game Menu Select.ogg")
select_sound.set_volume(0.1)
pygame.mixer.music.load("assets/M.O.O.N - Dust (Synthwave).ogg",)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
stat = MainClass()
