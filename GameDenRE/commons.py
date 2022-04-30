import pymunk
import math
import json


def _calculate_segment_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    exception_msg = "two lines inputted are parallel or coincident"

    dem = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if dem == 0:
        raise Exception(exception_msg)

    t1 = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    t = t1 / dem

    u1 = (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)
    u = -(u1 / dem)

    if t >= 0 and t <= 1 and u >= 0 and u <= 1:
        Px = x1 + t * (x2 - x1)
        Py = y1 + t * (y2 - y1)
        return Px, Py
    else:
        raise Exception(exception_msg)


def convert_rect_to_wall(rect):
    return (
        (rect.left, rect.top, rect.right, rect.top),
        (rect.left, rect.bottom, rect.right, rect.bottom),
        (rect.left, rect.top, rect.left, rect.bottom),
        (rect.right, rect.top, rect.right, rect.bottom),
    )


def convert_rects_to_walls(rects):
    walls = []
    for rect in rects:
        wall_lines = convert_rect_to_wall(rect)
        for wall_line in range(len(wall_lines)):
            walls.append(wall_lines[wall_line])
    return walls


def get_ray_endpoint(coord1, coord2, walls):
    x1, y1 = coord1
    x2, y2 = coord2
    line_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    highest_point = (x2, y2)
    highest_point_length = line_length
    for wall in walls:
        try:
            c = _calculate_segment_intersection(
                x1, y1, x2, y2, wall[0], wall[1], wall[2], wall[3]
            )
            c_length = math.sqrt((x1 - c[0]) ** 2 + (y1 - c[1]) ** 2)
            if highest_point_length > c_length:
                highest_point = c
                highest_point_length = c_length
        except:
            pass
    return highest_point


def get_v_movement(degree, speed):
    radian = math.radians(degree)
    x_distance = math.cos(radian) * speed
    y_distance = math.sin(radian) * speed
    return [x_distance, y_distance]


def convert_tiledjson(path):
    """Converts a tiled json map in GameDen's formatting"""
    with open(path, "r") as file:
        loaded_json = json.load(file)

    contents = []
    for layer in range(len(loaded_json["layers"])):
        json_contents = loaded_json["layers"][layer]["data"]
        n = loaded_json["width"]
        layer_contents = [
            json_contents[i * n : (i + 1) * n]
            for i in range((len(json_contents) + n - 1) // n)
        ]
        contents.append(layer_contents)
    tilemap = {
        # contents[layer_number][row][column]
        "contents": contents,
        "collision_layer": None,
        "invisible_layers": [],
    }
    return tilemap


def add_rects_to_space(space: pymunk.Space, rects: list) -> list:
    """This function should executed ONCE"""
    for rect in rects:

        def zero_gravity(body, gravity, damping, dt):
            pymunk.Body.update_velocity(body, (0, 0), damping, dt)

        _w, _h = rect[0].width, rect[0].height

        rect_b = pymunk.Body(1, 2, body_type=pymunk.Body.STATIC)
        rect_b.position = rect[0].x + _w / 2, rect[0].y + _h / 2
        rect_b.gameden = {"tile_id": rect[1]}
        rect_poly = pymunk.Poly(
            rect_b,
            [
                (-_w / 2, -_h / 2),
                (_w / 2, -_h / 2),
                (_w / 2, _h / 2),
                (-_w / 2, _h / 2),
            ],
        )
        rect_poly.friction = 0.8
        rect_poly.gameden = {"tile_id": rect[1]}
        space.add(rect_b, rect_poly)
        rect_b.velocity_func = zero_gravity

        rect.append(rect_b)
        rect.append(rect_poly)

    return rects
