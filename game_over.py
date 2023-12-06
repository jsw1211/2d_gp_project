import random
import json
import tomllib
import pickle
import os

from pico2d import *
import game_framework
import game_world

import server
import play_mode




def init():
    global game_over
    global font
    global bgm
    game_over = load_image('game_over.png')
    font = load_font('ENCR10B.TTF', 40)
    bgm = load_music('sound\\game_over.mp3')
    bgm.set_volume(32)
    bgm.play()


def finish():
    global game_over
    game_over = None

def pause():
    pass

def resume():
    pass


def create_new_world():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            create_new_world()
            server.background.end = False
            game_framework.change_mode(play_mode)

def update():
    pass

def draw():
    clear_canvas()
    game_over.draw(get_canvas_width()//2, get_canvas_height()//2 + 50)
    font.draw(840 // 2 - 200, 50, f'Final Score: {int(server.background.score)}', (0, 0, 0))
    update_canvas()






