from pygame.sprite import Sprite
from sprites.explosion import Explosion


class Bomb(Sprite):

    # Require cls.init()
    image = None

    speed = 6

    @classmethod
    def init(cls, asset_loader, containers):
        cls.image = asset_loader.load_image('bomb.gif')
        cls.containers = containers

    def __init__(self, alien):
        Sprite.__init__(self)
        [group.add(self) for group in Bomb.containers]
        self.image = Bomb.image
        self.rect = self.image.get_rect(midtop=alien.rect.midbottom)

    def update(self, display_rect):
        self.rect.move_ip(0, Bomb.speed)
        if self.rect.top > display_rect.bottom:
            self.kill()

    def explode(self):
        Explosion(self)
        self.kill()