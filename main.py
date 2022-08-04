from PIL import Image
import numpy as np
import random

directions = [[0, -1], [0, 1], [-1, 0], [1, 0]]
width = 101
height = 101
A = np.array([128, 128, 128])
B = np.array([0, 0, 0])
W = np.array([255, 255, 255])
G = np.array([0, 255, 0])
R = np.array([255, 0, 0])


def CDA(map, position):
    ret = [True, True, True, True]
    x = position[0]
    y = position[1]
    for direction in range(4):
        if not 0 <= x + directions[direction][0] * 2 <= width or not 0 <= y + directions[direction][1] * 2 <= height:
            ret[direction] = False
        elif not map[x + directions[direction][0] * 1][y + directions[direction][1] * 1].all() == B.all():
            ret[direction] = False
        elif not map[x + directions[direction][0] * 2][y + directions[direction][1] * 2].all() == B.all():
            ret[direction] = False
    return ret


def DrawOneRoad(data, position):
    direction_ability = CDA(data, position)
    while not direction_ability.count(True) == 0:
        choices = []
        for i in range(4):
            if direction_ability[i]:
                choices.append(i)
        direction = random.choice(choices)
        data[position[0] + directions[direction][0] * 1][position[1] + directions[direction][1] * 1] = A
        data[position[0] + directions[direction][0] * 2][position[1] + directions[direction][1] * 2] = W
        points.append(list(position))
        # 刷新位置及四方通达性
        position[0] += 2 * directions[direction][0]
        position[1] += 2 * directions[direction][1]
        direction_ability = CDA(data, position)


def IsEnd(map, position):
    IsWhite = [True, True, True, True]
    x = position[0]
    y = position[1]
    for direction in range(4):
        if 0 <= x + directions[direction][0] <= width - 1 and 0 <= y + directions[direction][1] <= height - 1:
            if not map[x + directions[direction][0]][y + directions[direction][1]].all() == W.all():
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
data[position[0]][position[1]] = W

direction_ability = CDA(data, position)
for position in points:
    DrawOneRoad(data, position)

for x in range(width):
    for y in range(height):
        if data[x][y].all() == A.all():
            data[x][y] = W

data[0][0] = G
data = SetEnd(data)

Image.fromarray(data).show()
