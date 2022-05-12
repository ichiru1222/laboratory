"""ファイルの移動用スクリプト
"""

import os
import glob
import tqdm
import re
import shutil

file_names = glob.glob('data/20211009/*.tsv')
file_names = sorted(file_names)
# print(file_names)

SP_NAME = "DGRP362"
sp_list = []

for i, file_name in enumerate(file_names):
    if SP_NAME in file_name:
        sp_list.append(file_names[i])
print(sp_list)

for file in sp_list:
    shutil.copy(file, f'data/{SP_NAME}')
