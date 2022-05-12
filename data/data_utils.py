import pickle
import numpy as np
import math
import shelve

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


"""15秒おきに20回刺激"""
def get_stimulation(row):
    diff = row["seconds_total"]
    if diff <= 300:
        return 0
    elif diff >= 600:
        return 5
    
    if 300 < diff <= 375:
        return 1
    elif 375 < diff <= 450:
        return 2
    elif 450 < diff <= 525:
        return 3
    else:
        return 4
    
def make_trajectory(row):
    state_num = 0
    d_R = row["R_verosity"]
    if d_R != 0:
        d_R = np.log10(d_R)
    
    d_theta = row["theta_verosity"]
    if d_theta != 0:
        d_theta = np.log10(d_theta)
    
    stimu = row["stimulation"]
    
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
    state_num = 121 * stimu + 11 * R_indx + theta_indx
    return state_num

def make_trajectory2(row):
    state_num = 0
    d_radius = row["R"]
    
    
    d_v = row["dist_v"]
    if d_v != 0:
        d_v = np.log10(d_v)
    
    stimu = row["stimulation"]
    
    # radius: 0 ~ 70
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
    state_num = 121 * stimu + 11 * radius_indx + v_indx
    return state_num

def make_prob(df):
    nS1 = 11 # v_R or R
    nS2 = 11 # v_theta or v
    nS3 = 6 # stimu
    nA1 = 21
    nA2 = 21

    nS = nS1 * nS2 * nS3
    nA = nA1 * nA2

    P = np.zeros((nS, nA, nS))

    traj_diff = df["trajectory"].diff()
    

if __name__ == "__main__":
    with open('datas.pickle', 'rb') as datas:
        s = pickle.load(datas)
        print(set(s["sp_list"]))
        min_dic = {}
        for sp in set(s["sp_list"]):
            t_min = 1000000
            for t in s[sp]:
                
                if len(t) > 0 and len(t) < t_min :
                    t_min = len(t)
                    min_dic[sp] = t_min
                    
        print(min_dic)
        print(len(min_dic))
        print(s)   