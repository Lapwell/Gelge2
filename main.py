from random import randrange
import pygame
import sys
import time
import background as bg

pygame.init()

#Colours
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0

#Load music
bg_music = pygame.mixer.music.load('assets/sounds/SpaceBopper.mp3') #Music made by my lil bro Charles :)

#Where pygame is setup
pygame.display.set_caption('Gelge 2')
WIDTH, HEIGHT = 800, 1200
ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 24)
FPS = 60
VEL = 4
BULLET_VEL = 8
P_SHIP = 80
E_SHIP = 60
clock = pygame.time.Clock()
dt = clock.tick(FPS)

#Pygame sprite stuff
star_array = []
star_num = randrange(16, 32)
star_count = 32
bullet_size = 8, 24
p_bullet_list = []

#Set pygame events
STAR_EVENT = 25
SHOOT_EVENT = 26
pygame.time.set_timer(STAR_EVENT, 971)
pygame.time.set_timer(SHOOT_EVENT, 2500)

i = 0
while i < star_count:
    star_array.append(bg.star(ROOT, randrange(0, WIDTH), randrange(0, HEIGHT)))
    i += 1


class bullet():
    def __init__(self, x, y, vel):
        self.object = pygame.Rect((x, y), bullet_size)
        self.vel = vel
    def move(self):
        if self.object.y < -bullet_size[1]:
            p_bullet_list.remove(self)
        self.object.y -= self.vel


class PlayerClass():
    def __init__(self, lives):
        img = pygame.image.load('assets/images/player_ship.png').convert_alpha()
        self.lives = lives
        self.sprite = pygame.transform.scale(img, (P_SHIP, P_SHIP))
        self.rect = self.sprite.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - P_SHIP)
    def move_player(self, VEL):
        self.rect.x -= VEL
    def shoot(self, vel):
        p_bullet_list.append(bullet(self.rect.x + P_SHIP / 2 - 4, self.rect.y, vel))


class Enemy1Class():
    def __init__(self, speed, lives):
        img = pygame.image.load('assets/images/enemy1.png').convert_alpha()
        self.speed = speed
        self.sprite = pygame.transform.scale(img, (E_SHIP, E_SHIP))
        self.rect = self.sprite.get_rect()


class Enemy2Class():
    def __init__(self, speed, lives):
        self.speed = speed
        self.lives = lives


def fps_counter():
    count = str(int(clock.get_fps()))
    fps_txt = FONT.render(count, True, WHITE)
    ROOT.blit(fps_txt, (fps_txt.get_width() - fps_txt.get_width()//2, fps_txt.get_height() - fps_txt.get_height()//2))

def custom_events():
    if pygame.event.get(STAR_EVENT):
        for item in star_array:
            item.value += 1

def draw_root(player_obj, enemy1_obj):
    ROOT.fill(BLACK)
    for item in star_array:
        item.animation()
    for item in p_bullet_list:
        pygame.draw.rect(ROOT, GREEN, item.object)
        item.move()
    ROOT.blit(player_obj.sprite, player_obj.rect)
    ROOT.blit(enemy1_obj.sprite, enemy1_obj.rect)
    fps_counter()
    pygame.display.update()

def check_events(player_obj):
    global bullet_count
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_obj.rect.x > 0:
        player_obj.move_player(VEL)
    if keys[pygame.K_RIGHT] and player_obj.rect.x + P_SHIP < WIDTH:
        player_obj.move_player(-VEL)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_SPACE] and len(p_bullet_list) < 2:
                print('pew pew')
                player_obj.shoot(16)


def main():
    run = True
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(loops= -1, start=0.0, fade_ms=8000)
    player_object = PlayerClass(3)
    enemy1_obj = Enemy1Class(16, 1)
    enemy2_obj = Enemy2Class(16, 2)
    while run:
        custom_events()  #For some reason, checking for custom events can not be immediatly before or after clock.tick()... not sure why
        draw_root(player_object, enemy1_obj)
        check_events(player_object)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if '__main__' == __name__:
    main()
