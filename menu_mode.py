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

from my_car import My_Car
from other_car import Other_Car
from background import BackGround


def init():
    global menu
    menu = load_image('main.png')

def finish():
    global menu
    menu = None

def pause():
    pass

def resume():
    pass


def create_new_world():
    server.background = BackGround()


    server.my_car = My_Car()


    #하드코딩
    # game_world.add_object(Zombie('zwi', 3800, 2560, 1.0), 1)
    # game_world.add_object(Zombie('jeni', 4000, 2560, 2.0), 1)
    # game_world.add_object(Zombie('jisu', 5000, 2560, 0.5), 1)

    #진짜 소프트 코딩
    with open('other_car_data.json', 'r') as f: # 파일을 오픈해서, f에 연결
        other_car_data_list = json.load(f)
        for item in other_car_data_list: #item : dictionary data
            # zombie = Zombie(item['name'], item['x'], item['y'], item['size'])
            other_car = Other_Car()
            other_car.__dict__.update(item)
            game_world.add_object(other_car, 1)
    # fill here


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            create_new_world()
            game_framework.change_mode(play_mode)

def update():
    pass

def draw():
    clear_canvas()
    menu.draw(get_canvas_width()//2, get_canvas_height()//2, 840, 650)
    update_canvas()






