import numpy as np
import pandas as pd
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pickle
import glob
import re

from utils.angle_plot_util import make_angle_plot

def pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data

# norpA, DGRP324, DGRP362, DGRP517
SP_NAME = "norpA"

# vR_vtheta, R_v, R_angle, a_angle
FEATURE_NAME = "a_angle"

# reward, Z_s
REWARD_Zs = "reward"

if REWARD_Zs == "reward":
    feature = "Reward"
else:
    feature = "State Value"


DIR_NAME = f"result/{REWARD_Zs}/{SP_NAME}/{FEATURE_NAME}/*.pkl"

file_names = glob.glob(DIR_NAME)
print(file_names)

for file_name in file_names:
     # pandasのファイル名 (ex no-12)
    key = re.search("no\d+-.+-\d", file_name).group()

    rewards = pickle_load(file_name)
    save_dir_path_start = f"plot/{REWARD_Zs}/{SP_NAME}/{FEATURE_NAME}/start/{key}_start.png"
    save_dir_path_stimu = f"plot/{REWARD_Zs}/{SP_NAME}/{FEATURE_NAME}/stimu/{key}_stimu.png"
    save_dir_path_end = f"plot/{REWARD_Zs}/{SP_NAME}/{FEATURE_NAME}/end/{key}_end.png"

    reward_start = rewards[0]
    reward_stimu = rewards[1]
    reward_end = rewards[2]
    
    
    plot_start = make_angle_plot(reward_start, key, feature, FEATURE_NAME)
    
    plot_start.savefig(save_dir_path_start)
    plt.close()
    
    plot_stimu = make_angle_plot(reward_stimu, key, feature, FEATURE_NAME)
    plot_stimu.savefig(save_dir_path_stimu)
    plt.close()

    plot_end = make_angle_plot(reward_end, key, feature, FEATURE_NAME)
    plot_end.savefig(save_dir_path_end)
    plt.close()
    
    
    
    
    
    
    
