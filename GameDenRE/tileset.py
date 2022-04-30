import pygame


class TileSet:
    def __init__(self, textures_path: str, tile_size: tuple, tiles_distance: int = 0):
        self.textures = pygame.image.load(textures_path)
        self.tile_size = tile_size
        self.tiles_distance = tiles_distance
        self.tileset_size = (
            int((self.textures.get_size())[0] / self.tile_size[0]),
            int((self.textures.get_size())[1] / self.tile_size[1]),
        )

    def get_tile_id_pos(self, tile_id: int) -> tuple:
        """Returns the position of the inputed tile ID"""
        if (self.tileset_size[0] * self.tileset_size[1]) > tile_id:
            return (
                int(tile_id % (self.tileset_size)[0]),
                int(tile_id / (self.tileset_size)[0]),
            )

    def pygame_render(self, position: tuple, surface, tile_id: int):
        """Renders an image of a tile. tile_id can never be 0"""
        t_width, t_height = self.tile_size
        if tile_id != 0:
            tile_id = tile_id - 1

            # cropping
            tile = pygame.Surface(self.tile_size, pygame.SRCALPHA, 32)
            tile = tile.convert_alpha()
            t_x, t_y = self.get_tile_id_pos(tile_id)
            tile.blit(
                self.textures,
                (0, 0),
                (t_width * t_x, t_height * t_y, t_width, t_height),
            )
            surface.blit(tile, position)

    def pygame_render2(self, tile_id: int):
        """Returns an image of a tile. tile_id can never be 0"""
        tile = pygame.Surface(self.tile_size, pygame.SRCALPHA, 32)
        tile = tile.convert_alpha()
        if tile_id != 0:
            self.pygame_render(tile, (0, 0), tile_id)
            return tile
        else:
            return tile
