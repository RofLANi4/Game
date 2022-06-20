import pygame, sys
from Setings import *
from Levels import Level
from Game_data import level_0


class Game:
    def __init__(self,screen,back):
        self.screen = screen
        self.back = back
        self.clock = pygame.time.Clock()

        self.level = Level(level_0, self.screen)

    def run(self):

        while True:
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                self.back()
            self.screen.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.level.run()
            pygame.display.update()
            self.clock.tick(30)



