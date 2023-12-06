# 이것은 각 상태들을 객체로 구현한 것임.
import math

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle, load_wav

import game_over
import game_world
import game_framework
import menu_mode
import server


# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



class Idle:

    @staticmethod
    def enter(my_car, e):
        pass

    @staticmethod
    def exit(my_car, e):
        pass

    @staticmethod
    def do(my_car):
        if my_car.end:
            server.background.end = True
            game_framework.change_mode(game_over)
        pass


    @staticmethod
    def draw(my_car):
        my_car.image.clip_draw(385, 500, 80, 70, my_car.x, my_car.y, 100, 100)
        my_car.draw_life()



class Run:

    @staticmethod
    def enter(my_car, e):
        if my_car.x == 230:
            if right_down(e) or left_up(e): # 오른쪽으로 RUN
                my_car.x, my_car.action, my_car.face_dir = my_car.x + 120, 1, 1
            elif left_down(e) or right_up(e): # 왼쪽으로 RUN
                my_car.action, my_car.face_dir = 0, -1
        elif my_car.x == 350:
            if right_down(e) or left_up(e): # 오른쪽으로 RUN
                my_car.x, my_car.action, my_car.face_dir = my_car.x + 135, 1, 1
            elif left_down(e) or right_up(e): # 왼쪽으로 RUN
                my_car.x, my_car.action, my_car.face_dir = my_car.x - 120, 0, -1
        elif my_car.x == 485:
            if right_down(e) or left_up(e): # 오른쪽으로 RUN
                my_car.x, my_car.action, my_car.face_dir = my_car.x + 130, 1, 1
            elif left_down(e) or right_up(e): # 왼쪽으로 RUN
                my_car.x, my_car.action, my_car.face_dir = my_car.x - 135, 0, -1
        elif my_car.x == 615:
            if right_down(e) or left_up(e): # 오른쪽으로 RUN
                my_car.action, my_car.face_dir = 1, 1
            elif left_down(e) or right_up(e): # 왼쪽으로 RUN
                my_car.x, my_car.action, my_car.face_dir = my_car.x - 130, 0, -1
        my_car.sound_brake.play()

    @staticmethod
    def exit(my_car, e):
        pass

    @staticmethod
    def do(my_car):
        my_car.x = clamp(210, my_car.x, 625)
        if my_car.end:
            game_framework.change_mode(game_over)
            server.background.end = True

    @staticmethod
    def draw(my_car):
        my_car.image.clip_draw(385, 500, 80, 70, my_car.x, my_car.y, 100, 100)
        my_car.draw_life()



class StateMachine:
    def __init__(self, my_car):
        self.my_car = my_car
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
        }

    def start(self):
        self.cur_state.enter(self.my_car, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.my_car)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.my_car, e)
                self.cur_state = next_state
                self.cur_state.enter(self.my_car, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.my_car)





class My_Car:
    life = 3

    def __init__(self):
        self.x, self.y = 350, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('car.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.life_image = load_image('life.png')
        self.end = False
        self.sound_crash = load_wav('sound\\car_crash.mp3')
        self.sound_crash.set_volume(32)
        self.sound_brake = load_wav('sound\\brake.mp3')
        self.sound_brake.set_volume(32)


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 50, self.x + 40, self.y + 50

    def handle_collision(self, group, other):
        if group == 'my_car:other_car':
            self.life -= 1
            self.sound_crash.play()
            if self.life < 1:
                self.end = True

    def draw_life(self):
        for i in range(self.life):
            self.life_image.draw(50 + i * 70, 600, 50, 50)
