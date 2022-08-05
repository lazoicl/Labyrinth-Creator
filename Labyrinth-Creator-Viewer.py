from turtle import *
import numpy as np
import random

# 一些常量
X = 0
Y = 1
directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

# 一些设定
width = 101  # 迷宫宽度
height = 101  # 迷宫高度
PenSize = 3  # 画笔粗细
speed(0)  # 速度最快
delay(1)  # 延迟1ms
ht()  # 隐藏turtle
bgcolor('Black')  # 背景颜色
pencolor('White')  # 画笔颜色


def CDA(map, position):
    ret = [True, True, True, True]
    for direction in range(4):
        # 判断边缘
        if not 0 <= position[X] + directions[direction][X] * 2 <= width or not 0 <= position[Y] + directions[direction][Y] * 2 <= height:
            ret[direction] = False
        # 判断下一个节点是否为黑
        elif not map[position[X] + directions[direction][X] * 2][position[Y] + directions[direction][Y] * 2] == '0':
            ret[direction] = False
    return ret


def DrawOneRoad(map, position):
    # 前往节点
    goto(PenSize * (position[X] - width / 2), PenSize * (position[Y] - height / 2))
    direction_ability = CDA(map, position)
    while not direction_ability.count(True) == 0:
        # 有方向空白则落笔
        pendown()

        # 随机选择方向
        choices = []
        for i in range(4):
            if direction_ability[i]:
                choices.append(i)
        direction = random.choice(choices)
        map[position[X] + directions[direction][X] * 1][position[Y] + directions[direction][Y] * 1] = ' '
        map[position[X] + directions[direction][X] * 2][position[Y] + directions[direction][Y] * 2] = ' '

        # 同步绘图
        PenGo = direction * 90
        seth(PenGo)
        fd(PenSize * 2)

        # 将新节点加入points数组，加速后续画分支
        points.append(list(position))

        # 刷新位置
        position[X] += 2 * directions[direction][X]
        position[Y] += 2 * directions[direction][Y]
        direction_ability = CDA(map, position)
    penup()


setup(width=500, height=500, startx=100, starty=100)
pensize(PenSize)
penup()
goto(-PenSize * width / 2, -PenSize * height / 2)

map = np.array([['0'] * width] * height)
position = [0, 0]
points = [[0, 0]]
map[position[X]][position[Y]] = ' '

for position in points:
    DrawOneRoad(map, position)

# 字符模式输出（调试用）
# for x in range(width):
#     for y in range(height):
#         print(map[x][y], end='')
#     print('')

done()
