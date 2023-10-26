from pico2d import load_image

class BackGround:
    def __init__(self):
        self.image = load_image('background.png')
    def draw(self):
        self.image.draw(420, 325)
    def update(self):
        pass
