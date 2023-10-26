from pico2d import *

import game_world
from background import BackGround

def handle_event():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass

def create_world():
    global running
    global background

    running = True

    background = BackGround()
    game_world.add_object(background, 0)
    pass

def update_world():
    game_world.update()
    pass

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass

open_canvas(840, 650)
create_world()

while running:
    handle_event()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
