from random import randrange
import background as bg
import pygame
import time
import sys

pygame.init()

#Colours
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0

#Where pygame is setup
pygame.display.set_caption('Gelge 2')
WIDTH, HEIGHT = 800, 800
ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 24)
FPS = 60
VEL = 4
BULLET_VEL = 8
P_SHIP_SIZE = 80
E_SHIP_SIZE = 52
clock = pygame.time.Clock()
bg_music = pygame.mixer.music.load('assets/sounds/SpaceBopper.mp3')  #Music made by my lil bro Charles :)

#dt is for removing movement from fps.
# t = pygame.time.get_ticks()
# dt = (t - getTicksLastFrame) / 1000.0
# getTicksLastFrame = t

#Pygame sprite stuff
star_array = []
star_num = randrange(16, 32)
star_count = 32
bullet_size = 8, 24
p_bullet_list = []
e_bullet_list = []
active_enemies = []  #This list is for storing the active/alive enemies on the screen. When an enemy is killed, it is removed from the list

#Set pygame events
STAR_EVENT = 25
SHOOT_EVENT = 26
pygame.time.set_timer(STAR_EVENT, 971)
pygame.time.set_timer(SHOOT_EVENT, 2500)

s = 0
while s < star_count:
    star_array.append(bg.star(ROOT, randrange(0, WIDTH), randrange(0, HEIGHT)))
    s += 1


#Class for the bullets from both the enemies and the player
class BulletClass():
    def __init__(self, x, y, vel, b_list):
        self.rect = pygame.Rect((x, y), bullet_size)
        self.vel = vel
        self.b_list = b_list
    def move(self):
        if self.rect.y < 0:
            self.b_list.remove(self)
        self.rect.y += self.vel
    def check_hits(self, list_to_check):
        hit_indices = self.rect.collidelistall(list_to_check)
        while len(hit_indices) > 0:
            self.b_list.remove(self)
            list_to_check.pop(hit_indices[0])
            hit_indices.pop(0)


#Obvious
class PlayerClass():
    def __init__(self, lives):
        img = pygame.image.load('assets/images/player_ship.png').convert_alpha()
        self.sprite = pygame.transform.scale(img, (P_SHIP_SIZE, P_SHIP_SIZE))
        self.rect = self.sprite.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - P_SHIP_SIZE)
        self.lives = lives
    def move_player(self, VEL):
        self.rect.x -= VEL
    def shoot(self):
        p_bullet_list.append(BulletClass(self.rect.x + P_SHIP_SIZE / 2 - 4, self.rect.y, -16, p_bullet_list))


#Class for all the enemies
class EnemyClass():
    def __init__(self, x_vel, y_vel, image_path):
        img = pygame.image.load(image_path).convert_alpha()  #Loads the image fron /assets
        self.sprite = pygame.transform.scale(img, (E_SHIP_SIZE, E_SHIP_SIZE))
        self.rect = self.sprite.get_rect()
        self.x_vel = x_vel
        self.y_vel = y_vel
    def move(self):
        #This if statement is for when the enemies hit the borders and move downwards.
        if self.rect.x <= -1 or self.rect.x >= WIDTH - E_SHIP_SIZE:
            self.x_vel *= -1
            self.rect.y += E_SHIP_SIZE
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
    def shoot(self):
        bullet_list.append(BulletClass(self.rect.x + E_SHIP_SIZE / 2 - 4, self.rect.y, 16, e_bullet_list))


def check_win_lose(active_enemies, player_object):
    if len(active_enemies) <= 0:
        print('VICTORY')
    if player_object.lives <= 0:
        print('DEFEAT')
    for i in active_enemies:
        if i.rect.y >= HEIGHT:
            print('DEFEAT')

def check_events(player_object):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_object.rect.x > 0:
        player_object.move_player(VEL)
    if keys[pygame.K_RIGHT] and player_object.rect.x + P_SHIP_SIZE < WIDTH:
        player_object.move_player(-VEL)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_SPACE] and len(p_bullet_list) < 2:
                player_object.shoot()

def draw_root(player_object, active_enemies):
    ROOT.fill(BLACK)
    for item in star_array:
        item.animation()
    for item in p_bullet_list:
        pygame.draw.rect(ROOT, GREEN, item.rect)
        item.move()
        item.check_hits(active_enemies)
    for item in e_bullet_list:
        pygame.draw.rect(ROOT, RED, item.rect)
        item.move()
        item.check_hits(player_object)
    for item in active_enemies:
        ROOT.blit(item.sprite, item.rect)
        item.move()
    ROOT.blit(player_object.sprite, player_object.rect)
    fps_counter()
    pygame.display.update()

def fps_counter():
    count = str(int(clock.get_fps()))
    fps_txt = FONT.render(count, True, WHITE)
    ROOT.blit(fps_txt, (fps_txt.get_width() - fps_txt.get_width()//2, fps_txt.get_height() - fps_txt.get_height()//2))

def custom_events():
    if pygame.event.get(STAR_EVENT):
        #This event is for the background stars to "twinkle"
        for item in star_array:
            item.value += 1


def main():
    run = True
    pygame.mixer.music.set_volume(1.0) #Play Charles' song
    pygame.mixer.music.play(loops= -1, start=0.0, fade_ms=8000)  #Starts the song, loops it and fades it in over 8secs
    player_object = PlayerClass(3)
    active_enemies.extend([EnemyClass(4, 0, 'assets/images/enemy1.png'), EnemyClass(3, 1, 'assets/images/enemy2.png')])
    while run:
        custom_events()
        draw_root(player_object, active_enemies)
        check_events(player_object)
        check_win_lose(active_enemies, player_object)
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if '__main__' == __name__:
    main()
