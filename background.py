import pygame
import os.path

clock = pygame.time.Clock()
img_dir = os.path.join(os.path.abspath(os.getcwd()), 'assets/images')

if not os.path.exists(img_dir):
    raise TypeError('Error: assets/images cannot be found.')


class star():
    def __init__(self, ROOT, x, y):
        self.ROOT = ROOT
        self.value = 0
        self.img_list = []
        self.sprite_images = [pygame.image.load('assets//images/star1.png'), pygame.image.load('assets/images/star2.png')]
        self.len_sprites = len(self.sprite_images)
        self.x = x
        self.y = y
    def animation(self):
        if (self.value >= self.len_sprites):
            self.value = 0
        image = self.sprite_images[self.value]
        self.ROOT.blit(image, (self.x, self.y))
