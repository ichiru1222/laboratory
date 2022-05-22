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

def get_flies_angle(row):
    x_diff = row["pos_x_wma"].diff() -70
    y_diff = row["pos_y_wma"].diff() -70
    x2 = row["pos_x_wma"] -70
    y2 = row["pos_y_wma"] -70
    x1 = x2 - x_diff
    y1 = y2 - y_diff
    naiseki = np.inner(np.array(x1, y1), np.array(x2, y2))
    l1 = np.linalg.norm(np.array(x1, y1))
    l2 = np.linalg.norm(np.array(x2, y2))
    theta = np.arccos(naiseki/(l1 * l2))
    phi = np.arctan(y2/x2)
    return theta + phi