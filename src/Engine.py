from pygame import *
from Camera2D import Camera2D
import math

# Global Variable initialization
FOV = 90
ray = 0
screen_scale = 8
move_speed = float(screen_scale)
pan_speed = 10
moving_f = False
moving_r = False
moving_b = False
moving_l = False
pan_velocity = 0  # right is positive, left is negative (for view)
screen_w = float(FOV * screen_scale)
screen_h = float(60 * screen_scale)
playing = True
camera = Camera2D(max_x=screen_w, max_y=screen_h)  # for this camera, forward and right will be considered the positive axes

# camera starts at (1,1) facing 270 (which is the positive x axis)
level_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

init()

screen = display.set_mode((int(screen_w), int(screen_h)))
display.set_caption('Ray Casting Engine')


def handlekeydown(e):
    global pan_speed, moving_b, moving_f, moving_l, moving_r, pan_velocity

    if e.key == K_ESCAPE:
        return False
    elif e.key == K_w:  # move forward
        moving_f = True
    elif e.key == K_a:  # move left
        moving_l = True
    elif e.key == K_s:  # move backward
        moving_b = True
    elif e.key == K_d:  # move right
        moving_r = True
    elif e.key == K_RIGHT:
        pan_velocity += pan_speed
    elif e.key == K_LEFT:
        pan_velocity -= pan_speed

    return True


def handlekeyup(e):
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
    """""
    Updates the camera position/rotation
    """""
    angle = camera.get_direction()
    camera.increment_x(
        (0, move_speed * math.cos(math.radians(angle)))[moving_f] +
        (0, move_speed * math.cos(math.radians((angle - 90) % 180)))[moving_r] +
        (0, -move_speed * math.cos(math.radians(angle)))[moving_b] +
        (0, -move_speed * math.cos(math.radians((angle + 90) % 180)))[moving_l]
    )
    camera.increment_y(
        (0, move_speed * math.sin(math.radians(angle)))[moving_f] +
        (0, move_speed * math.sin(math.radians((angle - 90) % 180)))[moving_r] +
        (0, -move_speed * math.sin(math.radians(angle)))[moving_b] +
        (0, -move_speed * math.sin(math.radians((angle + 90) % 180)))[moving_l]
    )
    camera.increment_direction(pan_velocity)


def refresh_screen():
    """""
    Updates what is being shown on the display
    """""

def find_intersection_distance(camera, ray):
    """""
    Starting from @camera, and going in direction @ray, 
    finds the distance in a straight line (this is not the
    distance to use when printing to the screen)
    """""
    return -1


def print_wall(column_num, scaled_distance):
    """""
    Given a column number and a distance to scale to, prints
    a wall to the screen at the scaled distance
    """""
    print()


def determine_color(distance):
    return 0, 0, 0


def main():
    global screen, ray, playing, camera

    while playing:
        # determine what the user wants
        for e in event.get():
            if e.type == QUIT:
                playing = False
            elif e.type == KEYDOWN:
                display.update()

                playing = handlekeydown(e)  # will return false if the escape key was pressed
            elif e.type == KEYUP:
                handlekeyup(e)

        update_camera()
        x = camera.get_x()
        y = camera.get_y()
        # resetting screen
        screen.fill((0, 0, 0))
        # drawing "camera"
        draw.circle(screen,
                    (0, 255, 0),
                    (int(x),
                     int(y)),
                    5)
        # drawing line in direction facing
        draw.line(screen,
                  (255, 0, 0),
                  (int(x),
                   int(y)),
                  (int(x + 20 * math.cos(math.radians(camera.get_direction()))),
                   int(y + 20 * math.sin(math.radians(camera.get_direction())))))
        # actual drawing portion (very slow)
        display.update()

        # ray = (ray + 1) % FOV


if __name__ == '__main__':
    init()
    main()
    quit()
