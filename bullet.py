import pygame

#普通子弹
class Bullet1(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('image/bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = position[0] - self.rect.width // 2
        self.rect.top = position[1] - self.rect.height
        self.speed = 12
        self.is_alive = True
        self.mask = pygame.mask.from_surface(self.image)#用于完美碰撞检测
    #子弹移动
    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:#超过边界则消失
            self.is_alive = False

    def reset(self, position):
        self.rect.left = position[0] - self.rect.width // 2
        self.rect.top = position[1] - self.rect.height
        self.is_alive = True

#超级子弹
class Bullet2(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('image/bullet2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = position[0] - self.rect.width // 2
        self.rect.top = position[1] - self.rect.height
        self.speed = 15
        self.is_alive = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.is_alive = False

    def reset(self, position):
        self.rect.left = position[0] - self.rect.width // 2
        self.rect.top = position[1] - self.rect.height
        self.is_alive = True
