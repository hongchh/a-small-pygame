import pygame
from random import *

#小型敌方飞机
class SmallPlane(pygame.sprite.Sprite):
    energy = 1 #总血量
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('image/smallPlane.png').convert_alpha()
        self.destroy_image = pygame.image.load('image/smallPlaneDestroy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.speed = 2
        self.rect.left, self.rect.top = \
                        randint(0, self.bg_width - self.rect.width), \
                        randint(-5 * self.bg_height, 0)#出现位置随机，在屏幕上方出现，制造从远方飞进屏幕的效果
        self.is_alive = True
        self.mask = pygame.mask.from_surface(self.image)#用于做完美碰撞检测
        self.energy = SmallPlane.energy #当前血量
    #飞机移动
    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:#超过屏幕下边界则重置
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = \
                        randint(0, self.bg_width - self.rect.width), \
                        randint(-5 * self.bg_height, 0)
        self.is_alive = True
        self.energy = SmallPlane.energy

#中型敌方飞机
class MiddlePlane(pygame.sprite.Sprite):
    energy = 8
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('image/middlePlane.png').convert_alpha()
        self.destroy_image = pygame.image.load('image/middlePlaneDestroy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = \
                        randint(0, self.bg_width - self.rect.width), \
                        randint(-10 * self.bg_height, -self.bg_height)
        self.is_alive = True
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MiddlePlane.energy

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = \
                        randint(0, self.bg_width - self.rect.width), \
                        randint(-10 * self.bg_height, -self.bg_height)
        self.is_alive = True
        self.energy = MiddlePlane.energy

#大型敌方飞机
class BigPlane(pygame.sprite.Sprite):
    energy = 20
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        #两张图片可用于切换显示BOSS特技
        self.image1 = pygame.image.load('image/bigPlane1.png').convert_alpha()
        self.image2 = pygame.image.load('image/bigPlane2.png').convert_alpha()
        self.destroy_image = pygame.image.load('image/bigPlaneDestroy.png').convert_alpha()
        self.rect = self.image1.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = \
                        randint(0, self.bg_width - self.rect.width), \
                        randint(-15 * self.bg_height, -5 * self.bg_height)
        self.is_alive = True
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = BigPlane.energy

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = \
                        randint(0, self.bg_width - self.rect.width), \
                        randint(-15 * self.bg_height, -5 * self.bg_height)
        self.is_alive = True
        self.energy = BigPlane.energy
