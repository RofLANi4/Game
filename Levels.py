import pygame
from Setings import *
from support import import_csv_layout, import_cut_graphics
from tile import Tile, StatiTile
from Player import Player


class Level:
    def __init__(self,level_data,surface):
        self.display_surface = surface
        self.world_shift = 0
        self.player = pygame.sprite.GroupSingle()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        roof_layout = import_csv_layout(level_data['roof'])
        self.roof_sprites = self.create_tile_group(roof_layout, 'roof')

        partition_layout = import_csv_layout(level_data["partition"])
        self.partition_sprites = self.create_tile_group(partition_layout, "partition")

        wall_layout = import_csv_layout(level_data["wall"])
        self.wall_sprites = self.create_tile_group(wall_layout,"wall")

        start_layout = import_csv_layout(level_data["start"])
        self.start_sprites = self.create_tile_group(start_layout, "start")
        self.start_setup(start_layout)

        self.background = pygame.sprite.Group()
        self.background_sprite = StatiTile(WIDTH,0,0, pygame.image.load("assets/Level/Map1.png").convert())
        self.background.add(self.background_sprite)


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "roof":
                        roof_tile_list = import_cut_graphics("assets/Level/tiles 3.png")
                        tile_surface = roof_tile_list[int(val)]
                        sprite = StatiTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == "partition":
                        partition_tile_list = import_cut_graphics("assets/Level/tiles 3.png")
                        tile_surface = partition_tile_list[int(val)]
                        sprite = StatiTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == "wall":
                        sprite = Tile(tile_size,x,y)
                        sprite_group.add(sprite)

        return sprite_group

    def start_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val != "-1":
                    layout_tile_list = import_cut_graphics("assets/Level/tiles 3.png")
                    tile_surface = layout_tile_list[int(val)]
                    sprite = StatiTile(tile_size, x, y, tile_surface)

                    self.start_sprites.add(sprite)
                    if val == "152":
                        player = Player((x, y), [self.visible_sprites])
                        self.player.add(player)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < WIDTH / 4 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > WIDTH - (WIDTH / 4) and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def horizontal_collisions(self):
        player = self.player.sprite

        for sprite in self.wall_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def run(self):
        # create roof
        self.background.draw(self.display_surface)
        self.background.update(self.world_shift)

        self.roof_sprites.draw(self.display_surface)
        self.roof_sprites.update(self.world_shift)

        # create partition
        self.partition_sprites.draw(self.display_surface)
        self.partition_sprites.update(self.world_shift)

        # create player
        self.start_sprites.draw(self.display_surface)
        self.start_sprites.update(self.world_shift)

        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()

        self.wall_sprites.update(self.world_shift)

        self.horizontal_collisions()

        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x > WIDTH - (WIDTH / 4) and direction_x == 0:
              self.world_shift = -5
              player.rect.centerx -= 5

        elif player_x < WIDTH / 4 and direction_x == 0:
              self.world_shift = 5
              player.rect.centerx += 5
        else:
            self.scroll_x()
