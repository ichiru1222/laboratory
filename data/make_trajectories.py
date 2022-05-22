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
    
    # radius: 　0 ~ 70
    radius_indx = 0
    for i, v in enumerate(np.arange(0, 70, 7)):
        
        if d_radius < v:
            radius_indx = i
            break
        radius_indx = i + 1
        
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
    
    # radius: 　0 ~ 70
    radius_indx = 0
    for i, v in enumerate(np.arange(0, 70, 7)):
        
        if d_radius < v:
            radius_indx = i
            break
        radius_indx = i + 1
        
    
    angle_indx = 0
    ## 12分割
    for i, v in enumerate(np.arange(-3.15, 3.15, 0.525)):
        if d_angle < v:
            angle_indx = i
            break
        angle_indx = i + 1
    #状態数11個バージョン
    state_num = 10 * radius_indx + angle_indx
    return state_num

def cut_trajctory():
    """15秒ごとに"""
    pass

