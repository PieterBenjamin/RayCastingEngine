class Camera2D:

    def __init__(self, x=1.0, y=1.0, direction=0.0, min_x=0.0, min_y=0.0, max_x=1.0, max_y=1.0):
        self.x = x
        self.y = y
        self.direction = direction
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def increment_x(self, x_increment):
        new_x = self.x + x_increment
        if (new_x <= self.max_x) & (new_x >= self.min_x):
            self.x = new_x

    def increment_y(self, y_increment):
        new_y = self.y + y_increment
        if (new_y <= self.max_y) & (new_y >= self.min_y):
            self.y = new_y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_direction(self):
        return self.direction

    def increment_direction(self, direction_increment):
        self.direction = (self.get_direction() + direction_increment) % 360

    def __str__(self):
        return "(" + str(int(self.x)) + ", " + str(int(self.y)) + "):" + str(int(self.ray_start))
