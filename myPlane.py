import pygame

#我方飞机
class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load('image/myPlane1.png').convert_alpha()
        self.image2 = pygame.image.load('image/myPlane2.png').convert_alpha()
        self.destroy_image = pygame.image.load('image/myPlaneDestroy.png').convert_alpha()
        self.rect = self.image1.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
                        (self.bg_width - self.rect.width) // 2, \
                        self.bg_height - self.rect.height - 60 #预留画面下方状态栏位置
        self.speed = 10
        self.is_alive = True#标记战机是否存活
        self.invincible = False #战机无敌状态标记
        self.mask = pygame.mask.from_surface(self.image1) #将图片中的非透明部分标记为mask便于做更好的碰撞检测

    #控制飞机移动，注意不能超出边界
    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.bg_height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.bg_height - 60

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.bg_width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.bg_width

    def reset(self):
        self.rect.left, self.rect.top = \
                        (self.bg_width - self.rect.width) // 2, \
                        self.bg_height - self.rect.height - 60 #预留画面下方状态栏位置
        self.is_alive = True
        self.invincible = True #仅当战机重生时设置为无敌
        
