import pygame
from Setings import *
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.groups = groups
        self.status = "stay"
        self.facing_right = True

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 0

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.status = "shoot1"
            self.animation_speed = 0.2
            self.animate()
            self.animation_speed = 0.15

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
            self.animate()
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
            self.animate()
        else:
            self.direction.x = 0

    def get_status(self):
        if self.direction.x > 0:
            self.status = "walk1"
        elif self.direction.x < 0:
            self.status = "walk1"
        else:
            self.status = "stay"

    def animate(self):

        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

    def move(self,speed):
        self.rect.center += self.direction * speed

    def update(self):
        self.input()
        self.move(self.speed)
        self.animate()
        self.get_status()

    def import_character_assets(self):
        character_path = "assets/Character/"
        self.animations = {"walk1": [], "shoot1": [], "stay" : []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
