import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pickle

def pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data

def min_max(x, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    result = (x-min)/(max-min)
    return result

reward = pickle_load("no1-norpA-1-2.pkl")

def make_angle_plot(reward, title: str, feature_name:str, f): # f: a_angle or R_angle
    theta = np.linspace(0, 2*np.pi, 12) 
    r = np.linspace(0, 70, 11)
    if f == "a_angle":
        r = np.linspace(0, 10, 11)

    tt, rr = np.meshgrid(theta,r)
    z = reward.reshape((11, 12))
    # z = min_max(reward[2].reshape((11, 12)))
    z = np.flipud(z)
    print(z)
    fig = plt.figure()

    # ax = plt.subplot(111, polar=True)
    ax = fig.add_subplot(111, polar=True)

    # ax.set_theta_direction(-1)
    # ax.set_theta_zero_location("E")
    ax.set_title(title)
    ax.set_rgrids(r, angle=60., fontname="Arial", fontsize=6)
    theta_labels = ("270°","300°","330°","0°","30°","60°","90°","120°","150°","180°","210°","240°",)
    ax.set_thetagrids(range(0, 360, 30), labels=theta_labels, fontsize=8)
    ctf = plt.contourf(tt, rr, z, 100, cmap=cm.jet)
    colb = plt.colorbar(pad=0.08)
    colb.set_label(feature_name, fontname="Arial", fontsize=10)

    return plt

if __name__ == "__main__":
    make_angle_plot(reward[0], title="test", feature_name="test", f="a").show()