from pygame.sprite import Sprite
from pygame.transform import flip
from sprites.bullet import Bullet
from sprites.bullet import Explosion


class Player(Sprite):

    # Require cls.init()
    left_image = None
    right_image = None

    bounce = 24
    gun_offset = -11
    max_shots = 3
    speed = 5

    @classmethod
    def init(cls, asset_loader, containers):
        cls.left_image = asset_loader.load_image('player1.gif')
        cls.right_image = flip(cls.left_image, 1, 0)
        cls.containers = containers

    def __init__(self, midbottom):
        Sprite.__init__(self)
        [group.add(self) for group in Player.containers]
        self.image = Player.left_image
        self.rect = self.image.get_rect(midbottom=midbottom)
        self.original_bottom = midbottom[1]
        self.facing = -1

    def shoot(self):
        Bullet((self.rect.centerx + self.facing * Player.gun_offset, self.rect.top))

    def move(self, direction, display_rect):
        if direction != 0:
            self.facing = direction
        if direction < 0:
            self.image = Player.left_image
        elif direction > 0:
            self.image = Player.right_image
        self.rect.move_ip((direction * Player.speed, 0))
        self.rect.bottom = self.original_bottom - (self.rect.left // self.bounce % 2)
        self.rect.clamp_ip(display_rect)

    def explode(self):
        Explosion(self)
        self.kill()