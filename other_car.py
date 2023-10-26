from pico2d import load_image

import game_world


class Other_Car:
    image = None

    def __init__(self, x = 420, y = 300, velocity = 1):
        if Other_Car.image == None:
            self.image = load_image('car.png')
        self.x, self.y, self.velocity = x, y, velocity
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        self.y -= self.velocity

        if self.y < 50:
            game_world.remove_object(self)
