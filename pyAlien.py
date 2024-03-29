from assetLoader import AssetLoader
from sprites import Alien, Bomb, Bullet, Explosion, Player
from randomUtil import chance
from pygame.locals import *
import pygame

display_width = 640
fps = 40
frames_between_difficulty_increase = 5 * fps


def repeat(frame, frames_between_action, action):
    if frame % frames_between_action == 0:
        action()


def build_background(asset_loader, display_rect):
    tile_image = asset_loader.load_image('background.gif')
    image = pygame.Surface(display_rect.size)
    for x in range(0, display_width, tile_image.get_width()):
        image.blit(tile_image, (x, 0))
    return image


def start_music(asset_loader):
    asset_loader.load_music('house_lo.wav')
    pygame.mixer.music.play(-1)


def increase_difficulty():
    Alien.spawn_percentage_chance = min(1.05 * Alien.spawn_percentage_chance, 1.0)
    Alien.bomb_percentage_chance = min(1.25 * Alien.bomb_percentage_chance, 1.0)
    Alien.frames_between_spawn = max(int(Alien.frames_between_spawn - 1), 3)
    Alien.speed = min(1.03 * Alien.speed, 14.0)


def main():
    pygame.init()

    pygame.display.set_caption('pyAlien')

    display_rect = Rect(0, 0, 640, 480)
    display = pygame.display.set_mode(display_rect.size)

    asset_loader = AssetLoader()

    background = build_background(asset_loader, display_rect)
    display.blit(background, (0, 0))
    pygame.display.flip()

    # Initialize sprite groups
    aliens = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    bombs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    last_alien = pygame.sprite.GroupSingle()

    # Initialize sprite classes
    Alien.init(asset_loader, [all, aliens, last_alien])
    Bomb.init(asset_loader, [all, bombs])
    Bullet.init(asset_loader, [all, bullets])
    Explosion.init(asset_loader, [all])
    Player.init(asset_loader, [all])

    start_music(asset_loader)

    player = Player(display_rect.midbottom)

    clock = pygame.time.Clock()
    frame = 0

    while player.alive():
        frame += 1
        key_state = pygame.key.get_pressed()

        fps_multiplier = 2 if key_state[K_BACKQUOTE] and key_state[K_LCTRL] else 1
        clock.tick(fps_multiplier * fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_SPACE:
                    if key_state[K_LCTRL]:
                        [alien.explode() for alien in aliens]
                    elif len(bullets) < Player.max_shots:
                        player.shoot()

        # Clear game object images before next frame
        all.clear(display, background)

        # Handle player movement
        move = key_state[K_RIGHT] - key_state[K_LEFT]
        player.move(move, display_rect)

        # Update game objects
        all.update(display_rect)

        # Check for collisions between aliens and bullets
        for bullet in pygame.sprite.groupcollide(bullets, aliens, False, True):
            bullet.explode()

        # Check for collisions between player and bombs
        for bomb in pygame.sprite.spritecollide(player, bombs, False):
            bomb.explode()
            player.explode()

        # Check for collisions between player and aliens
        for alien in pygame.sprite.spritecollide(player, aliens, False):
            alien.explode()
            player.explode()

        # Last alien to potentially drop bomb
        if chance(Alien.bomb_percentage_chance) and last_alien.sprite:
            last_alien.sprite.shoot()

        # Potentially spawn new alien
        repeat(frame, Alien.frames_between_spawn, lambda: Alien.spawn_with_chance(display_rect))

        # Increase game difficulty over time
        repeat(frame, frames_between_difficulty_increase, increase_difficulty)

        # Draw updated game objects
        all_rects = all.draw(display)

        # Render new display
        pygame.display.update(all_rects)


if __name__ == '__main__':
    main()
