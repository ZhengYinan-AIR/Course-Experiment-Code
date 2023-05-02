# -*- coding: utf-8 -*-
"""
@author: zyn
"""
import seaborn as sns
import scipy.io as scio
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.decomposition import PCA

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams

# 全局设置字体及大小，设置公式字体即可，若要修改刻度字体，可在此修改全局字体
font = {
    "mathtext.fontset": 'stix',
    # "font.family":'serif',
    # "font.serif": ['SimSun'],
    "font.size": 9,
}
rcParams.update(font)

# 载入宋体
SimSun = FontProperties(fname='D:\Anaconda\envs\ML\Lib\site-packages\matplotlib\mpl-data/fonts/ttf/SimSun.ttf')

titlefont = {'family': 'SimSun',
             'weight': 'bold',
             'size': 9,
             }

dataFile = 'no_error.mat'
data = scio.loadmat(dataFile)
simout = data['simout']

nrows = len(simout)
ncols = len(simout[0])
row_data = []
for i in range(nrows):
    row = simout[i].tolist()
    row_data.append(row)
row_data = np.array(row_data)

df = pd.DataFrame(data=row_data)

scaler1 = StandardScaler()  # 标准化转换
scaler1.fit(row_data)
norm_data = scaler1.transform(row_data)
df = pd.DataFrame(data=row_data)
norm_df = pd.DataFrame(data=row_data)
sns.set(style='darkgrid')
# # matrix output
# Coef_matrix = np.corrcoef(norm_df, rowvar=False)
# coedf = pd.DataFrame(data=Coef_matrix)
#
#
# figure, ax = plt.subplots(figsize=(8.5, 8))
# plt.rc('font', family='Times New Roman')
# cmap=sns.heatmap(Coef_matrix,linewidths=0.8)
#
# cbar = cmap.collections[0].colorbar
# cbar.ax.tick_params(labelsize=9)
# plt.tick_params(labelsize=9)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.tick_params(labelsize=9)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.savefig('heat.png', format='png', bbox_inches='tight', dpi=600)

figure, ax = plt.subplots(figsize=(4, 4))
plt.rc('font', family='Times New Roman')
# plt.scatter(norm_data[:,6],norm_data[:,12])
plt.scatter(row_data[:,34],row_data[:,10])
plt.xlabel('反应釜压力', size=9, fontproperties=SimSun)
plt.ylabel('产品分离器压力', size=9, fontproperties=SimSun)
plt.tick_params(labelsize=9)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
plt.tick_params(labelsize=9)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
plt.savefig('scatter.png', format='png', bbox_inches='tight', dpi=600)

# plt.close()

figure, ax = plt.subplots()
plt.plot(row_data[:,29])
plt.show()