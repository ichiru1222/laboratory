import numpy as np
import pandas as pd

import re
import glob
import pickle

from data.make_trajectories import make_trajectory_vR_vtheta, make_trajectory_R_v, make_trajectory_R_angle, make_trajectory_a_angle, make_trajectory_stimuli_a, make_trajectory_stimuli_angle_a

"""軌跡を３次元リストに
    1次元： 0, 1, 2 -> 0~300s, 300~600s, 600~900s
"""


SP_NAME = "DGRP324"
DIR_NAME = f"data/pandas/{SP_NAME}/*.pkl"

file_names = glob.glob(DIR_NAME)

print(file_names)

def make_traj(pd, stimu_time, column: str, indx: int):
    s_time = pd.index[0]
    # stimu_time = pd.Timedelta(seconds=15)
    traj = pd[(pd.index >= s_time + stimu_time * indx) & (pd.index <= s_time + stimu_time * (indx + 1))][column]
    return traj
def make_stimu_columm(pd):
    stimu_time = 0.5
    stimu_range = 15
    stimu_start = 300
    for i in range(20):
        start = i * stimu_range + stimu_start
        end = start + stimu_time
        pd["stimuli_int"][(pd["seconds_total"] >= start) & (pd["seconds_total"] <= end)] = 1
        # print(pd["stimuli_int"].describe())
    return pd

def pickle_dump(obj, path):
    with open(path, mode='wb') as f:
        pickle.dump(obj,f)

