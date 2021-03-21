# coding=UTF-8
import os, sys, time, math
import numpy as np

# 游戏算法
'''
1、根据球的两次位置确定球的方向

2、计算出球的移动速度

3、根据球方向的切线计算球的移动轨迹，根据夹角计算出距离，根据速度判断是否撞墙，撞墙的话

4、根据球的移动坐标确定球桌的宽度

5、如果不撞墙，板移动到接球位置，如果撞球，计算后撞墙后的角度，进行位置预估

'''


def get_angle(v1, v2):
    dx1 = v1[2] - v1[0]
    dy1 = v1[3] - v1[1]
    dx2 = v2[2] - v2[0]
    dy2 = v2[3] - v2[1]
    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180 / math.pi)
    # print(angle1)
    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180 / math.pi)
    # print(angle2)
    if angle1 * angle2 >= 0:
        included_angle = abs(angle1 - angle2)
    else:
        included_angle = abs(angle1) + abs(angle2)
        if included_angle > 180:
            included_angle = 360 - included_angle
    return included_angle


class MrTreeGame(object):
    INT_MIN = -sys.maxsize
    desk_x = INT_MIN
    desk_y = INT_MIN
    up_down = 0  # 0上1下

    def __init__(self):
        self.pre_x = 0
        self.pre_y = 0
        self.round = 0
        self.step = 0
        self.is_running = False
        self.first_ballx = -1

    def get_info(self, x, y):
        if self.round == 0:
            pass
        self.desk_x = max(abs(x), self.desk_x)
        self.desk_y = max(abs(y), self.desk_y)

    def compute_data(self, x, y):
        dis = math.sqrt((self.pre_x - x) * (self.pre_x - x) + (self.pre_y - y) * (self.pre_y - y))
        speed = dis / 0.5

        up_down = y < 0


    def game_run(self, ball_x, ball_y, bar_state):
        # fetch the desk size
        self.get_info(ball_x, ball_x)
        if ball_x > 0 :
            self.is_running = True
            return 'stop'
        if self.is_running or self.round== 0:
            self.first_ballx = ball_x
            if self.round  == -1:
                self.round = 0
            self.is_running = False
        
        AB = [0, 0, self.first_ballx, 0]  # 中点直线
        CD = [self.pre_x, self.pre_y, ball_x, ball_y]  # 球轨迹延伸出曲线
        angle = 90 - get_angle(AB, CD)
        
        next_y = math.sqrt(ball_x * ball_x + ball_y * ball_y) * math.sin(math.radians(90 - angle))
        if angle >= 10 and self.step < 185:
            self.step += 10
        print(self.step, angle, next_y)
        self.pre_x, self.pre_y = (ball_x, ball_x)
        self.round += 1
        # print(self.pre_x, self.pre_y)


if __name__ == "__main__":
    MrTree = MrTreeGame()
    with open('./test.dat', 'r') as f:
        data = f.readlines()
    for line in data:
        time.sleep(0.5)
        (test_x, test_y) = line.strip().split(',')
        # print(float(test_x)/float(test_y))
        MrTree.game_run(float(test_x), float(test_y), 0)
        # break

