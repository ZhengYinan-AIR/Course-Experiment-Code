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
# describe=df.describe()
# # describe.to_csv("OPT.csv")
# print(df.describe())
# # print(df)
#
a_flow = row_data[:, 0]
# print("均值")
# print(np.mean(a_flow))  # 均值
# print("中位数")
# print(np.median(a_flow))  # 中位数
# print("众数")
# print(stats.mode(a_flow)[0][0])  # 众数

########################################################################################################## example
# x = np.linspace(0, 10, 1000)
# plt.plot(x, np.sin(x), label=u"宋体 $\mathrm{1}$")  # 图例
# plt.plot(x, np.cos(x), label=u"宋体 $\mathrm{2}$")  # 图例
#
# plt.title(u'宋体 $\mathrm{Times \; New \; Roman1}$', size=14, fontproperties=SimSun)  # 局部设置中文为宋体，英文数字为Times New Roman
# plt.xlabel(u'宋体 $\mathrm{Times \; New \; Roman2}$', size=14, fontproperties=SimSun)
# plt.ylabel(u'宋体 $\mathrm{Times \; New \; Roman3}$', size=14, fontproperties=SimSun)
# plt.text(3, 0.5, u"宋体 $\mathrm{12}$", size=14, fontproperties=SimSun)  # 设置标注文字中文为宋体，英文数字为Times New Roman
# plt.legend(prop={'family': 'SimSun', 'size': 12})  # 设置图例字体为宋体
#
# # plt.axis('off') # 刻度仍为默认字体
# plt.savefig("usestix.pdf", dpi=600, bbox_inches='tight')  # 保存为pdf
# # plt.savefig("usestix.svg") # 若使用了公式，直接导出的svg无法使用
# os.system("pdf2svg usestix.pdf usestix.svg")  # 将pdf转换为svg(若仅需要设置中文字体，则不需要使用pdf2svg进行转换)
############################################################################################################

sns.set(style='darkgrid')
# # plt.figure(1, figsize=(11,12))

# # curve
# # 可视化数据
# plt1size = 12
# ax = plt.subplot(2, 2, 1)
# plt.plot(a_flow,c='darkcyan')
# plt.title(u'$\mathrm{(a)}$：时序图', size=plt1size, fontproperties=SimSun)
# plt.xlabel('数据点', size=plt1size, fontproperties=SimSun)
# plt.ylabel(u'$\mathrm{A}$物料流量（$\mathrm{kscmh}$）', size=plt1size, fontproperties=SimSun)
# plt.tick_params(labelsize=plt1size)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
#
# # Boxplot
# ax = plt.subplot(2, 2, 3)
# plt.boxplot(a_flow, showmeans=True, meanline=True)
# plt.title(u'$\mathrm{(c)}$：箱型图', size=plt1size, fontproperties=SimSun)
# plt.tick_params(labelsize=plt1size)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.grid(True)
#
# ax = plt.subplot(2, 2, 2)
# sns.distplot(a_flow,color="r",bins=30,kde=True)
# plt.tick_params(labelsize=plt1size)
# plt.title(u'$\mathrm{(b)}$：直方图', size=plt1size, fontproperties=SimSun)
# plt.xlabel(u'$\mathrm{A}$物料流量（$\mathrm{kscmh}$）', size=plt1size, fontproperties=SimSun)
# plt.ylabel('频次',size=plt1size, fontproperties=SimSun)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
#
# ax = plt.subplot(2, 2, 4)
# plt.plot(a_flow)
# plt.fill_between(x=range(nrows), y1=0, y2=a_flow, alpha = 0.3,facecolor='royalblue')
# plt.title(u'$\mathrm{(d)}$：二维图', size=plt1size, fontproperties=SimSun)
# plt.xlabel('数据点', size=plt1size, fontproperties=SimSun)
# plt.ylabel(u'$\mathrm{A}$物料流量（$\mathrm{kscmh}$）', size=plt1size, fontproperties=SimSun)
# plt.tick_params(labelsize=plt1size)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.savefig('fig1.png', format='png', bbox_inches='tight', dpi=600)
# plt.close()
#
# # 去除离群点
# def Data_Clean(data):  # 根据箱型图去除异常值
#     outlier_index = []
#     outlier_index = list(set(outlier_index + Outlier_Detect(data)))
#
#     clean_data = np.delete(data, outlier_index, axis=0)
#     return clean_data
#
# def Outlier_Detect(bc_data):
#     percentile = np.percentile(bc_data, (25, 50, 75), interpolation='midpoint')
#     # print("分位数：", percentile)
#     # 以下为箱线图的五个特征值
#     Q1 = percentile[0]  # 上四分位数
#     Q3 = percentile[2]  # 下四分位数
#     IQR = Q3 - Q1  # 四分位距
#     ulim = Q3 + 1.5 * IQR  # 上限 非异常范围内的最大值
#     llim = Q1 - 1.5 * IQR  # 下限 非异常范围内的最小值
#
#     outlier_index = []
#     for i in range(len(bc_data)):
#         if bc_data[i] < llim or bc_data[i] > ulim:
#             outlier_index.append(i)
#     return outlier_index
#
# clean_data = Data_Clean(a_flow)
#
# plt.figure(2, figsize=(7,3))
# sns.set(style='darkgrid')
# # curve
#
# ax = plt.subplot(1, 2, 1)
# plt.boxplot(a_flow, showmeans=True, meanline=True)
# plt.title(u'$\mathrm{(a)}$：未清洗数据箱型图', size=9, fontproperties=SimSun)
# plt.tick_params(labelsize=9)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
#
# # Boxplot
# ax = plt.subplot(1, 2, 2)
# plt.boxplot(clean_data, showmeans=True, meanline=True)
# plt.title(u'$\mathrm{(b)}$：已清洗数据箱型图', size=9, fontproperties=SimSun)
# plt.tick_params(labelsize=9)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
#
# plt.savefig('fig2.png', format='png', bbox_inches='tight', dpi=600)
# plt.close()
#
#
# 平滑
dataFile1 = 'A_flow_smooth1.mat'
data1 = scio.loadmat(dataFile1)
A_flow_smooth1 = data1['A_flow_smooth1'].reshape(-1, 1)
dataFile2 = 'A_flow_smooth2.mat'
data2 = scio.loadmat(dataFile2)
A_flow_smooth2 = data2['A_flow_smooth2'].reshape(-1, 1)
dataFile3 = 'A_flow_smooth3.mat'
data3 = scio.loadmat(dataFile3)
A_flow_smooth3 = data3['A_flow_smooth3'].reshape(-1, 1)
s_data1 = []
s_data2 = []
s_data3 = []
for i in range(nrows):
    row = A_flow_smooth1[i].tolist()
    s_data1.append(row)