for file_name in file_names:
     # pandasのファイル名 (ex no-12)
    key = re.search("no\d+-.+-\d", file_name).group()

    pd_file = pd.read_pickle(file_name)
    pd_file["time_index"] = pd.to_datetime(pd_file["seconds_total"], unit="s")

    pd_file = pd_file.replace({"N": 1, "Y":2})



    # ダウンサンプリング
    pd_file = pd_file.set_index("time_index")
    pd_file = pd_file.resample("100L").mean()
    pd_file = pd_file.dropna()
    pd_file["stimuli_int"] = 0
    pd_file = make_stimu_columm(pd_file)
    
    # print(pd_file.query('314<= seconds_total <= 600')["stimuli_int"].head(30))
    # 特徴量の追加
    pd_file["traj_R_angle"] = pd_file.apply(make_trajectory_R_angle, axis=1)
    pd_file["traj_vR_vtheta"] = pd_file.apply(make_trajectory_vR_vtheta, axis=1)
    pd_file["traj_R_v"] = pd_file.apply(make_trajectory_R_v, axis=1)
    pd_file["traj_a_angle"] = pd_file.apply(make_trajectory_a_angle, axis=1)
    pd_file["traj_stimuli_a"] = pd_file.apply(make_trajectory_stimuli_a, axis=1)
    pd_file["traj_stimuli_angle_a"] = pd_file.apply(make_trajectory_stimuli_angle_a, axis=1)

    

    
    
    # 3区間に分割
    pd_file_start = pd_file.query('0<= seconds_total <= 300')
    pd_file_stimu = pd_file.query('300<= seconds_total <= 600')
    pd_file_end = pd_file.query('600<= seconds_total <= 900')

    # 3区間の軌跡を格納
    trajectories_vR_vtheta = []
    trajectories_R_v = []
    trajectories_R_angle = []
    trajectories_a_angle = []
    trajectories_stimuli_a = []
    trajectories_stimuli_angle_a = []

    trajs_vR_vtheta_start = []
    trajs_vR_vtheta_stimu = []
    trajs_vR_vtheta_end = []

    trajs_R_v_start = []
    trajs_R_v_stimu = []
    trajs_R_v_end = []

    trajs_R_angle_start = []
    trajs_R_angle_stimu = []
    trajs_R_angle_end = []

    trajs_a_angle_start = []
    trajs_a_angle_stimu = []
    trajs_a_angle_end = []

    trajs_stimuli_a_start = []
    trajs_stimuli_a_stimu = []
    trajs_stimuli_a_end = []

    trajs_stimuli_angle_a_start = []
    trajs_stimuli_angle_a_stimu = []
    trajs_stimuli_angle_a_end = []

    for i in range(20):
        # 15seconds
        stimu_time = pd.Timedelta(seconds=15)

        # traj_vR_vtheta
        traj_vR_vtheta_start = make_traj(pd_file_start, stimu_time, "traj_vR_vtheta", i).values
        traj_vR_vtheta_stimu = make_traj(pd_file_stimu, stimu_time, "traj_vR_vtheta", i).values
        traj_vR_vtheta_end = make_traj(pd_file_end, stimu_time, "traj_vR_vtheta", i).values

        trajs_vR_vtheta_start.append(traj_vR_vtheta_start)
        # 空 or 短すぎる軌跡の削除
        trajs_vR_vtheta_start = [t for t in trajs_vR_vtheta_start if t.size >= 120]
        trajs_vR_vtheta_stimu.append(traj_vR_vtheta_stimu)
        trajs_vR_vtheta_stimu = [t for t in trajs_vR_vtheta_stimu if t.size >= 120]
        trajs_vR_vtheta_end.append(traj_vR_vtheta_end)
        trajs_vR_vtheta_end = [t for t in trajs_vR_vtheta_end if t.size >= 120]

        
        # traj_R_v
        traj_R_v_start = make_traj(pd_file_start, stimu_time, "traj_R_v", i).values
        traj_R_v_stimu = make_traj(pd_file_stimu, stimu_time, "traj_R_v", i).values
        traj_R_v_end = make_traj(pd_file_end, stimu_time, "traj_R_v", i).values

        trajs_R_v_start.append(traj_R_v_start)
        # 空 or 短すぎる軌跡の削除
        trajs_R_v_start = [t for t in trajs_R_v_start if t.size >= 120]
        trajs_R_v_stimu.append(traj_R_v_stimu)
        trajs_R_v_stimu = [t for t in trajs_R_v_stimu if t.size >= 120]
        trajs_R_v_end.append(traj_R_v_end)
        trajs_R_v_end = [t for t in trajs_R_v_end if t.size >= 120]
        
        # traj_R_angle
        traj_R_angle_start = make_traj(pd_file_start, stimu_time, "traj_R_angle", i).values
        traj_R_angle_stimu = make_traj(pd_file_stimu, stimu_time, "traj_R_angle", i).values
        traj_R_angle_end = make_traj(pd_file_end, stimu_time, "traj_R_angle", i).values

        trajs_R_angle_start.append(traj_R_angle_start)
        # 空 or 短すぎる軌跡の削除
        trajs_R_angle_start = [t for t in trajs_R_angle_start if t.size >= 120]
        trajs_R_angle_stimu.append(traj_R_angle_stimu)
        trajs_R_angle_stimu = [t for t in trajs_R_angle_stimu if t.size >= 120]
        trajs_R_angle_end.append(traj_R_angle_end)
        trajs_R_angle_end = [t for t in trajs_R_angle_end if t.size >= 120]

        # traj_a_angle
        traj_a_angle_start = make_traj(pd_file_start, stimu_time, "traj_a_angle", i).values
        traj_a_angle_stimu = make_traj(pd_file_stimu, stimu_time, "traj_a_angle", i).values
        traj_a_angle_end = make_traj(pd_file_end, stimu_time, "traj_a_angle", i).values

        trajs_a_angle_start.append(traj_a_angle_start)
        # 空 or 短すぎる軌跡の削除
        trajs_a_angle_start = [t for t in trajs_a_angle_start if t.size >= 120]
        trajs_a_angle_stimu.append(traj_a_angle_stimu)
        trajs_a_angle_stimu = [t for t in trajs_a_angle_stimu if t.size >= 120]
        trajs_a_angle_end.append(traj_a_angle_end)
        trajs_a_angle_end = [t for t in trajs_a_angle_end if t.size >= 120]

        # traj_stimuli_a
        traj_stimuli_a_start = make_traj(pd_file_start, stimu_time, "traj_stimuli_a", i).values
        traj_stimuli_a_stimu = make_traj(pd_file_stimu, stimu_time, "traj_stimuli_a", i).values
        traj_stimuli_a_end = make_traj(pd_file_end, stimu_time, "traj_stimuli_a", i).values

        trajs_stimuli_a_start.append(traj_stimuli_a_start)
        # 空 or 短すぎる軌跡の削除
        trajs_stimuli_a_start = [t for t in trajs_stimuli_a_start if t.size >= 120]
        trajs_stimuli_a_stimu.append(traj_stimuli_a_stimu)
        trajs_stimuli_a_stimu = [t for t in trajs_stimuli_a_stimu if t.size >= 120]
        trajs_stimuli_a_end.append(traj_stimuli_a_end)
        trajs_stimuli_a_end = [t for t in trajs_stimuli_a_end if t.size >= 120]

        # traj_stimuli_angle_a
        traj_stimuli_angle_a_start = make_traj(pd_file_start, stimu_time, "traj_stimuli_angle_a", i).values
        traj_stimuli_angle_a_stimu = make_traj(pd_file_stimu, stimu_time, "traj_stimuli_angle_a", i).values
        traj_stimuli_angle_a_end = make_traj(pd_file_end, stimu_time, "traj_stimuli_angle_a", i).values

        trajs_stimuli_angle_a_start.append(traj_stimuli_angle_a_start)
        # 空 or 短すぎる軌跡の削除
        trajs_stimuli_angle_a_start = [t for t in trajs_stimuli_angle_a_start if t.size >= 120]
        trajs_stimuli_angle_a_stimu.append(traj_stimuli_angle_a_stimu)
        trajs_stimuli_angle_a_stimu = [t for t in trajs_stimuli_angle_a_stimu if t.size >= 120]
        trajs_stimuli_angle_a_end.append(traj_stimuli_angle_a_end)
        trajs_stimuli_angle_a_end = [t for t in trajs_stimuli_angle_a_end if t.size >= 120]
    
    # vR_vtheta
    trajectories_vR_vtheta.append(trajs_vR_vtheta_start)
    trajectories_vR_vtheta.append(trajs_vR_vtheta_stimu)
    trajectories_vR_vtheta.append(trajs_vR_vtheta_end)

    # _R_v
    trajectories_R_v.append(trajs_R_v_start)
    trajectories_R_v.append(trajs_R_v_stimu)
    trajectories_R_v.append(trajs_R_v_end)

    # _R_angle
    trajectories_R_angle.append(trajs_R_angle_start)
    trajectories_R_angle.append(trajs_R_angle_stimu)
    trajectories_R_angle.append(trajs_R_angle_end)

    # _a_angle
    trajectories_a_angle.append(trajs_a_angle_start)
    trajectories_a_angle.append(trajs_a_angle_stimu)
    trajectories_a_angle.append(trajs_a_angle_end)

    # _stimuli_a
    trajectories_stimuli_a.append(trajs_stimuli_a_start)
    trajectories_stimuli_a.append(trajs_stimuli_a_stimu)
    trajectories_stimuli_a.append(trajs_stimuli_a_end)

    # _stimuli_angle_a
    trajectories_stimuli_angle_a.append(trajs_stimuli_angle_a_start)
    trajectories_stimuli_angle_a.append(trajs_stimuli_angle_a_stimu)
    trajectories_stimuli_angle_a.append(trajs_stimuli_angle_a_end)
        
    print(trajectories_stimuli_a[1])
    # 一番短い軌跡の長さを取り出す
    print(len(min(trajectories_a_angle[2], key=len)))

    path_vR_vtheta = f'data/maxent_traj/{SP_NAME}/vR_vtheta/{key}.pkl'
    path_R_v = f'data/maxent_traj/{SP_NAME}/R_v/{key}.pkl'
    path_R_angle = f'data/maxent_traj/{SP_NAME}/R_angle/{key}.pkl'
    path_a_angle = f'data/maxent_traj/{SP_NAME}/a_angle/{key}.pkl'

    path_stimuli_a = f'data/maxent_traj/{SP_NAME}/stimuli_a/{key}.pkl'
    path_stimuli_angle_a = f'data/maxent_traj/{SP_NAME}/stimuli_angle_a/{key}.pkl'
    
    # pickleとして軌跡のリストを保存
    pickle_dump(trajectories_vR_vtheta, path_vR_vtheta)
    pickle_dump(trajectories_R_v, path_R_v)
    pickle_dump(trajectories_R_angle, path_R_angle)
    pickle_dump(trajectories_a_angle, path_a_angle)

    pickle_dump(trajectories_stimuli_a, path_stimuli_a)
    pickle_dump(trajectories_stimuli_angle_a, path_stimuli_angle_a)

