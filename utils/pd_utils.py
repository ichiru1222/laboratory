"""pandas化の際に特徴量をカラムに作成
"""

import numpy as np
import math

#極座標を計算する関数

def get_R(row):
    x = row["pos_x_wma"] - 70 
    y = row["pos_y_wma"] - 70
    return math.sqrt(x**2 + y**2)

def get_theta(row):
    x = row["pos_x_wma"] - 70 
    y = row["pos_y_wma"] - 70
    rad = math.atan2(y, x)
    degree = math.degrees(rad)
    return rad

def get_dist_V(row):
    dist = row["travelled_dist_diff"]
    second = row["seconds_diff"]
    return dist / second

def get_R_verosity(row):
    diff = row["diff_R"]
    second = row["seconds_diff"]
    return diff / second

def get_theta_verosity(row):
    diff = row["diff_theta"]
    second = row["seconds_diff"]
    return diff / second
