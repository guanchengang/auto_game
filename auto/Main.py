import Check
import Frame
import Mouse

import sys
import random
from time import sleep
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])

# chest 0.6
# bossFight 0.5
# fight 0.6
# win 0.4
# chestInStart 0.85
# 选择关卡 1460 335
# 探索 1625 405
# 确认退出 965 535

# 初始化位置
# 基本点位
start_button = Point(1175, 705)
return_button = Point(60, 100)
return_button_again = Point(965, 535)
explore_button = Point(1625, 405)
'''选择关卡'''
stage_button = Point(1460, 335)

hwnd = Frame.getWindowHwndByName('MuMu模拟器')
if hwnd is None:
    print("没有目标窗口")
    sys.exit(0)
pos = Frame.getWindowRect(hwnd)
left_top = Point(pos[0], pos[1])
right_bottom = Point(pos[2], pos[3])

Frame.alert('开始')
sleep(2)

while True:
    # 进入游戏界面
    isFight = False
    if Check.diffImage(Frame.toImage('target/startFrame.png'), Frame.screenshot(hwnd)) > 0.95:
        Mouse.leftClick(
            pos=(left_top[0]+start_button[0]+random.randint(0, 10),
                 left_top[1]+start_button[1]+random.randint(0, 10)),
            duration=random.uniform(0.5, 1.5)
        )
        sleep(2)
        isFight = True
    else:
        # 领开始界面的箱子
        chestInStart_position = Check.checkInImage(
            tar_image=Frame.toImage('target/chestInStart.png'),
            image=Frame.screenshot(hwnd),
            threshold=0.85
        )
        if chestInStart_position is not None:
            # 点击箱子
            Mouse.leftClick(
                pos=(left_top[0]+chestInStart_position[0]+random.randint(-5, 5),
                     left_top[1]+chestInStart_position[1]+random.randint(-5, 5)),
                duration=random.uniform(0.5, 1.5)
            )
            sleep(1.5)
            # 确定
            Mouse.leftClick(
                pos=(right_bottom[0]-left_top[0]-random.randint(0, 50),
                     right_bottom[1]-left_top[1]-random.randint(0, 50)),
                duration=random.uniform(0.5, 1.5)
            )
            sleep(0.5)
        else:
            # 点击进入开始界面
            Mouse.leftClick(
                pos=(left_top[0]+stage_button.x+random.randint(-15, 15),
                     left_top[1]+stage_button.y+random.randint(-15, 15)),
                duration=random.uniform(0.5, 1.5)
            )
            sleep(1.5)

    while isFight:
        isBoss = True
        ready_fight = True
        # 寻找目标
        # 找boss
        click_target = Check.checkInImage(
            tar_image=Frame.toImage('target/bossFight.png'),
            image=Frame.screenshot(hwnd),
            threshold=0.5
        )
        # 找小怪
        if click_target is None:
            click_target = Check.checkInImage(
                tar_image=Frame.toImage('target/fight.png'),
                image=Frame.screenshot(hwnd),
                threshold=0.6
            )
            isBoss = False
        # 如果没有目标,把屏幕往左边拖动一段距离
        if click_target is None:
            Mouse.moveTo(
                pos=(left_top[0]+700+random.randint(0, 100),
                     left_top[1]+200+random.randint(0, 300)),
                duration=random.uniform(0.5, 1.5)
            )
            Mouse.dragTo(
                pos=(left_top[0]+100+random.randint(0, 100),
                     left_top[1]+100+random.randint(0, 300)),
                duration=random.uniform(0.5, 1.5)
            )
            ready_fight = False
        if ready_fight:
            # 点击战斗
            Mouse.leftClick(
                pos=(left_top[0]+click_target[0]+random.randint(-10, 10),
                     left_top[1]+click_target[1]+random.randint(-10, 10)),
                duration=random.uniform(0.5, 1.5)
            )
            # 战斗时间
            sleep(18)

            if Check.checkInImage(
                tar_image=Frame.toImage('target/win.png'),
                image=Frame.screenshot(hwnd),
                threshold=0.4
            ):
                Mouse.leftClick(
                    pos=(left_top[0]+(right_bottom[0]-left_top[0])//2+random.randint(50, 100),
                         left_top[1]+(right_bottom[1]-left_top[1])//2+random.randint(100, 150)),
                    duration=random.uniform(0.5, 1.5)
                )
            else:
                sleep(10)
                Mouse.leftClick(
                    pos=(left_top[0]+(right_bottom[0]-left_top[0])//2+random.randint(50, 100),
                         left_top[1]+(right_bottom[1]-left_top[1])//2+random.randint(100, 150)),
                    duration=random.uniform(0.5, 1.5)
                )
            # 此刻已经完成一次战斗
            if isBoss:
                # 等箱子跳出来
                sleep(6)
                # 捡箱子
                while True:
                    chest_position = Check.checkInImage(
                        tar_image=Frame.toImage('target/chest.png'),
                        image=Frame.screenshot(hwnd),
                        threshold=0.6
                    )
                    if chest_position is None:
                        break
                    else:
                        # 点箱子
                        Mouse.leftClick(
                            pos=(left_top[0]+chest_position[0]+random.randint(-5, 5),
                                 left_top[1]+chest_position[1]+random.randint(-5, 5)),
                            duration=random.uniform(0.5, 1.5)
                        )
                        sleep(1.5)
                        # 点击确定
                        Mouse.leftClick(
                            pos=(left_top[0]+100+random.randint(0, 400),
                                 left_top[1]+100+random.randint(0, 400)),
                            duration=random.uniform(0.5, 1.5)
                        )
                        sleep(0.5)
                # 打完boss直接退出
                sleep(3)
                # 重置战斗状态
                isFight = False