s_data1 = np.array(s_data1)
for i in range(nrows):
    row = A_flow_smooth2[i].tolist()
    s_data2.append(row)
s_data2 = np.array(s_data2)
for i in range(nrows):
    row = A_flow_smooth3[i].tolist()
    s_data3.append(row)
s_data3 = np.array(s_data3)

# plt.figure(3, figsize=(6,5))
# sns.set(style='darkgrid')
# # curve
# plt1size = 9
# ax = plt.subplot(3, 1, 1)
# plt.plot(a_flow[0:50],c='darkcyan',label='原数据',marker='>',markersize=2,linewidth=1)
# plt.plot(s_data1[0:50],label='平滑后数据',marker='o',markersize=2,linewidth=1)
# plt.title(u'$\mathrm{(a)}$：滑动窗口大小-2', size=plt1size, fontproperties=SimSun)
# plt.xlabel('数据点', size=plt1size, fontproperties=SimSun)
# plt.ylabel(u'$\mathrm{A}$物料流量（$\mathrm{kscmh}$）', size=plt1size, fontproperties=SimSun)
#
# plt.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
#                 mode="expand", borderaxespad=0, ncol=2,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
# plt.tick_params(labelsize=plt1size)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
#
# ax = plt.subplot(3, 1, 2)
# plt.plot(a_flow[0:50],c='darkcyan',label='原数据',marker='>',markersize=2,linewidth=1)
# plt.plot(s_data2[0:50],label='平滑后数据',marker='o',markersize=2,linewidth=1)
# plt.title(u'$\mathrm{(b)}$：滑动窗口大小-5', size=plt1size, fontproperties=SimSun)
# plt.xlabel('数据点', size=plt1size, fontproperties=SimSun)
# plt.ylabel(u'$\mathrm{A}$物料流量（$\mathrm{kscmh}$）', size=plt1size, fontproperties=SimSun)
# plt.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
#                 mode="expand", borderaxespad=0, ncol=2,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
# plt.tick_params(labelsize=plt1size)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
#
# ax = plt.subplot(3, 1, 3)
# plt.plot(a_flow[0:50],c='darkcyan',label='原数据',marker='>',markersize=2,linewidth=1)
# plt.plot(s_data3[0:50],label='平滑后数据',marker='o',markersize=2,linewidth=1)
# plt.title(u'$\mathrm{(c)}$：滑动窗口大小-15', size=plt1size, fontproperties=SimSun)
# plt.xlabel('数据点', size=plt1size, fontproperties=SimSun)
# plt.ylabel(u'$\mathrm{A}$物料流量（$\mathrm{kscmh}$）', size=plt1size, fontproperties=SimSun)
# plt.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
#                 mode="expand", borderaxespad=0, ncol=2,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
# plt.tick_params(labelsize=plt1size)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.tight_layout()
#
# plt.savefig('fig3.png', format='png', bbox_inches='tight', dpi=600)
# plt.close()

