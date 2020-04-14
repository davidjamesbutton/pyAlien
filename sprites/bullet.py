from pygame.sprite import Sprite
from sprites.explosion import Explosion


class Bullet(Sprite):

    # Require cls.init()
    image = None
    sound = None

    speed = 10

    @classmethod
    def init(cls, asset_loader, containers):
        cls.image = asset_loader.load_image('shot.gif')
        cls.sound = asset_loader.load_sound('car_door.wav')
        cls.containers = containers

    def __init__(self, midbottom):
        Sprite.__init__(self)
        [group.add(self) for group in Bullet.containers]
        Bullet.sound.play()
        self.image = Bullet.image
        self.rect = self.image.get_rect(midbottom=midbottom)

    def update(self, display_rect):
        self.rect.move_ip(0, -Bullet.speed)
        if self.rect.bottom < 0:
            self.kill()

    def explode(self):
        Explosion(self)
        self.kill()