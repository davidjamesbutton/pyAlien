import os
import pygame
import ssl
import urllib.request


class AssetLoader(object):

    folder = 'assets'
    source = 'https://raw.githubusercontent.com/pygame/pygame/master/examples/data'

    def __init__(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        # Allow https requests without certificate
        ssl._create_default_https_context = ssl._create_unverified_context

        self.loaded_images = {}
        self.loaded_sounds = {}

    def load_image(self, filename):
        if filename in self.loaded_images:
            return self.loaded_images[filename]

        filepath = os.path.join(self.folder, filename)

        if not os.path.exists(filepath):
            self.__download_asset(filename)

        image = pygame.image.load(filepath).convert()

        self.loaded_images[filename] = image

        return image

    def load_sound(self, filename):
        if filename in self.loaded_sounds:
            return self.loaded_sounds[filename]

        filepath = os.path.join(self.folder, filename)

        if not os.path.exists(filepath):
            self.__download_asset(filename)

        sound = pygame.mixer.Sound(filepath)

        self.loaded_images[filename] = sound

        return sound

    def load_music(self, filename):
        filepath = os.path.join(self.folder, filename)

        if not os.path.exists(filepath):
            self.__download_asset(filename)

        pygame.mixer.music.load(filepath)

    def __download_asset(self, filename):
        url = f'{AssetLoader.source}/{filename}'
        filepath = os.path.join(self.folder, filename)
        urllib.request.urlretrieve(url, filepath)