figure, (ax1, ax2, ax3) = plt.subplots(3, 1,
                                        figsize=(9, 7),
                                        dpi=600,
                                        # 共享x轴
                                        sharex='all')
ax1.plot(a_flow[0:50]*25,c='darkcyan',label='原数据',marker='>',markersize=2,linewidth=1)
ax1.plot(s_data1[0:50]*25,label='滑动窗口大小-2',marker='o',markersize=2,linewidth=1)
ax2.plot(a_flow[0:50]*25,c='darkcyan',label='原数据',marker='>',markersize=2,linewidth=1)
ax2.plot(s_data2[0:50]*25,label='滑动窗口大小-5',marker='o',markersize=2,linewidth=1)
ax3.plot(a_flow[0:50]*25,c='darkcyan',label='原数据',marker='>',markersize=2,linewidth=1)
ax3.plot(s_data3[0:50]*25,label='滑动窗口大小-15',marker='o',markersize=2,linewidth=1)
ax1.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=2,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
ax2.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=2,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
ax3.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=2,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体

figure.text(0.5, 0, '数据点', size=11, fontproperties=SimSun, ha='center')
figure.text(0, 0.5, u'$\mathrm{RPM}$', size=11, fontproperties=SimSun, va='center', rotation='vertical')
labels = ax1.get_xticklabels() + ax1.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
labels = ax2.get_xticklabels() + ax2.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
labels = ax3.get_xticklabels() + ax3.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
plt.tight_layout()
figure.subplots_adjust(hspace=0.1)
plt.savefig('fig111.png', format='png', bbox_inches='tight', dpi=600)
#
# # 滤波
# dataFile4 = 'A_flow_nodp.mat'
# data4 = scio.loadmat(dataFile4)
# A_flow_smooth4 = data4['A_flow_nodp'].reshape(-1, 1)
# w_data = []
#
# for i in range(nrows):
#     row = A_flow_smooth4[i].tolist()
#     w_data.append(row)
# w_data = np.array(w_data)
# figure, (ax1, ax2) = plt.subplots(2, 1,
#                                         figsize=(9, 7),
#                                         dpi=600,
#                                         # 共享x轴
#                                         sharex='all')
# ax1.plot(a_flow,c='darkcyan',label='原数据',linewidth=1)
# ax2.plot(w_data,label='小波滤波后数据',linewidth=1)
# ax1.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
#                 mode="expand", borderaxespad=0, ncol=1,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
# ax2.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.1), loc="lower left",
#                 mode="expand", borderaxespad=0, ncol=2,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
#
# figure.text(0.5, 0, '数据点', size=11, fontproperties=SimSun, ha='center')
# figure.text(0, 0.5, u'$\mathrm{A}$物料流量（$\mathrm{kscmh}$）', size=11, fontproperties=SimSun, va='center', rotation='vertical')
# labels = ax1.get_xticklabels() + ax1.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# labels = ax2.get_xticklabels() + ax2.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.tight_layout()
# figure.subplots_adjust(hspace=0.1)
# plt.savefig('fig4.png', format='png', bbox_inches='tight', dpi=600)
#
# # # pca
# pca = PCA(n_components=5, whiten=True, random_state=41)  # 降维至3个特征
# newX = pca.fit_transform(row_data)
# print(newX.shape)
# explained_var = pca.explained_variance_ratio_  # 获取贡献率
# print(explained_var)
# labels = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5']
# figure, ax = plt.subplots(figsize=(5.5, 5.5))
# for i in range(len(labels)):
#     plt.bar(labels[i], explained_var[i])
# plt.tick_params(labelsize=9)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.xlabel('Pricipal Component')
# plt.ylabel('Proportion of Variance Explained')
# plt.xlabel('主成分', size=9, fontproperties=SimSun)
# plt.ylabel('主成分贡献率', size=9, fontproperties=SimSun)
# plt.tick_params(labelsize=9)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.savefig('pca.png', format='png', bbox_inches='tight', dpi=600)
# plt.close()
#
# # 小波分析
# dataFile1 = 'coffec.mat'
# data1 = scio.loadmat(dataFile1)
# A_flow_smooth1 = data1['coffec'].reshape(-1, 1)
# dataFile2 = 'AA1.mat'
# data2 = scio.loadmat(dataFile2)
# A_flow_smooth2 = data2['AA1'].reshape(-1, 1)
# dataFile3 = 'AA2.mat'
# data3 = scio.loadmat(dataFile3)
# A_flow_smooth3 = data3['AA2'].reshape(-1, 1)
# dataFile4 = 'AA3.mat'
# data4 = scio.loadmat(dataFile4)
# A_flow_smooth4 = data4['AA3'].reshape(-1, 1)
# s_data1 = []
# s_data2 = []
# s_data3 = []
# s_data4 = []
# for i in range(len(A_flow_smooth1)):
#     row = A_flow_smooth1[i].tolist()
#     s_data1.append(row)
# s_data1 = np.array(s_data1)
# for i in range(len(A_flow_smooth2)):
#     row = A_flow_smooth2[i].tolist()
#     s_data2.append(row)
# s_data2 = np.array(s_data2)
# for i in range(len(A_flow_smooth3)):
#     row = A_flow_smooth3[i].tolist()
#     s_data3.append(row)
# s_data3 = np.array(s_data3)
# for i in range(len(A_flow_smooth4)):
#     row = A_flow_smooth4[i].tolist()
#     s_data4.append(row)
# s_data4 = np.array(s_data4)
#
#
# plt.figure(10, figsize=(7,5))
# sns.set(style='darkgrid')
# # curve
# plt1size = 9
# ax = plt.subplot(4, 1, 1)
# plt.plot(s_data1,linewidth=0.5)
# plt.title('低频系数', size=plt1size, fontproperties=SimSun)
# plt.tick_params(labelsize=plt1size)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
#
# ax = plt.subplot(4, 1, 2)
# plt.plot(s_data2,linewidth=0.5)
# plt.title('尺度2高频系数', size=plt1size, fontproperties=SimSun)
# plt.tick_params(labelsize=plt1size)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
#
# ax = plt.subplot(4, 1, 3)
# plt.plot(s_data3,linewidth=0.5)
# plt.title('尺度3高频系数', size=plt1size, fontproperties=SimSun)
# plt.tick_params(labelsize=plt1size)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.tight_layout()
#
# ax = plt.subplot(4, 1, 4)
# plt.plot(s_data4,linewidth=0.5)
# plt.title('尺度4高频系数', size=plt1size, fontproperties=SimSun)
# plt.tick_params(labelsize=plt1size)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.tight_layout()
#
# plt.savefig('xiaobofenxi.png', format='png', bbox_inches='tight', dpi=600)
# plt.close()
#
# # curve
# ax = plt.subplot(2, 1, 1)
# plt.plot(a_flow[0:1000])
# plt.title('A Flow Rate', font)
# plt.tick_params(labelsize=9)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# ax = plt.subplot(2, 1, 2)
# plt.plot(data_noisereduc[0:1000])
# plt.title('Wavelet', font)
# plt.tick_params(labelsize=9)
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
#
# ## 变换
# scaler1 = StandardScaler()  # 标准化转换
# scaler1.fit(a_flow.reshape(-1,1))
# norm_data = scaler1.transform(a_flow.reshape(-1,1))
#
# scaler2 = MinMaxScaler()  # 最大最小转换
# scaler2.fit(a_flow.reshape(-1,1))
# minmax_data = scaler2.transform(a_flow.reshape(-1,1))
#
# scaler3 = MaxAbsScaler()  # 最大最小转换
# scaler3.fit(a_flow.reshape(-1,1))
# maxabs_data = scaler3.transform(a_flow.reshape(-1,1))
# #
# figure, (ax1, ax2, ax3,ax4) = plt.subplots(4, 1,
#                                         figsize=(9, 9),
#                                         dpi=600,
#                                         # 共享x轴
#                                         sharex='all')
# ax1.plot(a_flow,c='darkcyan',label='原数据',linewidth=1)
#
# ax2.plot(norm_data,label='z分数归一化',linewidth=1)
#
#
# ax3.plot(minmax_data,c='lightcoral',label='最大最小归一化',linewidth=1)
#
# ax4.plot(maxabs_data,c='orange',label='最大绝对归一化',linewidth=1)
# ax1.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
#                 mode="expand", borderaxespad=0, ncol=1,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
# ax2.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
#                 mode="expand", borderaxespad=0, ncol=1,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
# ax3.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
#                 mode="expand", borderaxespad=0, ncol=1,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
# ax4.legend(frameon=False,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
#                 mode="expand", borderaxespad=0, ncol=1,prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体
# figure.text(0.5, 0, '数据点', size=11, fontproperties=SimSun, ha='center')
#
# labels = ax1.get_xticklabels() + ax1.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# labels = ax2.get_xticklabels() + ax2.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# labels = ax3.get_xticklabels() + ax3.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# labels = ax4.get_xticklabels() + ax4.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.tight_layout()
# figure.subplots_adjust(hspace=0.1)
# plt.savefig('fig5.png', format='png', bbox_inches='tight', dpi=600)


# pca

plt.show()
