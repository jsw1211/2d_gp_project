from pico2d import *
import game_framework

import game_world
import menu_mode
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
            game_framework.change_mode(menu_mode)
        else:
            my_car.handle_event(event)

def init():
    global other_cars
    global background
    global my_car

    running = True

    other_cars = [Other_Car(i) for i in range(5)]
    game_world.add_objects(other_cars, 1)

    background = BackGround()
    game_world.add_object(background, 0)

    my_car = My_Car()
    game_world.add_object(my_car, 1)

    game_world.add_collision_pair('my_car:other_car', my_car, None)

    for other_car in other_cars:
        game_world.add_collision_pair('my_car:other_car', None, other_car)




def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collision()
    # delay(0.5)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass