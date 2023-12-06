from pico2d import load_image, load_font, get_time, load_music

import game_framework
import server


class BackGround:
    i = 0
    j = 650
    def __init__(self):
        self.image = load_image('background.png')
        self.font = load_font('ENCR10B.TTF', 26)
        self.score = 0
        self.start_time = get_time()
        self.end = False
        self.bgm = load_music("sound\\background.mp3")
        self.bgm.set_volume(32)
        self.bgm.repeat_play()
        server.background = self

    def draw(self):
        self.image.clip_draw_to_origin(0,0, 840, 650, 0, self.i)
        self.image.clip_draw_to_origin(0,0, 840, 650, 0, self.j)
        self.j -= 2
        self.i -= 2
        if self.i == -650:
            self.i = 650
        if self.j == -650:
            self.j = 650

        self.font.draw(600, 600, f'(Score: {int(self.score)})', (255, 255, 0))
    def update(self):
        if self.end:
            self.bgm.pause()
        else:
            self.score = (get_time() - self.start_time) * 100
        pass

