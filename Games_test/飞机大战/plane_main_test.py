#!/usr/local/bin/python3.7
# -*- coding:utf-8 -*-
from 飞机大战.plane_sprites_test import *
import pygame

class PlaneGame(object):
    def __init__(self):
        print("游戏初始化")
        # 1. 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        # 2. 创建游戏时钟
        self.clock = pygame.time.Clock()

        # 3. 调用私有方法, 创建精灵和精灵组
        self.__create_sprites()

        # 4. 设置定时器事件, 创建敌机 - 1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)

        # 5. 设置定时器事件, 创建子弹 - 0.5s
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(is_alt=True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机精灵和精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄精灵和英雄精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("游戏开始...")
        while True:
            # 1. 设置游戏刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2. 设置事件监听
            self.__event_handler()

            # 3. 设置碰撞检测
            self.__check_collide()

            # 4. 更新/绘制精灵组
            self.__update_sprites()

            # 5. 更新屏幕显示
            pygame.display.update()

    def __event_handler(self):
        # 设置事件监听
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                print("敌机精灵来袭...")
                # 创建敌机精灵
                enumy = Enumy()
                # 将敌机精灵添加到精灵组
                self.enemy_group.add(enumy)

            # 英雄发射子弹
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

            # 使用键盘提供的方法获取键盘按键
            keys_pressed = pygame.key.get_pressed()
            # 判断元组中对应的按键索引值, 如果为对应的按键, 就将速度+2或-2
            if keys_pressed[pygame.K_RIGHT]:
                self.hero.speed = 2
            elif keys_pressed[pygame.K_LEFT]:
                self.hero.speed = -2
            # 如果是对应按键, 英雄就会发射子弹
            #elif keys_pressed[pygame.K_UP]:
            #    print("英雄开火...")
                #self.hero.fire()
            else:
                self.hero.speed = 0

    def __check_collide(self):
        # 设置碰撞检测
        # 1. 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, dokilla=True, dokillb=True)
        # 2. 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, dokill=True)
        # 判断精灵列表长度, 如果有内容, 杀死英雄, 游戏结束
        if len(enemies) > 0:
            self.hero.kill()
            PlaneGame.__game_over()

    def __update_sprites(self):
        # 更新/绘制背景精灵组
        self.back_group.update()
        self.back_group.draw(self.screen)

        # 更新/绘制敌机精灵组
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        # 更新/绘制英雄精灵组
        self.hero_group.update()
        self.hero_group.draw(self.screen)

        # 更新/绘制子弹精灵组
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        # 游戏结束
        print("游戏结束...")
        pygame.quit()
        exit()

if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()

    # 启动游戏
    game.start_game()

