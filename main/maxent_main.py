import sys
import pickle
import glob
import re
import time
from tqdm import tqdm

import numpy as np
sys.path.append("../env")
sys.path.append("../irl")
from maxent_env import Environment
from maxent_irl import MaxEntIRL
# print(sys.path)

"""1: SP_NAME, 2: FEATURE_NAME"""
args = sys.argv

def pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data

def pickle_dump(obj, path):
    with open(path, mode='wb') as f:
        pickle.dump(obj,f)


# norpA, DGRP324, DGRP362, DGRP517
# SP_NAME = "DGRP362"
SP_NAME = args[1]

# vR_vtheta, R_v, R_angle, a_angle, stimuli_a, stimuli_angle_a
# FEATURE_NAME = "vR_vtheta"
FEATURE_NAME = args[2]

DIR_NAME = f"../data/maxent_traj/{SP_NAME}/{FEATURE_NAME}/*.pkl"

file_names = glob.glob(DIR_NAME)
print(file_names)

env = Environment(11, 11, 4)
P = env.P

if FEATURE_NAME == "R_angle" or FEATURE_NAME == "a_angle":
    env = Environment(11, 12, 4)
    P = env.P_angle
if FEATURE_NAME == "stimuli_a" or FEATURE_NAME == "stimuli_angle_a":
    env = Environment(2, 11, 4)
    P = env.P

# 時間計測
start_experiment_time = time.time()

for file_name in tqdm(file_names):
     # pandasのファイル名 (ex no-12)
    key = re.search("no\d+-.+-\d", file_name).group()
    trajectories = pickle_load(file_name)

    reward = []
    Z_s = []

    
    

    # start trajectories[0]
    max_step_start = len(min(trajectories[0], key=len)) # 一番短い軌跡の長さを取り出す
    trajectories_start = [t[:max_step_start] for t in trajectories[0]]
    # stimu trajectories[1]
    max_step_stimu = len(min(trajectories[1], key=len))
    trajectories_stimu = [t[:max_step_stimu] for t in trajectories[1]]
    # end trajectories[2]
    max_step_end = len(min(trajectories[2], key=len))
    trajectories_end = [t[:max_step_end] for t in trajectories[2]]
    

    # 時間計測
    start_irl_time = time.time()
    R_start, policy, theta, Z_s_start = MaxEntIRL(env, P, trajectories_start, n_iter=5000, max_step=max_step_start, learning_rate=0.01)
    elapsed_irl_time  = time.time() - start_irl_time 
    print(f"elapsed IRL time (start):  {elapsed_irl_time} [sec]")

    start_irl_time = time.time()
    R_stimu, policy, theta, Z_s_stimu = MaxEntIRL(env, P, trajectories_stimu, n_iter=5000, max_step=max_step_stimu, learning_rate=0.01)
    elapsed_irl_time  = time.time() - start_irl_time 
    print(f"elapsed IRL time (stimu):  {elapsed_irl_time} [sec]")

    start_irl_time = time.time()
    R_end, policy, theta, Z_s_end = MaxEntIRL(env, P, trajectories_end, n_iter=5000, max_step=max_step_end, learning_rate=0.01)
    elapsed_irl_time  = time.time() - start_irl_time 
    print(f"elapsed IRL time (end):  {elapsed_irl_time} [sec]")

    reward.append(R_start)
    reward.append(R_stimu)
    reward.append(R_end)

    Z_s.append(Z_s_start)
    Z_s.append(Z_s_stimu)
    Z_s.append(Z_s_end)

    path_reward = f'../result/reward/{SP_NAME}/{FEATURE_NAME}/{key}.pkl'
    path_Z_s = f'../result/Z_s/{SP_NAME}/{FEATURE_NAME}/{key}.pkl'

    pickle_dump(reward, path_reward)
    pickle_dump(Z_s, path_Z_s)


elapsed_experiment_time = time.time() - start_experiment_time
print("####"*30)
print(f"elapsed experiment time:  {elapsed_experiment_time} [sec]")

# trajectories = np.array([[0, 2, 4], [1, 2, 4], [8, 2, 4]])

# R, policy, theta, Z_s = MaxEntIRL(env, trajectories, n_iter=50, max_step=len(trajectories[0]), learning_rate=0.01)
# print(R)