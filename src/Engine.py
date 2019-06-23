from pygame import *
from Camera2D import Camera2D
import math

# debugging variables
ray_length = 600
# Global Variable initialization
FOV = 90
screen_size = 90
screen_scale = 8
move_speed = float(screen_scale)
pan_speed = 10
moving_f = False  # moving forward
moving_r = False  # moving right
moving_b = False  # moving backward
moving_l = False  # moving left
pan_velocity = 0  # right is positive, left is negative
screen_w = float(FOV * screen_scale)
screen_h = float(FOV * (screen_scale - 2))
playing = True
camera = Camera2D(max_x=screen_w, max_y=screen_h)  # forward and right are considered the positive axes
BACKGROUND = (0, 0, 0)
RAY_COLOR = (255, 0, 0)
CAMERA_COLOR = (0, 255, 0)
SQUARE_COLOR = (0, 0, 255)

# this is laid out like an image (positive y is down)
level_map = [[1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1]]

init()

screen=display.set_mode((int(screen_w), int(screen_h)))
display.set_caption('Ray Casting Engine')


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
    angle = camera.get_direction()
    cos_angle = math.cos(math.radians(angle))
    sin_angle = math.sin(math.radians(angle))

    camera.increment_x(
        (0, move_speed * cos_angle)[moving_f] +
        (0, -move_speed * math.cos(math.radians((angle - 90) % 360)))[moving_r] +
        (0, -move_speed * cos_angle)[moving_b] +
        (0, -move_speed * math.cos(math.radians((angle + 90) % 360)))[moving_l]
    )
    camera.increment_y(
        (0, move_speed * sin_angle)[moving_f] +
        (0, -move_speed * math.sin(math.radians((angle - 90) % 360)))[moving_r] +
        (0, -move_speed * sin_angle)[moving_b] +
        (0, -move_speed * math.sin(math.radians((angle + 90) % 360)))[moving_l]
    )
    camera.increment_direction(pan_velocity)


def refresh_screen():
    global screen
    """
    Updates what is being shown on the screen
    """
    x = camera.get_x()
    y = camera.get_y()
    direction = camera.get_direction()

    screen.fill(BACKGROUND)  # resetting screen

    # drawing sight lines
    draw.line(screen,
              RAY_COLOR,
              (int(x),
               int(y)),
              (int(x + ray_length * math.cos(math.radians(direction - (FOV/2)))),
               int(y + ray_length * math.sin(math.radians(direction - (FOV/2))))))
    draw.line(screen,
              RAY_COLOR,
              (int(x),
               int(y)),
              (int(x + ray_length * math.cos(math.radians(direction + (FOV/2)))),
               int(y + ray_length * math.sin(math.radians(direction + (FOV/2))))))

    # actual drawing portion (very slow)
    # print("casting...")
    cast(x,
         y,
         lambda z: direction - z)
    cast(x,
         y,
         lambda z: direction + z)

    # drawing camera position
    draw.circle(screen,
                CAMERA_COLOR,
                (int(x),
                 int(y)),
                5)

    display.update()


def cast(x, y, angle_calc):
    global screen

    for ray in range(int(FOV / 2)):
        dir_in_array = angle_calc(ray) % 360

        draw.line(screen,
                  RAY_COLOR,
                  (int(x),
                   int(y)),
                  (int(x + ray_length * math.cos(math.radians(dir_in_array))),
                   int(y + ray_length * math.sin(math.radians(dir_in_array)))))

        rise = math.sin(math.radians(dir_in_array))
        run = 0 if (dir_in_array == 90 or dir_in_array == 270) else math.cos(math.radians(dir_in_array))

        coordinates = find_intersection_coordinates(x / screen_size,
                                                    y / screen_size,
                                                    rise,
                                                    run)  # TODO: fix not Δy issue
        draw.rect(screen,
                  SQUARE_COLOR,
                  coordinates)


def find_intersection_coordinates(x, y, rise, run):
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
    the first intersection in the level map.
    """

    while (x < screen_scale) and (y < screen_scale - 2) and x > 0 and y > 0:
        x_index = int(x)
        y_index = int(y)

        if level_map[y_index][x_index] != 0:
            return (x_index * screen_size), (y_index * screen_size), \
                   ((x_index + 1) * screen_size) + screen_scale, ((y_index + 1) * screen_size) + screen_scale
        x += run
        y += rise

    return 0, 0, 10, 10


def print_wall(column_num, scaled_distance):
    """
    Given a column number and a distance to scale to, prints a wall
    to the screen at the scaled distance (with appropriate color).
    """


def determine_color(distance):
    return BACKGROUND


def main():
    global screen, playing, camera

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
    init()
    main()
    quit()
