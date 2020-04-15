from pygame.sprite import Sprite
from sprites.bomb import Bomb
from sprites.explosion import Explosion
from randomUtil import chance
import random


class Alien(Sprite):

    # Require cls.init()
    images = []
    containers = []

    frames_per_image = 12
    frames_between_spawn = 16
    speed = 8
    spawn_percentage_chance = 0.20
    bomb_percentage_chance = 0.01

    @classmethod
    def init(cls, asset_loader, containers):
        Alien.images = [asset_loader.load_image(filename) for filename in ('alien1.gif', 'alien2.gif', 'alien3.gif')]
        cls.containers = containers

    @staticmethod
    def spawn_with_chance(display_rect):
        if chance(Alien.spawn_percentage_chance):
            direction = random.choice([-1, 1])
            if direction == -1:
                Alien(direction, right=display_rect.right)
            else:
                Alien(direction, left=display_rect.left)

    def __init__(self, direction, **kwargs):
        Sprite.__init__(self)
        [group.add(self) for group in Alien.containers]
        self.frame = 0
        self.direction = direction
        self.image = Alien.images[0]
        self.rect = self.image.get_rect(**kwargs)

    def update(self, display_rect):
        self.rect.move_ip(self.direction * Alien.speed, 0)
        if not display_rect.contains(self.rect):
            self.direction = -self.direction
            self.rect.move_ip(0, self.rect.height + 1)
            self.rect.clamp_ip(display_rect)
        self.frame += 1
        self.image = self.images[self.frame // self.frames_per_image % len(Alien.images)]

    def shoot(self):
        Bomb(self)

    def explode(self):
        Explosion(self)
        self.kill()
