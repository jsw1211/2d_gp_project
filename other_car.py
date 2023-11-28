from pico2d import *
import random
import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

other_car_image_x = 450 / 5
other_car_image_y = 555 / 8

class Run:
    @staticmethod
    def enter(other_car, e):
        pass

    @staticmethod
    def do(other_car):
        other_car.frame = (other_car.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        other_car.y -= other_car.dir * RUN_SPEED_PPS * game_framework.frame_time
        other_car.y = clamp(25, other_car.y, 1600 - 25)
        if other_car.dir == 1 and other_car.y > 1600 - 50:
            other_car.dir = -1
        elif other_car.dir == -1 and other_car.y < 50:
            other_car.dir = 1

    @staticmethod
    def draw(other_car):
        if other_car.dir == 1:
            other_car.image.clip_draw(385, 0, 80, 70, other_car.x, other_car.y, 100, 100)

class StateMachine:
    def __init__(self, other_car):
        self.other_car = other_car
        self.cur_state = Run


    def start(self):
        self.cur_state.enter(self.other_car, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.other_car)

    def draw(self):
        self.cur_state.draw(self.other_car)

class Other_Car:
    image = None

    def __init__(self, velocity = 1):
        self.x_pos = [230, 350, 485, 615]
        self.x, self.y = random.choice(self.x_pos), 800
        self.velocity = velocity
        self.frame = random.randint(0, 5)
        self.action = 3
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('car.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def update(self):
        self.state_machine.update()
        self.y -=self.velocity
        if self.y < 25:
            game_world.remove_object(self)

    