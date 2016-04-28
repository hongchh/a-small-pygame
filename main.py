import pygame
import sys
import random
from pygame.locals import *

import myPlane
import enemy
import bullet
import supply

pygame.init()
pygame.mixer.init()

#游戏背景
bg_size = bg_width, bg_height = 426, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('Plane War ---更新版2')

background = pygame.image.load('image/background.jpg').convert()

#加载音乐音效
pygame.mixer.music.load('sound/bg_music.ogg')
pygame.mixer.music.set_volume(0.2)
bomb_sound = pygame.mixer.Sound('sound/bomb.wav')
bomb_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound('sound/getBomb.wav')
get_bomb_sound.set_volume(0.2)
bullet1_sound = pygame.mixer.Sound('sound/bullet1.wav')
bullet1_sound.set_volume(0.1)
bullet2_sound = pygame.mixer.Sound('sound/bullet2.wav')
bullet2_sound.set_volume(0.1)
get_bullet_sound = pygame.mixer.Sound('sound/getBullet.wav')
get_bullet_sound.set_volume(0.2)
bigPlane_out_sound = pygame.mixer.Sound('sound/bigPlaneOut.wav')
bigPlane_out_sound.set_volume(0.3)
bigPlane_down_sound = pygame.mixer.Sound('sound/bigPlaneDown.wav')
bigPlane_down_sound.set_volume(0.2)
middlePlane_down_sound = pygame.mixer.Sound('sound/middlePlaneDown.wav')
middlePlane_down_sound.set_volume(0.2)
smallPlane_down_sound = pygame.mixer.Sound('sound/smallPlaneDown.wav')
smallPlane_down_sound.set_volume(0.2)
myPlane_down_sound = pygame.mixer.Sound('sound/myPlaneDown.wav')
myPlane_down_sound.set_volume(0.2)
game_over_sound = pygame.mixer.Sound('sound/gameover.wav')
game_over_sound.set_volume(0.2)

#颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#添加敌方飞机函数
def add_small_planes(group1, group2, num):
    for i in range(num):
        plane = enemy.SmallPlane(bg_size)
        group1.add(plane)
        group2.add(plane)

def add_middle_planes(group1, group2, num):
    for i in range(num):
        plane = enemy.MiddlePlane(bg_size)
        group1.add(plane)
        group2.add(plane)

def add_big_planes(group1, group2, num):
    for i in range(num):
        plane = enemy.BigPlane(bg_size)
        group1.add(plane)
        group2.add(plane)

#加快敌机飞行速度
def inc_speed(tar, inc):
    for each in tar:
        each.speed += inc

