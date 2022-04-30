import pymunk

class Entity:
    def __init__(self, body, size, tilemap=None):
        self.tilemap = tilemap

        # animations
        self.tick = 0
        self.current_texture = None
        self.image_offset_position = [0, 0]

        # pymunk setup
        self.body = body
        self.width, self.height = size
        self.poly = pymunk.Poly(
            self.body,
            [
                (-self.width / 2, -self.height / 2),
                (self.width / 2, -self.height / 2),
                (self.width / 2, self.height / 2),
                (-self.width / 2, self.height / 2),
            ],
        )

    def set_position(self, position: tuple, tilemap):
        x, y = position
        m_x, m_y = tilemap.position
        t_width, t_height = tilemap.tile_size

        self.body.position[0] = m_x + t_width * tilemap.render_size * x
        self.body.position[1] = m_y + t_height * tilemap.render_size * y
