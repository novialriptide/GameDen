import pygame


class TileMap:
    def __init__(self, map_data: dict, tileset):
        self.map_data = map_data
        map_contents = self.map_data["contents"]
        self.map_size = (len(map_contents[0][0]), len(map_contents[0]))

        self.tileset = tileset
        self.tile_size = tileset.tile_size
        self.textures = tileset.textures

    def get_position_by_px(self, position: tuple) -> tuple:
        x_px, y_px = position
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size

        return (
            (t_width * m_width - x_px) / m_width,
            (t_height * m_width - y_px) / m_height,
        )

    def get_tile_id(self, position: tuple, layer: int) -> int:
        row, column = position
        try:
            return self.map_data["contents"][layer][row][column]
        except TypeError:
            raise Exception(f"tile location doesn't exist ({row}, {column})")

    def get_collision_rects(
        self, position: tuple, layer: int, render_size: int = 1
    ) -> list:
        collision_rects = []
        a_x, a_y = position
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size

        y = 0
        for row in range(m_height):
            x = 0
            for column in range(m_width):
                tile_id = self.get_tile_id((row, column), layer)
                if tile_id != 0:
                    rect = pygame.Rect(
                        (
                            (a_x + x, a_y + y),
                            (t_width * render_size, t_height * render_size),
                        )
                    )
                    collision_rects.append([rect, tile_id])

                x += int(t_width * render_size)
            y += int(t_height * render_size)
        return collision_rects

    def set_position(self, new_position):
        self.rect.x, self.rect.y = new_position

    def create_new_layer(self):
        self.tilemap["contents"].append(
            [[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])]
        )

    def get_image_layer(self, layer_id: int):
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size
        map_surface = pygame.Surface(
            (t_width * m_width, t_height * m_height), pygame.SRCALPHA, 32
        )
        map_surface = map_surface.convert_alpha()

        for row in range(m_height):
            for column in range(m_width):
                tile_id = self.get_tile_id((row, column), layer_id)
                self.tileset.pygame_render(
                    (column * t_width, row * t_height), map_surface, tile_id
                )

        return map_surface

    def get_image_map(self):
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size
        map_surface = pygame.Surface(
            (t_width * m_width, t_height * m_height), pygame.SRCALPHA, 32
        )
        map_surface = map_surface.convert_alpha()

        for layer in range(len(self.map_data["contents"])):
            if layer not in self.map_data["invisible_layers"]:
                map_surface.blit(self.get_image_layer(layer), (0, 0))

        return map_surface