def main():
    pygame.mixer.music.play(-1)
    global background

    #游戏分数
    best_score = 0
    your_score = 0
    #字体
    font = pygame.font.Font('font/font.ttf', 36)
    game_over_font = pygame.font.Font('font/font.ttf', 50)
    #生成我方飞机
    me = myPlane.MyPlane(bg_size)
    #生成敌方飞机
    enemies = pygame.sprite.Group()
    small_planes = pygame.sprite.Group()
    add_small_planes(small_planes, enemies, 15)
    middle_planes = pygame.sprite.Group()
    add_middle_planes(middle_planes, enemies, 5)
    big_planes = pygame.sprite.Group()
    add_big_planes(big_planes, enemies, 2)
    #生成子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    #生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 4
    for i in range(BULLET2_NUM):
        bullet2.append(bullet.Bullet2(me.rect.midtop))
    #全屏炸弹
    bomb_image = pygame.image.load('image/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_rect.left = 0
    bomb_rect.bottom = bg_height
    bomb_num = 3
    #玩家生命
    life_image = pygame.image.load('image/myPlaneLife.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_rect.left = bg_width // 2
    life_rect.bottom = bg_height
    life_num = 3
    #补给包
    bomb_supply = supply.BombSupply(bg_size)
    bullet_supply = supply.BulletSupply(bg_size)
    #补给包定时器，设定每30秒发放一次补给包
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
    #超级子弹定时器
    SUPPER_BULLET_TIME = USEREVENT + 1
    is_supper_bullet = False
    #我方飞机无敌定时器
    MY_PLANE_INVINCIBLE_TIME = USEREVENT + 2

    #记录飞机毁灭之后隔多久重置
    big_plane_destroy = 0
    middle_plane_destroy = 0
    small_plane_destroy = 0
    my_plane_destroy = 0
    
    #用于切换图片
    switch_image = True
    #用于延迟
    delay = 100
    #游戏暂停
    paused = False
    pause_image = pygame.image.load('image/pause.png').convert_alpha()
    pause_rect = pause_image.get_rect()
    pause_rect.left = bg_width // 2 - pause_rect.width // 2
    pause_rect.top = bg_height // 2 - pause_rect.height // 2
    #游戏难度级别
    level = 1
    #用于防止重复打开记录文件
    recorded = False
    #游戏结束后的选项及其属性
    quit_text = font.render('Quit', True, WHITE)
    again_text = font.render('Again', True, WHITE)
    quit_pos = quit_text.get_rect()
    again_pos = again_text.get_rect()
    quit_pos.left = bg_width // 3 - quit_pos.width // 2
    quit_pos.top = bg_height // 2 + 150
    again_pos.left = bg_width // 3 * 2 - again_pos.width // 2
    again_pos.top = bg_height // 2 + 150
    
    clock = pygame.time.Clock()
    running = True

    #绘制前言介绍
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                running = False

        info = pygame.image.load('image/info.jpg').convert()
        screen.blit(info, (0, 0))

        pygame.display.flip()
        clock.tick(30)

    #游戏正式开始
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            #点击鼠标游戏暂停
            elif life_num > 0 and event.type == MOUSEBUTTONDOWN:
                paused = not paused
                if paused:#暂停游戏时关闭音乐音效和补给
                    pygame.time.set_timer(SUPPLY_TIME, 0)
                    pygame.mixer.music.pause()
                    pygame.mixer.pause()
                else:#非暂停状态则重新开启资源
                    pygame.time.set_timer(SUPPLY_TIME, 30)
                    pygame.mixer.music.unpause()
                    pygame.mixer.unpause()
            #空格引爆全屏炸弹
            elif event.type == KEYDOWN and \
                 life_num > 0 and \
                 not paused:
                if event.key == K_SPACE and bomb_num > 0:
                    bomb_num -= 1
                    bomb_sound.play()
                    for each in enemies:
                        if each.rect.bottom > 0:#炸毁对象必须出现在屏幕中
                            each.is_alive = False
            #每30秒随机发放一个补给包
            elif event.type == SUPPLY_TIME:
                if random.choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            #开启超级子弹18秒后自动关闭
            elif event.type == SUPPER_BULLET_TIME:
                is_supper_bullet = False
                pygame.time.set_timer(SUPPER_BULLET_TIME, 0)
            #重生3秒后关闭无敌状态
            elif event.type == MY_PLANE_INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(MY_PLANE_INVINCIBLE_TIME, 0)
            #gameover之后玩家的选择
            elif life_num == 0 and event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                #玩家选择退出
                if mouse_pos[0] > quit_pos.left and \
                   mouse_pos[0] < quit_pos.right and \
                   mouse_pos[1] > quit_pos.top and \
                   mouse_pos[1] < quit_pos.bottom:
                    sys.exit()
                #玩家选择再玩
                if mouse_pos[0] > again_pos.left and \
                   mouse_pos[0] < again_pos.right and \
                   mouse_pos[1] > again_pos.top and \
                   mouse_pos[1] < again_pos.bottom:
                    #重设背景并播放背景音乐同时关闭gameover音效
                    background = pygame.image.load('image/background.jpg').convert()
                    pygame.mixer.stop()
                    pygame.mixer.music.play(-1)
                    #重设分数
                    your_score = 0
                    #重新生成敌机
                    enemies = pygame.sprite.Group()
                    small_planes = pygame.sprite.Group()
                    add_small_planes(small_planes, enemies, 15)
                    middle_planes = pygame.sprite.Group()
                    add_middle_planes(middle_planes, enemies, 5)
                    big_planes = pygame.sprite.Group()
                    add_big_planes(big_planes, enemies, 2)
                    #重设全屏炸弹数量及玩家生命数，重设我方飞机
                    bomb_num = 3
                    life_num = 3
                    me.reset()
                    pygame.time.set_timer(MY_PLANE_INVINCIBLE_TIME, 3000)
                    #开启补给包，超级子弹判断重设
                    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                    is_supper_bullet = False
                    #重设飞机毁灭恢复参数
                    big_plane_destroy = 0
                    middle_plane_destroy = 0
                    small_plane_destroy = 0
                    my_plane_destroy = 0
                    #其他设定
                    switch_image = True
                    delay = 100
                    paused = False
                    level = 1
                    recorded = False
        
        #根据用户得分增加游戏难度
        if level == 1 and your_score > 50000:
            level = 2
            #增加3加小型敌机，2架中型敌机，1加大型敌机
            add_small_planes(small_planes, enemies, 3)
            add_middle_planes(middle_planes, enemies, 2)
            add_big_planes(big_planes, enemies, 1)
            #增加敌机飞行速度
            inc_speed(small_planes, 1)
        elif level == 2 and your_score > 300000:
            level = 3
            #增加5加小型敌机，3架中型敌机，2加大型敌机
            add_small_planes(small_planes, enemies, 5)
            add_middle_planes(middle_planes, enemies, 3)
            add_big_planes(big_planes, enemies, 2)
            #增加敌机飞行速度
            inc_speed(small_planes, 1)
            inc_speed(middle_planes, 1)
        elif level == 3 and your_score > 600000:
            level = 4
            #增加5加小型敌机，3架中型敌机，2加大型敌机
            add_small_planes(small_planes, enemies, 5)
            add_middle_planes(middle_planes, enemies, 3)
            add_big_planes(big_planes, enemies, 2)
            #增加敌机飞行速度
            inc_speed(small_planes, 1)
            inc_speed(middle_planes, 1)
            inc_speed(big_planes, 1)
        elif level == 4 and your_score > 1000000:
            level = 5
            #增加5加小型敌机，3架中型敌机，2加大型敌机
            add_small_planes(small_planes, enemies, 5)
            add_middle_planes(middle_planes, enemies, 3)
            add_big_planes(big_planes, enemies, 2)
            #增加敌机飞行速度
            inc_speed(small_planes, 1)
            inc_speed(middle_planes, 1)
            inc_speed(big_planes, 1)

        #游戏主流程
        screen.blit(background, (0, 0))#画背景
        if life_num > 0 and not paused:
            #检测玩家键盘操作控制我方飞机方向
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_RIGHT]:
                me.moveRight()

            #若补给包存在则绘制补给包并检测玩家是否获得
            if bomb_supply.is_alive:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3: #全屏炸弹数量上限为3
                        bomb_num += 1
                    bomb_supply.is_alive = False
            if bullet_supply.is_alive:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    bullet_supply.is_alive = False
                    is_supper_bullet = True
                    pygame.time.set_timer(SUPPER_BULLET_TIME, 18 * 1000) #设定18秒后关闭
            
            #发射子弹
            if not is_supper_bullet:
                if not(delay % 10):
                    bullet1[bullet1_index].reset(me.rect.midtop)
                    bullet1_sound.play()
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM
            else:
                if not(delay % 10):
                    bullet2[bullet2_index].reset(me.rect.midtop)
                    bullet2_sound.play()
                    bullet2_index = (bullet2_index + 1) % BULLET2_NUM
            #绘制子弹并检测子弹是否击中敌机
            for b in (bullet2 if is_supper_bullet else bullet1):
                if b.is_alive:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemies_hit = \
                                pygame.sprite.spritecollide(b, enemies, False, \
                                                            pygame.sprite.collide_mask)
                    if enemies_hit:
                        b.is_alive = False
                        for e in enemies_hit:
                            e.energy -= (2 if is_supper_bullet else 1) #普通子弹伤害为1，超级子弹为2
                            if e.energy <= 0:
                                e.is_alive = False

            #绘制大型敌机
            for each in big_planes:
                each.move()
                if each.is_alive:
                    if switch_image:#切换两张图片实现闪烁效果，BOSS特效
                        screen.blit(each.image1, each.rect)
                    else:
                        screen.blit(each.image2, each.rect)
                    #绘制血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    #血量 > 20%时显示绿色，否则红色
                    energy_remain = each.energy * 1.0 / enemy.BigPlane.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                    #即将出现在画面中时播放音效
                    if each.rect.bottom >= -50:
                        bigPlane_out_sound.play(-1)#循环播放确保BOSS飞行中带有音效
                else: #毁灭
                    screen.blit(each.image1, each.rect)
                    if not(delay % 3):
                        if big_plane_destroy == 0: #确保只播放一次音效
                            bigPlane_down_sound.play()
                        screen.blit(each.destroy_image, each.rect)
                        big_plane_destroy = (big_plane_destroy + 1) % 6
                        if big_plane_destroy == 0:
                            bigPlane_out_sound.stop()#停止BOSS飞行音效
                            each.reset()
                            your_score += 10000
                    
            #绘制中型敌机
            for each in middle_planes:
                each.move()
                screen.blit(each.image, each.rect)
                #绘制血槽
                pygame.draw.line(screen, BLACK, \
                                (each.rect.left, each.rect.top - 5), \
                                (each.rect.right, each.rect.top - 5), \
                                2)
                #血量 > 20%时显示绿色，否则红色
                energy_remain = each.energy * 1.0 / enemy.MiddlePlane.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen, energy_color, \
                                (each.rect.left, each.rect.top - 5), \
                                (each.rect.left + each.rect.width * energy_remain, \
                                each.rect.top - 5), 2)
                
                if not each.is_alive:#毁灭
                    if not(delay % 3):
                        if middle_plane_destroy == 0:
                            middlePlane_down_sound.play()
                        screen.blit(each.destroy_image, each.rect)
                        middle_plane_destroy = (middle_plane_destroy + 1) % 4
                        if middle_plane_destroy == 0:
                            each.reset()
                            your_score += 5000
                        
            #绘制小型敌机
            for each in small_planes:
                each.move()
                screen.blit(each.image, each.rect)
                if not each.is_alive:#毁灭
                    if not(delay % 3):
                        if small_plane_destroy == 0:
                            smallPlane_down_sound.play()
                        screen.blit(each.destroy_image, each.rect)
                        small_plane_destroy = (small_plane_destroy + 1) % 4
                        if small_plane_destroy == 0:
                            each.reset()
                            your_score += 1000

            #检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, \
                                                       enemies, \
                                                       False, \
                                                       pygame.sprite.collide_mask)
            #若我方飞机在非无敌状态被撞，双方飞机都阵亡
            if enemies_down and not me.invincible:
                me.is_alive = False
                for each in enemies_down:
                    each.is_alive = False

            #绘制我方飞机
            if me.is_alive:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:#我方飞机毁灭
                screen.blit(me.image1, me.rect)
                if not(delay % 3):
                    if my_plane_destroy == 0:
                        myPlane_down_sound.play()
                    screen.blit(me.destroy_image, me.rect)
                    my_plane_destroy = (my_plane_destroy + 1) % 4
                    if my_plane_destroy == 0:
                        life_num -= 1
                        if life_num > 0:
                            me.reset()
                            pygame.time.set_timer(MY_PLANE_INVINCIBLE_TIME, 3000) #3秒后关闭无敌状态
        #游戏暂停
        elif paused:
            screen.blit(pause_image, pause_rect)

        if life_num > 0:#游戏正常运行
            #画出分数和难度级别
            score_text = font.render(\
                'Score: %s Level: %s' % (str(your_score), str(level)), True, WHITE)
            screen.blit(score_text, (10, 5))
            #绘制状态栏，全屏炸弹图标+数量，生命图标+数量
            screen.blit(bomb_image, bomb_rect)
            bomb_text = font.render(' X %s' % str(bomb_num), True, WHITE)
            screen.blit(bomb_text, (bomb_rect.left + bomb_rect.width, \
                                    bomb_rect.top + 20))
            screen.blit(life_image, life_rect)
            life_text = font.render(' X %s' % str(life_num), True, WHITE)
            screen.blit(life_text, (life_rect.left + life_rect.width, \
                                    life_rect.top + 20))

        if life_num == 0:#游戏结束
            #绘制gameover画面
            game_over = game_over_font.render('GAME OVER', True, WHITE)
            screen.blit(game_over, ((bg_width - game_over.get_width()) // 2, \
                                    (bg_height - game_over.get_height()) // 2))
            #关闭其他资源
            pygame.mixer.music.stop()
            pygame.time.set_timer(SUPPLY_TIME, 0)
            #记录历史最高分
            if not recorded:#确保只进行一次文件操作
                with open('record.data', 'r') as f:
                    temp = f.read()
                    if temp != '':
                        best_score = int(temp)
                if best_score < your_score:
                    best_score = your_score
                    with open('record.data', 'w') as f:
                        f.write(str(best_score))
                recorded = True
                pygame.mixer.stop() #停止其他音效
                game_over_sound.play() #顺便防止重复播放结束音乐
                #防止重复加载图片
                background = pygame.image.load('image/gameover_background.jpg').convert()
            #绘制分数，最高分和当前分数
            best_score_text = font.render('Best Score: %s' % str(best_score), True, WHITE)
            screen.blit(best_score_text, (40, 50))
            your_score_text = font.render('Your Score: %s' % str(your_score), True, WHITE)
            screen.blit(your_score_text, ((bg_width - your_score_text.get_width()) // 2, \
                                          (bg_height + game_over.get_height()) // 2 + 30))
            #绘制选择项
            screen.blit(quit_text, quit_pos)
            screen.blit(again_text, again_pos)
            #鼠标停在Quit上时字体变为红色，否则为白色
            #鼠标停在Again上时字体变为绿色，否则为白色
            mouse_pos = pygame.mouse.get_pos()
            #Quit部分
            if mouse_pos[0] > quit_pos.left and \
               mouse_pos[0] < quit_pos.right and \
               mouse_pos[1] > quit_pos.top and \
               mouse_pos[1] < quit_pos.bottom:
                quit_text = font.render('Quit', True, RED)
            else:
                quit_text = font.render('Quit', True, WHITE)

            if mouse_pos[0] > again_pos.left and \
               mouse_pos[0] < again_pos.right and \
               mouse_pos[1] > again_pos.top and \
               mouse_pos[1] < again_pos.bottom:
                again_text = font.render('Again', True, GREEN)
            else:
                again_text = font.render('Again', True, WHITE)
        #每隔5帧切换图片
        if not(delay % 5):
            switch_image = not switch_image 

        delay -= 1
        if not delay:
            delay = 100
        #显示游戏画面
        pygame.display.flip()
        #设置帧率
        clock.tick(60)

if __name__ == '__main__':
    main()
