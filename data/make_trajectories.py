import numpy as np
import pandas as pd

import math
import glob

SP_NAME = "norpA"
FILE_NAME = f"pandas/{SP_NAME}"

def make_trajectory_vR_vtheta(row):
    state_num = 0
    d_R = row["R_verosity"]
    if d_R != 0:
        d_R = np.log10(d_R)
    
    d_theta = row["theta_verosity"]
    if d_theta != 0:
        d_theta = np.log10(d_theta)
    
    # R: 　=> 0.8 : 11個
    R_indx = 0
    for i, v in enumerate(np.arange(-4, 4, 0.8)):
        
        if d_R < v:
            R_indx = i
            break
        R_indx = i + 1
        
    # theta:  => 0.6 : 11個
    theta_indx = 0
    for i, v in enumerate(np.arange(-4, 2, 0.6)):
        if d_theta < v:
            theta_indx = i
            break
        theta_indx = i + 1
    
    
    #状態数11個バージョン
    state_num = 11 * R_indx + theta_indx
    return state_num

def make_trajectory_R_v(row):
    state_num = 0
    d_radius = row["R"]
    
    d_v = row["dist_v"]
    if d_v != 0:
        d_v = np.log10(d_v)
    
    # radius: 　0 ~ 7, 7 ~ 14, ... , 63 ~ 70  70~: 11等分
    if d_radius > 69.9:
        d_radius = 70
    radius_indx = int(d_radius // 7)
    # radius_indx = 0
    # for i, v in enumerate(np.arange(0, 70, 7)):
        
    #     if d_radius < v:
    #         radius_indx = i
    #         break
    #     radius_indx = i + 1
        
    # v(log10):  0 ~ 2
    v_indx = 0
    for i, v in enumerate(np.arange(0, 2, 0.2)):
        if d_v < v:
            v_indx = i
            break
        v_indx = i + 1
    #状態数11個バージョン
    state_num = 11 * radius_indx + v_indx
    return state_num

def make_trajectory_R_angle(row):
    state_num = 0
    d_radius = row["R"]
    
    d_angle = row["angle_diff_based"]
    
    # radius: 　0 ~ 7, 7 ~ 14, ... , 63 ~ 70  70~: 11等分

    # 壁にとても近いものは70に
    if d_radius > 69.9:
        d_radius = 70
    radius_indx = int(d_radius // 7)
        
    angle_indx = 0
    ## 12分割
    for i, v in enumerate(np.arange(-3.15, 3.15, 0.525)):
        if v < d_angle < v + 0.525:
            angle_indx = i
            break
        if d_angle <= -3.15:
            angle_indx = 11
        if d_angle >= 3.15:
            angle_indx = 0

    #self.nS1 * s2 + s1
    state_num = 11 * angle_indx + radius_indx
    return state_num

def make_trajectory_a_angle(row):
    state_num = 0
    d_acce = row["dist_v"] / row["seconds_diff"]
    d_acce = np.log10(d_acce + 0.01)
    
    d_angle = row["angle_diff_based"]

    angle_indx = 0
    ## 12分割
    for i, v in enumerate(np.arange(-3.15, 3.15, 0.525)):
        if v < d_angle < v + 0.525:
            angle_indx = i
            break
        if d_angle <= -3.15:
            angle_indx = 11
        if d_angle >= 3.15:
            angle_indx = 0
    
    ## 11分割
    # log10とって -2 4 の間
    acce_indx = int(d_acce // (6/11) + 4)
    if acce_indx >10:
        acce_indx = 10
    if acce_indx < 0:
        acce_indx = 0
    #self.nS1 * s2 + s1
    state_num = 11 * angle_indx + acce_indx
    return state_num

def make_trajectory_stimuli_a(row):
    stimuli_indx = int(row['stimuli_int'])
    d_acce = row["dist_v"] / row["seconds_diff"]
    d_acce = np.log10(d_acce + 0.01)

    # if d_stimuli == "N":
    #     stimuli_indx = 0
    # else:
    #     stimuli_indx = 1

    ## 11分割
    acce_indx = int(d_acce // (6/11) + 4)
    if acce_indx >10:
        acce_indx = 10
    if acce_indx < 0:
        acce_indx = 0
    #self.nS1 * s2 + s1
    state_num = 11 * stimuli_indx + acce_indx
    return state_num

def make_trajectory_stimuli_angle_a(row):
    stimuli_indx = int(row['stimuli_int'])
    d_acce = abs(row['angle_verosity'] / row["seconds_diff"])
    
    # 0 division 防止のため0.1たす
    d_acce = np.log10(d_acce + 0.1)
    

    # if d_stimuli == "N":
    #     stimuli_indx = 0
    # else: # stimuli = Y
    #     stimuli_indx = 1

    ## 11分割
    # log10 とって -1 5 の間
    acce_indx = int(d_acce // (6/11) + 2)
    if acce_indx >10:
        acce_indx = 10
    if acce_indx < 0:
        acce_indx = 0
    #self.nS1 * s2 + s1
    state_num = 11 * stimuli_indx + acce_indx
    return state_num
    


def cut_trajctory():
    """15秒ごとに"""
    pass

