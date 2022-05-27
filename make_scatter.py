from turtle import circle
import numpy as np
import pandas as pd
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import patches
import pickle
import glob
import re



def pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data

# norpA, DGRP324, DGRP362, DGRP517
SP_NAME = "DGRP362"




DIR_NAME = f"data/pandas/{SP_NAME}/*.pkl"

file_names = glob.glob(DIR_NAME)
print(file_names)

def make_scatter(x, y, value, title):
    fig, ax = plt.subplots()
    c = patches.Circle(xy=(70, 70), radius=70, fill=False)
    ax.add_patch(c)
    mappable = ax.scatter(x, y,s=10, c=value, cmap=cm.jet, vmin=-2, vmax=4)
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim([0, 140])
    ax.set_ylim([0, 140])
    ax.grid(True)
    
    colb = fig.colorbar(mappable, ax=ax)
    colb.set_label("acceleration(log10)", fontsize=10)
    return plt

for file_name in file_names:
    key = re.search("no\d+-.+-\d", file_name).group()

    pd_file = pd.read_pickle(file_name)

    # 3区間に分割
    pd_file_start = pd_file.query('0<= seconds_total <= 300')
    pd_file_stimu = pd_file.query('300<= seconds_total <= 600')
    pd_file_end = pd_file.query('600<= seconds_total <= 900')

    pd_list = [pd_file_start, pd_file_stimu, pd_file_end]
    range_list = ["start", "stimu", "end"]

    for range_idx, pd_file in enumerate(pd_list):

        x = pd_file["pos_x_wma"]
        y = pd_file["pos_y_wma"]
        a = pd_file["dist_v"] / pd_file["seconds_diff"]
        a_log10 = np.log10(a + 0.01)
        print(a_log10.describe())
        title = key + range_list[range_idx]
        make_scatter(x, y, a_log10, title)
        scatter_path = f"scatter/{SP_NAME}/{range_list[range_idx]}/{key}_{range_list[range_idx]}.png"
        plt.savefig(scatter_path)
        plt.close()
        
    


