from pico2d import *
import game_framework

import game_world
from other_car import Other_Car
from background import BackGround
from my_car import My_Car


# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            my_car.handle_event(event)

def init():
    global other_car
    global background
    global my_car

    running = True

    other_car = Other_Car()
    game_world.add_object(other_car, 1)

    background = BackGround()
    game_world.add_object(background, 0)

    my_car = My_Car()
    game_world.add_object(my_car, 1)



def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # delay(0.5)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass