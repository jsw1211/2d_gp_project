from pico2d import load_image
class BackGround:
    i = 0
    j = 650
    def __init__(self):
        self.image = load_image('background.png')
    def draw(self):
        self.image.clip_draw_to_origin(0,0, 840, 650, 0, self.i)
        self.image.clip_draw_to_origin(0,0, 840, 650, 0, self.j)
        self.j -= 2
        self.i -= 2
        if self.i == -650:
            self.i = 650
        if self.j == -650:
            self.j = 650
    def update(self):
        pass

