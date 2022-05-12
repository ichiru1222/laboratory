"""tsv -> pandas
  pickle化
"""

import glob
import pickle
import re

import pandas as pd
from data.data_utils import get_dist_V, get_R, get_R_verosity, get_theta, get_theta_verosity

SP_NAME = "norpA"
DIR_NAME = f"data/raw/{SP_NAME}/*.tsv"

file_names = glob.glob(DIR_NAME)

print(file_names)

print("initialize pandas data")
for file in file_names:
    # pandasのファイル名 (ex no-12)
    key = re.search("no\d+-.+-\d", file).group()
    df = pd.read_csv(file, delimiter='\t')

    df = df.query("pos_x_wma <= 140")
    df = df.query("pos_y_wma <= 140")

    df["R"] = df.apply(get_R, axis=1)
    df["theta"] = df.apply(get_theta, axis=1)

    df["diff_R"] = df["R"].diff().abs()
    #(rad)
    df["diff_theta"] = df["theta"].diff().abs()

    df["dist_v"] = df.apply(get_dist_V, axis=1)
    df["R_verosity"] = df.apply(get_R_verosity, axis=1)
    df["theta_verosity"] = df.apply(get_theta_verosity, axis=1)
    df = df.dropna()
    
    # pickleとして保存
    df.to_pickle(f'data/pandas/{SP_NAME}/{key}.pkl')