from PIL import Image
import numpy as np
import random

# 一些常量：
directions = [[0, -1], [0, 1], [-1, 0], [1, 0]]
X = 0
Y = 1
width = 51                                          # 默认宽度
height = 51                                         # 默认高度
A = np.array([128, 128, 128])                       # Gray (中间色)
B = np.array([0, 0, 0])                             # Black
W = np.array([255, 255, 255])                       # White
G = np.array([0, 255, 0])                           # Green
R = np.array([255, 0, 0])                           # Red


def CDA(map, position):
    ret = [True, True, True, True]
    for direction in range(4):
        # 判断边缘
        if not 0 <= position[X] + directions[direction][X] * 2 <= width or not 0 <= position[Y] + directions[direction][Y] * 2 <= height:
            ret[direction] = False
        # 判断下一个节点是否为黑
        elif not map[position[X] + directions[direction][X] * 2][
                     position[Y] + directions[direction][Y] * 2].all() == B.all():
            ret[direction] = False
    return ret


def DrawOneRoad(map, position):
    direction_ability = CDA(map, position)
    while not direction_ability.count(True) == 0:
        choices = []
        for i in range(4):
            if direction_ability[i]:
                choices.append(i)
        direction = random.choice(choices)
        map[position[X] + directions[direction][X] * 1][position[Y] + directions[direction][Y] * 1] = W
        map[position[X] + directions[direction][X] * 2][position[Y] + directions[direction][Y] * 2] = W
        points.append(list(position))
        # 刷新位置
        position[X] += 2 * directions[direction][X]
        position[Y] += 2 * directions[direction][Y]
        direction_ability = CDA(map, position)


def IsEnd(map, position):
    IsWhite = [True, True, True, True]
    for direction in range(4):
        if not (0 <= position[X] + directions[direction][X] <= width - 1 and 0 <= position[Y] + directions[direction][Y] <= height - 1):
            IsWhite[direction] = False
        elif not map[position[X] + directions[direction][X]][position[Y] + directions[direction][Y]].all() == W.all():
            IsWhite[direction] = False
    if IsWhite.count(True) == 1:
        return True
    else:
        return False


def SetEnd(map):
    for x in range(width - 1, 0, -2):
        for y in range(height - 1, 0, -2):
            if IsEnd(map, [x, y]):
                map[x][y] = R
                return map
    return map


data = np.array(Image.new(mode='RGB', size=(width, height)))
position = [0, 0]
points = [[0, 0]]
data[position[X]][position[Y]] = W

for position in points:
    DrawOneRoad(data, position)

data[0][0] = G
data = SetEnd(data)

Image.fromarray(data).show()
