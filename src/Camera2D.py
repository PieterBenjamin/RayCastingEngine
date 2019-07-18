class Camera2D:

    def __init__(self, x=1.0, y=1.0, direction=0.0):
        self.x = x
        self.y = y
        self.direction = direction

    def increment_x(self, x_increment):
        self.x = self.x + x_increment

    def increment_y(self, y_increment):
        self.y = self.y + y_increment

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
