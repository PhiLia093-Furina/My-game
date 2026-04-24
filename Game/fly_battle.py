import pygame
from pygame.locals import *
import sys
import random


WIN_W = 1280
WIN_H = 720
BLOCK_SIZE = 40

ground_list = []
wall_pos_list = []
enemy_list = [(BLOCK_SIZE*31, BLOCK_SIZE*1), (BLOCK_SIZE*31, BLOCK_SIZE*4), (BLOCK_SIZE*31,  BLOCK_SIZE*7), 
              (BLOCK_SIZE*31, BLOCK_SIZE*10), (BLOCK_SIZE*31, BLOCK_SIZE*13), (BLOCK_SIZE*31, BLOCK_SIZE*16)]



def ground():
        # ---------------------- 1. 外框完整围墙 ----------------------
    # 顶部
    for x in range(0, WIN_W, BLOCK_SIZE):
        ground_list.append((x, -40))
    # 底部
    for x in range(0, WIN_W, BLOCK_SIZE):
        ground_list.append((x, WIN_H))
    # 左侧
    for y in range(0, WIN_H , BLOCK_SIZE):
        ground_list.append((-40, y))
    # 右侧
    for y in range(0, WIN_H, BLOCK_SIZE):
        ground_list.append((WIN_W , y))

class bullet(pygame.sprite.Sprite):
    def __init__(self, location, dirt):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill("#42F13C")
        # 获取图片rect区域
        self.rect = self.image.get_rect(center = location )
        self.direct =  dirt
        pass

class player(pygame.sprite.Sprite):
    def __init__(self, location, filename = None):
        pygame.sprite.Sprite.__init__(self)
        self.pos = location 
        img = pygame.image.load(filename)
        self.image = pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = location

        self.Direction = [0, 1]
        self.shoot_cd = 0        # 射击冷却
        self.score = 0

    def shot(self):

        self.shoot_cd += 1
        if self.shoot_cd < 1:
            return
        self.shoot_cd = 0

        Bullet = bullet(self.rect.center, self.Direction)
        bullet_group.add(Bullet)

    def update_bullets(self):

        for b in bullet_group:
            b.rect.move_ip(b.direct)
        hits1 = pygame.sprite.groupcollide(bullet_group, wall_group, True, False)
        # if hits :
        #     print("撞墙")
        hits2 = pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)
        if hits2:
            print("命中")
            self.score += 1
        hits3 = pygame.sprite.groupcollide(bullet_group, enemy_bullet_group, True, True)

        hits4 = pygame.sprite.spritecollide(bos, bullet_group, True)

        if hits4:
            bos.life -= 1
        pass

class enemy(pygame.sprite.Sprite):
    #定义构造函数
    def __init__(self, location, filename = None):
        # 调父类来初始化子类
        pygame.sprite.Sprite.__init__(self)
        # 加载图片
        if filename!=None:
            img = pygame.image.load(filename)
            self.image = pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))
        else:
        # 获取图片rect区域
            self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            self.image.fill("#E01F1F")
        # 获取图片rect区域
        self.rect = self.image.get_rect()
        # 设置位置
        self.rect.topleft = location

        self.move_cd = 0
        self.shot_cd = 0
        self.now_dir = (-BLOCK_SIZE/10, 0)

    def update(self):

        self.move_cd += 1
        # 每 15 帧走一格，速度适中
        if self.move_cd < 20:
            return
        self.move_cd = 0
        dx, dy = self.now_dir
        # 1. 先预判下一个位置
        self.rect.x += dx
        self.rect.y += dy
        # 2. 检测是否撞墙
        hit_wall = pygame.sprite.spritecollide(self, wall_group, False)
        hit_self = pygame.sprite.spritecollide(self, enemy_group, False)

        if hit_wall :
            self.kill()

        if len(hit_self) > 1:
            direct = random.choice([(0, -BLOCK_SIZE), (0, BLOCK_SIZE)])
            self.rect.move_ip(direct)

    def enemy_shot(self):

        self.shot_cd += 1
        if self.shot_cd < 10:
            return
        self.shot_cd = 0
        sign = random.randint(1, 100)
        if sign < 2:
            Bullet = bullet(self.rect.center, [-2, 0])
            enemy_bullet_group.add(Bullet)

