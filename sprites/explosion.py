from pygame.sprite import Sprite
from pygame.transform import flip


class Explosion(Sprite):

    # Require cls.init()
    images = []
    sound = None
    containers = []

    lifetime = 12
    frames_per_image = 3

    @classmethod
    def init(cls, asset_loader, containers):
        cls.sound = asset_loader.load_sound('boom.wav')
        image = asset_loader.load_image('explosion1.gif')
        cls.images = [image, flip(image, 1, 0)]
        cls.containers = containers

    def __init__(self, sprite):
        Sprite.__init__(self)
        Explosion.sound.play()
        [group.add(self) for group in Explosion.containers]
        self.frame = 0
        self.image = Explosion.images[0]
        self.rect = self.image.get_rect(center=sprite.rect.center)

    def update(self, *args):
        self.frame += 1
        if self.frame >= Explosion.lifetime:
            self.kill()
        self.image = self.images[self.frame // self.frames_per_image % len(Explosion.images)]
