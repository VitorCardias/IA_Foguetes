class Rocket:
    def __init__(self, x=700, y=300, velocity_x=0, velocity_y=0, fuel=100):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.fuel = fuel
        self.width = 40
        self.height = 60

    def apply_gravity(self, gravity=0.1):
        self.velocity_y += gravity

    def apply_thrust(self, thrust_x, thrust_y):
        if self.fuel > 0:
            self.velocity_x += thrust_x
            self.velocity_y -= thrust_y
            self.fuel -= abs(thrust_x) + abs(thrust_y)

    def update_position(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def check_collision(self, landing_pad):
        if (
            self.x + self.width > landing_pad.x and
            self.x < landing_pad.x + landing_pad.width and
            self.y + self.height > landing_pad.y and
            self.y < landing_pad.y + landing_pad.height
        ):
            return True
        return False

    def is_out_of_bounds(self, screen_width, screen_height):
        return self.x < 0 or self.x > screen_width or self.y > screen_height or self.y < 0
