import pygame
import random

#全屏炸弹补给包
class BombSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('image/bombSupply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.bg_width - self.rect.width), -100
        self.speed = 5
        self.is_alive = False #是否出现补给包标记
        self.mask = pygame.mask.from_surface(self.image)#用于做完美碰撞检测

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:#超过下边界则视为玩家没获取该补给包，补给包消失
            self.is_alive = False

    def reset(self):
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.bg_width - self.rect.width), -100
        self.is_alive = True

#超级子弹补给包
class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('image/bulletSupply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.bg_width - self.rect.width), -100
        self.speed = 5
        self.is_alive = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.is_alive = False

    def reset(self):
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.bg_width - self.rect.width), -100
        self.is_alive = True
