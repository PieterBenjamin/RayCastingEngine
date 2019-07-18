from pygame import *
from Camera2D import Camera2D
import math

""" Game state (don't play with these) """
level_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
playing = True
slice_size = 90  # width of each slice on the screen
screen_hscale = len(level_map[0])
screen_vscale = len(level_map)
max_dist = math.sqrt(pow((screen_hscale - 2), 2) + pow((screen_vscale - 2), 2))
moving_f = False  # moving forward
moving_r = False  # moving right
moving_b = False  # moving backward
moving_l = False  # moving left
pan_velocity = 0  # right is positive, left is negative
screen_w = float(slice_size * screen_hscale)
screen_h = float(slice_size * screen_vscale)
camera = Camera2D(x=screen_hscale/2, y=screen_vscale-1.001, direction=270)
ray_num = 0

""" Used in computing the height of a slice """
m = (screen_h * 0.8)/(1 - max_dist)
b = screen_h - m

""" Customization variables (play with these) """
top_down = False
move_speed = 0.1  # how much WASD moves the camera
pan_speed = 3  # how much the L/R arrow keys will pan
ray_length = 600
FOV = 90
BACKGROUND = (0, 0, 0)
RAY_COLOR = (255, 0, 0)
CAMERA_COLOR = (0, 255, 0)
SQUARE_COLOR = (0, 0, 255)


def handle_key_down(e):
    global pan_speed, moving_b, moving_f, moving_l, moving_r, pan_velocity

    if e.key == K_ESCAPE:
        return False
    elif e.key == K_w:
        moving_f = True
    elif e.key == K_a:
        moving_l = True
    elif e.key == K_s:
        moving_b = True
    elif e.key == K_d:
        moving_r = True
    elif e.key == K_RIGHT:
        pan_velocity += pan_speed
    elif e.key == K_LEFT:
        pan_velocity -= pan_speed

    return True


def handle_key_up(e):
    global pan_speed, moving_f, moving_b, moving_r, moving_l, pan_velocity

    if e.key == K_w:
        moving_f = False
    elif e.key == K_a:
        moving_l = False
    elif e.key == K_s:
        moving_b = False
    elif e.key == K_d:
        moving_r = False
    elif e.key == K_RIGHT:
        pan_velocity -= pan_speed
    elif e.key == K_LEFT:
        pan_velocity += pan_speed


def update_camera():
    global camera
    """
    Updates the camera position/rotation
    """
    x = camera.get_x()
    y = camera.get_y()
    angle = camera.get_direction()
    cos_angle = math.cos(math.radians(angle))
    sin_angle = math.sin(math.radians(angle))

    x_increment = (0, move_speed * cos_angle)[moving_f] + \
                  (0, -move_speed * math.cos(math.radians((angle - 90) % 360)))[moving_r] + \
                  (0, -move_speed * cos_angle)[moving_b] + \
                  (0, -move_speed * math.cos(math.radians((angle + 90) % 360)))[moving_l]

    y_increment = (0, move_speed * sin_angle)[moving_f] + \
                  (0, -move_speed * math.sin(math.radians((angle - 90) % 360)))[moving_r] + \
                  (0, -move_speed * sin_angle)[moving_b] + \
                  (0, -move_speed * math.sin(math.radians((angle + 90) % 360)))[moving_l]

    camera.increment_x(
        (0, x_increment)[(0 < x + x_increment < screen_hscale)
                         and level_map[int(y)][int((x + x_increment))] == 0]
    )
    camera.increment_y(
        (0, y_increment)[(0 < y + y_increment < screen_vscale)
                         and level_map[int((y + y_increment))][int(x)] == 0]
    )
    camera.increment_direction(pan_velocity)


