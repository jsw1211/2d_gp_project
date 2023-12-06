from pico2d import *
import random
import game_framework
import game_world

other_car_image_x = 450 / 5
other_car_image_y = 555 / 8


class Other_Car:
    image = None

    def __init__(self , y):
        self.x_pos = [230, 350, 485, 615]
        self.x, self.y = random.choice(self.x_pos), random.randint(600, 10000)
        self.velocity = 5

        if Other_Car.image == None:
            Other_Car.image = load_image('car.png')

    def draw(self):
        self.image.clip_draw(385, 0, 80, 70, self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.velocity += 0.001
        self.y -= self.velocity
        if self.y < 100:
            self.x = random.choice(self.x_pos)
            self.y = random.randint(900, 1500)

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40

    def handle_collision(self, group, other):
        if group == 'my_car:other_car':
            game_world.remove_object(self)