class boss(pygame.sprite.Sprite):
    def __init__(self, filename = None):
        # 调父类来初始化子类
        pygame.sprite.Sprite.__init__(self)
        self.life = 20
        # 加载图片
        if filename!=None:
            img = pygame.image.load(filename)
            self.image = pygame.transform.scale(img, (BLOCK_SIZE*2, BLOCK_SIZE*2))
        else:
        # 获取图片rect区域
            self.image = pygame.Surface((BLOCK_SIZE*2, BLOCK_SIZE*2))
            self.image.fill("#0FFFA3")
        # 获取图片rect区域
        self.rect = self.image.get_rect()
        # 设置位置
        self.rect.topleft = BLOCK_SIZE*29, BLOCK_SIZE*13

        self.move_cd = 0
        self.shot_cd = 0


    def update(self):

        self.move_cd += 1
        # 每 15 帧走一格，速度适中
        if self.move_cd < 30:
            return
        self.move_cd = 0
        dx, dy = random.choice([(0, BLOCK_SIZE/5), (0, -BLOCK_SIZE/5)])
        # 1. 先预判下一个位置
        old_x = self.rect.x
        old_y = self.rect.y
        self.rect.x += dx
        self.rect.y += dy
        # 2. 检测是否撞墙
        hit_wall = pygame.sprite.spritecollide(self, wall_group, False)

        if hit_wall :
            self.rect.x = old_x
            self.rect.y = old_y

    def enemy_shot(self):

        self.shot_cd += 1
        if self.shot_cd < 8:
            return
        self.shot_cd = 0
        sign = random.randint(1, 100)
        if sign < 2:
            Bullet = bullet(self.rect.center, [-2, 0])
            enemy_bullet_group.add(Bullet)

class board_wall(pygame.sprite.Sprite):
    #定义构造函数
    def __init__(self, location, img = None):
        # 调父类来初始化子类
        pygame.sprite.Sprite.__init__(self)
        # 获取图片rect区域
        if img!=None:
            
            self.image = pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))
        else:
        # 获取图片rect区域
            self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
        # 获取图片rect区域
        self.rect = self.image.get_rect()
        # 设置位置
        self.rect.topleft = location

def update_enemy_bullets():
    for b in enemy_bullet_group:
        b.rect.move_ip(b.direct)
    pygame.sprite.groupcollide(enemy_bullet_group, wall_group, True, False)
    hits = pygame.sprite.groupcollide(enemy_bullet_group, play_group, True, False)
    for b, play in hits.items():
        for p in play:
            p.rect.topleft = p.pos

def update_coliision():
    collide_p_to_e = pygame.sprite.groupcollide(play_group, enemy_group, False, True)
    collide_p_to_b = pygame.sprite.spritecollide(bos, play_group, False)
    if collide_p_to_e :
        for play, en in collide_p_to_e.items():
            play.rect.topleft = play.pos

    if collide_p_to_b:
        for play in collide_p_to_b:
            play.rect.topleft = play.pos

def check_player_collision(player_id, site):

    if site == [0, 0]:
        return 
    
    collide_wall = pygame.sprite.spritecollide(player_id, wall_group, False)
    
    if collide_wall:
        back = [-site[0], -site[1]]
        player_id.rect.move_ip(back)
        return 

def update():
    
    # main_win.blit(main_bg, (0,0))
    main_win.fill("#08AFFC")
    wall_group.draw(main_win)
    update_coliision()

    enemy_group.draw(main_win)
    enemy_group.update()
    main_win.blit(bos.image, bos.rect)
    bos.update()
    enemy_bullet_group.update()
    enemy_bullet_group.draw(main_win)

    bullet_group.update()    # 子弹逻辑更新
    bullet_group.draw(main_win)
    play_group.draw(main_win)

    
    player1.update_bullets()
    update_enemy_bullets()

    main_win.blit(p1_text, p1_text_rect)
    main_win.blit(p2_text, p2_text_rect)