def refresh_screen():
    global screen, ray_num
    """
    Updates what is being shown on the screen
    """
    x = camera.get_x()
    y = camera.get_y()
    direction = camera.get_direction()

    screen.fill(BACKGROUND)  # resetting screen
    ray_num = 45
    cast(x, y, lambda z: direction - z, lambda r: r - 1)
    ray_num = 45
    cast(x, y, lambda z: direction + z, lambda r: r + 1)

    if top_down:
        # drawing camera position
        draw.circle(screen, CAMERA_COLOR, (int(x * slice_size), int(y * slice_size)), 5)
        # drawing sight lines
        draw.line(screen,
                  (255, 255, 255),
                  (x * slice_size,
                   y * slice_size),
                  ((x * slice_size) + ray_length * math.cos(math.radians(direction - (FOV / 2))),
                   (y * slice_size + ray_length * math.sin(math.radians(direction - (FOV / 2))))))
        draw.line(screen,
                  (255, 255, 255),
                  (x * slice_size,
                   y * slice_size),
                  ((x * slice_size) + ray_length * math.cos(math.radians(direction + (FOV / 2))),
                   (y * slice_size) + ray_length * math.sin(math.radians(direction + (FOV / 2)))))
    display.update()


def cast(x, y, angle_calc, ray_inc):
    global screen, top_down, ray_num

    for ray in range(int(FOV / 2),):
        ray_dir = angle_calc(ray) % 360
        #  The following two variables represent the distance from the camera to the
        #  next horizontal (dy) and vertical (dx) grid line
        dy = -(y % 1) if math.sin(math.radians(ray_dir)) < 0 else 1 - (y % 1)
        dx = -(x % 1) if math.cos(math.radians(ray_dir)) < 0 else 1 - (x % 1)
        rise = math.sin(math.radians(ray_dir))
        run = math.cos(math.radians(ray_dir))

        coordinates = find_intersection_coordinates(x, y, rise/10, run/10)
        if top_down:
            draw.rect(screen, SQUARE_COLOR, coordinates)
        else:
            print_wall(ray_num, math.sqrt(pow((x - (coordinates[0]/slice_size)), 2) + pow((y - coordinates[1]/slice_size), 2)))
        ray_num = ray_inc(ray_num)


def find_intersection_coordinates(x, y, rise, run):
    global top_down
    """
    level_map[y][x]
    @param x:
        The index within the array
    @param y:
        The index of the array
    @param rise:
        The amount to increment @y
    @param run:
        The amount to increment @x

    Starting from (@x, @y), finds the coordinates of
    the first intersection in the level map, scaled to 
    the appropriate location on the screen.
    """
    orig_x = x
    orig_y = y
    while screen_hscale > x > 0 and screen_vscale > y > 0:
        x_index = int(x)
        y_index = int(y)

        if level_map[y_index][x_index] != 0:
            if top_down:
                draw.line(
                    screen,
                    RAY_COLOR,
                    (orig_x * slice_size, orig_y * slice_size),
                    (x * slice_size, y * slice_size)
                )

            return (x * slice_size), (y * slice_size), slice_size, slice_size
        x += run
        y += rise

    return 0, 0, 0, 0


def print_wall(column_num, scaled_distance):
    """
    Given a column number and a distance to scale to, prints a wall
    to the screen at the scaled distance (with appropriate color).
    """
    h = (m * scaled_distance) + b
    draw.rect(screen, determine_color(scaled_distance), (column_num * (screen_w/FOV), (screen_h - h)/2, screen_w/FOV, h))


def determine_color(distance):
    return 0, 0, (255 - 255*(distance/max_dist))


def main():
    global screen, playing, camera

    init()
    screen = display.set_mode((int(screen_w), int(screen_h)))
    display.set_caption('Pieter Benjamin\'s Ray Casting Engine')

    while playing:
        # determine what the user wants
        for e in event.get():
            if e.type == QUIT:
                playing = False
            elif e.type == KEYDOWN:
                playing = handle_key_down(e)  # will return false if the escape key was pressed
            elif e.type == KEYUP:
                handle_key_up(e)

        update_camera()
        refresh_screen()


if __name__ == '__main__':
    main()
    quit()
