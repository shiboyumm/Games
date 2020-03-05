#!/usr/local/bin/python3.7
# -*- coding:utf-8 -*-
import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)

# 刷新的帧率
FRAME_PER_SEC = 60

# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT

# 创建英雄发射子弹的定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""
    def __init__(self, image_name, speed=1):
        # 继承父类的初始化方法
        super().__init__()
        # 定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed

class Background(GameSprite):
    """游戏背景精灵"""
    def __init__(self, is_alt=False):
        # 调用父类方法实现创建背景精灵
        super().__init__("./images/background.png")
        # 判断是否为交替图像, 如果是,需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        # 调用父类方法实现 在屏幕上移动
        super().update()

        # 判断是否移出屏幕, 如果是, 将图像设置到屏幕的上方
        if self.rect.y >=  SCREEN_RECT.height:
            self.rect.y = -self.rect.height

class Enumy(GameSprite):
    """敌机精灵"""
    def __init__(self):
        # 调用父类初始方法创建敌机精灵
        super().__init__("./images/enemy1.png")
        # 指定敌机随机速度
        self.speed = random.randint(1, 3)
        # 这样敌机不会出现的特别突兀
        self.rect.bottom = 0
        # 指定敌机初始位置为随机
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        # 调用父类 update 方法
        super().update()
        # 如果敌机的 y 值大于屏幕的 height, 那么就把敌机从敌机精灵组里删除
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()

class Hero(GameSprite):
    """英雄飞机"""
    def __init__(self):
        # 调用父类的初始化方法, 设置英雄精灵的图片和 speed
        super().__init__("./images/me1.png", 0)
        # 设置英雄初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 使英雄飞机在水平方向移动
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_RECT.right:
            self.rect.x = SCREEN_RECT.right

    def fire(self):
        print("发射子弹")

        for i in (0, 1, 2):
            # 创建子弹精灵
            bullet = Bullet()
            # 指定子弹精灵位置, 与英雄同centerx, 在英雄正上方有一定距离
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # 将子弹精灵加入精灵组
            self.bullets.add(bullet)

class Bullet(GameSprite):
    """子弹类"""
    def __init__(self):
        # 调用父类初始化方法, 指定子弹图片, 指定子弹初始速度
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        # 调用父类方法, 让子弹沿垂直飞行
        super().update()
        # 判断子弹是否飞出屏幕, 如果飞出, 从精灵组中删除
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁...")