def game_over():
    sign = 0
    while True:
        sucess_text , suc_text_rect = txt(f"恭喜通关\n点击鼠标继续游玩", (470,350), "#FF0000")
        # main_win.blit(main_bg, (0,0))
        main_win.fill("#08AFFC")
        wall_group.draw(main_win)
        enemy_group.draw(main_win)
        enemy_bullet_group.update()
        enemy_bullet_group.draw(main_win)

        play_group.draw(main_win)
        update_enemy_bullets()
        main_win.blit(sucess_text, suc_text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sign = 1
                break
        if sign ==1:
            break
    bos.life = 20
    main_win.blit(bos.image, bos.rect)

def fit_line(p1, p2):

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and y1 == y2:
            return 0, 0, 0
    # 水平方向（x变化大）—— 用 y = ax + b
    if abs(x1 - x2) >= abs(y1 - y2):
        if x1 == x2:  # 防止除0
            return 0, -1, y1
        a = (y1 - y2) / (x1 - x2)
        b = y1 - a * x1
        return a, -1, b

    # 垂直方向（y变化大）—— 用 x = ay + b（必须补！否则返回None）
    else:
        if y1 == y2:  # 防止除0
            return -1, 0, x1
        a = (x1 - x2) / (y1 - y2)
        b = x1 - a * y1
        return -1, a, b

def mouse_move(obj, site2):

    x1, y1 = obj.rect.topleft
    x2, y2 = site2
    A, B, C = fit_line(obj.rect.topleft, site2)
    x, y = 0, 0

    if abs(x1 - x2) >= abs(y1 - y2):
        if x2 > x1:
            for x in range(x1, x2+1, 1):
                y = A*x + C
                # main_win.blit(main_bg, (0, 0))
                main_win.fill("#08AFFC")
                main_win.blit(obj.image, (int(x), int(y)))
                pygame.display.flip()
                pygame.time.delay(3)
                
        elif x2 < x1:
            for x in range(x1, x2-1, -1):
                y = A*x + C
                # main_win.blit(main_bg, (0, 0))
                main_win.fill("#08AFFC")
                main_win.blit(obj.image, (int(x), int(y)))
                pygame.display.flip()
                pygame.time.delay(3)
    else:
        if y2 > y1:
            for y in range(y1, y2+1, 1):
                x = B*y + C
                # main_win.blit(main_bg, (0, 0))
                main_win.fill("#08AFFC")
                main_win.blit(obj.image, (int(x), int(y)))
                pygame.display.flip()
                pygame.time.delay(3)
                
        elif y2 < y1:
            for y in range(y1, y2-1, -1):
                x = B*y + C
                # main_win.blit(main_bg, (0, 0))
                main_win.fill("#08AFFC")
                main_win.blit(obj.image, (int(x), int(y)))
                pygame.display.flip()
                pygame.time.delay(3)
        
    obj.rect = obj.rect.move((int(x2-x1), int(y2-y1)))

def key_move(event):

    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
        site1 = [0, 0]
        if event.key == pygame.K_UP:
            site1[1] -= BLOCK_SIZE
        if event.key == pygame.K_DOWN:
            site1[1] += BLOCK_SIZE
        if event.key == pygame.K_LEFT:
            site1[0] -= BLOCK_SIZE
        if event.key == pygame.K_RIGHT:
            site1[0] += BLOCK_SIZE
        player1.rect.move_ip(site1)
        if site1[0] != 0 or site1[1] != 0:
            player1.Direction = [site1[0] // 8, site1[1] // 8]
        check_player_collision(player1, site1)

    if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:    
        site2 = [0, 0]
        if event.key == pygame.K_w:
            site2[1] -= BLOCK_SIZE
        if event.key == pygame.K_s:
            site2[1] += BLOCK_SIZE
        if event.key == pygame.K_a:
            site2[0] -= BLOCK_SIZE
        if event.key == pygame.K_d:
            site2[0] += BLOCK_SIZE

        player2.rect.move_ip(site2)
        if site2[0] != 0 or site2[1] != 0:
            player2.Direction = [site2[0] // 10, site2[1] // 10]
        check_player_collision(player2, site2)

def bg_resize(size):
    global main_bg
    # main_bg = pygame.image.load("image/1776353230989.png").convert()
    # main_bg = pygame.transform.scale(main_bg, size)
    main_win.fill("#08AFFC")
    #标题
    pygame.display.set_caption("PhiLia093")

def txt(title, location, rgb):
    
    text = f.render(title, True, rgb)
    textRect = text.get_rect()
    textRect.topleft = location
    return text, textRect

main_bg = None

if __name__ == "__main__":

    pygame.init()
    f = pygame.font.Font('C:/Windows/Fonts/simhei.ttf',25)
    #窗口大小
    main_win = pygame.display.set_mode((WIN_W, WIN_H), flags = pygame.RESIZABLE)
    
    bg_resize((WIN_W, WIN_H))
    #玩家人物
    play_group = pygame.sprite.Group()
    player1 = player((BLOCK_SIZE*2, BLOCK_SIZE*3), "config/ico.png")
    player2 = player((BLOCK_SIZE*1, BLOCK_SIZE*1), "config/ico2.png")
    play_group.add(player1, player2)

    bullet_group = pygame.sprite.Group()

    enemy_group = pygame.sprite.Group()
    for pos in enemy_list:
        e = enemy(pos)
        enemy_group.add(e)
        break

    bos = boss("config/boss.jpg")

    enemy_bullet_group = pygame.sprite.Group()

    ground()
    wall_group = pygame.sprite.Group()
    for grd in ground_list:
        w = board_wall(grd)
        wall_group.add(w)


    
    clock = pygame.time.Clock()
    while True:
        p1_text, p1_text_rect = txt(f"玩家1得分:{player1.score}", (0,0), "#FC0808")
        p2_text, p2_text_rect = txt(f"玩家2得分:{player2.score}", (1100,0), "#EE2207")

        if player1.score >= 100 or player2.score >= 100 or bos.life == 0:
                player1.score = 0
                player2.score = 0
                game_over()
        print(bos.life)
        clock.tick(60)
        for e in enemy_group:
            e.enemy_shot()
            bos.enemy_shot()

        if len(enemy_group)<6 and random.randint(1,10)<2:
            pos = random.choice(enemy_list)
            w = enemy(pos)
            enemy_group.add(w)

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                bg_resize(event.size)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print("按下左键")
                mouse_move(player1, event.pos)

            if event.type == pygame.KEYDOWN:

                key_move(event)
                if event.key == pygame.K_SPACE:
                    player1.shot()
                if event.key == pygame.K_j:
                    player2.shot()

        # key_move()
        pygame.sprite.spritecollide
        update()
        pygame.display.flip()