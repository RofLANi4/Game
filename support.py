from csv import reader
from os import walk
import pygame

from settings import tile_size


def import_csv_layout(path):
    with open(path) as map:
        roof_map = []
        level = reader(map, delimiter=",")
        for row in level:
            roof_map.append(list(row))

        return roof_map


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size))
            new_surf.set_colorkey("black")
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles


def import_folder(path):
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            stock_image = pygame.image.load(full_path).convert()
            stock_image.set_colorkey("green")
            image_surf = pygame.transform.scale(stock_image, (stock_image.get_size()[0]*2, stock_image.get_size()[1]*2))
            surface_list.append(image_surf)

    return surface_list
