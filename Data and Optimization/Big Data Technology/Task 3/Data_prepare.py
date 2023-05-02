# -*- coding: utf-8 -*-
"""
@author: zyn
"""
import seaborn as sns
import scipy.io as scio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
random_seed = 13

font = {
    "mathtext.fontset": 'stix',
    # "font.family":'serif',
    # "font.serif": ['SimSun'],
    "font.size": 9,
}
rcParams.update(font)

# 载入宋体
SimSun = FontProperties(fname='D:\Anaconda\envs\ML\Lib\site-packages\matplotlib\mpl-data/fonts/ttf/SimSun.ttf')

sns.set(style='darkgrid')

dataFile = 'data.mat'
data = scio.loadmat(dataFile)
ROP_sn = data['data']


def DB_Index(data):  # 根据箱型图去除异常值
    speed = data[:,0:1]
    power = data[:,2:3]
    item = np.hstack((speed,power))
    category = DBSCAN(eps=0.02, min_samples=10).fit_predict(item)
    return category
def DB_Index1(data,eps,minsamples):  # 根据箱型图去除异常值
    speed = data[:,0:1]
    power = data[:,2:3]
    item = np.hstack((speed,power))
    category = DBSCAN(eps=eps, min_samples=minsamples).fit_predict(item)
    return category

def KM_Index(data):  # 根据箱型图去除异常值
    speed = data[:,0:1]
    power = data[:,2:3]
    item = np.hstack((speed,power))
    clf = KMeans(n_clusters=2)
    category = clf.fit_predict(item)
    center = clf.cluster_centers_
    return category,center

def Data_Clean(data, index,row):
    clean_data = []
    for i in range(row):
        if index[i] != -1:
            clean_data.append(data[i,:])
    clean_data = np.array(clean_data)
    return clean_data

def Data_classify(data,index,row):
    class1 = []
    class2 = []
    for i in range(row):
        if index[i]==0:
            class1.append(data[i,:])
        else:
            class2.append(data[i,:])
    class1 = np.array(class1)
    class2 = np.array(class2)
    return class1,class2

class ROP_Data:
    """
    ROP Data preparation
    """

    def __init__(self):
        self.data = []
        self.input_feature = 0
        self.nrows = 20000
        self.ncols = len(ROP_sn[0])
        self.input_feature = self.ncols - 1
        for i in range(self.nrows):
            row_data = ROP_sn[i].tolist()
            self.data.append(row_data)
        self.data = np.array(self.data)
        self.df = pd.DataFrame(data=self.data, columns=['Speed', 'Direction', 'Power'])
        print(self.df.describe())
        self.min = np.min(self.data, axis=0)
        self.max = np.max(self.data, axis=0)
        scaler = MinMaxScaler(feature_range=(0, 1))  # 标准化转换
        scaler.fit(self.data)
        self.norm_data = scaler.transform(self.data)
        self.cf = pd.DataFrame(data=self.norm_data, columns=['Speed', 'Direction', 'Power'])
        #
        self.clean_index = DB_Index(self.norm_data)
        self.clean_data = Data_Clean(self.norm_data,self.clean_index,self.nrows)

        self.cat,self.center = KM_Index(self.clean_data)

        self.class1,self.class2 = Data_classify(self.clean_data,self.cat,np.shape(self.clean_data)[0])

    def Get_center(self):
        return self.center
    def Get_minmax(self):
        return self.min,self.max

    def Get_Data(self):
        return self.data

    def Get_Clean_Data(self):
        return self.clean_data

    def Get_Class1(self):
        return self.class1

    def Get_Class2(self):
        return self.class2

    def Corre_Analy(self):
        # matrix output
        Coef_matrix = np.corrcoef(self.df, rowvar=False)
        print('Coef_matrix:', Coef_matrix)

    def Print_Data(self):
        """
        plot the data, basic visualization
        """
        # Features curve
        # plt.figure(1, figsize=(16,8))
        # ax = plt.subplot(3, 1, 1)
        # plt.plot(self.data[:, 0])
        # plt.ylabel('风速', size=9, fontproperties=SimSun)
        # plt.xlabel('数据点', size=9, fontproperties=SimSun)
        # plt.tick_params(labelsize=9)
        # labels = ax.get_xticklabels() + ax.get_yticklabels()
        # [label.set_fontname('Times New Roman') for label in labels]
        #
        # ax = plt.subplot(3, 1, 2)
        # plt.plot(self.data[:, 1],color='orange')
        # plt.ylabel('风向', size=9, fontproperties=SimSun)
        # plt.xlabel('数据点', size=9, fontproperties=SimSun)
        # plt.tick_params(labelsize=9)
        # labels = ax.get_xticklabels() + ax.get_yticklabels()
        # [label.set_fontname('Times New Roman') for label in labels]
        #
        # ax = plt.subplot(3, 1, 3)
        # plt.plot(self.data[:, 2],color='lightcoral')
        # plt.ylabel('功率', size=9, fontproperties=SimSun)
        # plt.xlabel('数据点', size=9, fontproperties=SimSun)
        # plt.tick_params(labelsize=9)
        # labels = ax.get_xticklabels() + ax.get_yticklabels()
        # [label.set_fontname('Times New Roman') for label in labels]
        # plt.tight_layout()
        # plt.savefig('fig1.png', format='png', bbox_inches='tight', dpi=600)

        # g = sns.pairplot(self.df, diag_kind="kde")
        # g.map_lower(sns.kdeplot, levels=3, color=".2")
        # plt.savefig('fig2.png', format='png', bbox_inches='tight', dpi=600)
        #
        #
        # Heatmap
        # figure, ax = plt.subplots(figsize=(7, 7))
        # sns.heatmap(self.cf.corr(), square=True, annot=True, ax=ax, xticklabels=True,
        #             yticklabels=True,linewidths=0.8,cmap='YlGnBu',cbar=False)
        # plt.tick_params(labelsize=9)
        # labels = ax.get_xticklabels() + ax.get_yticklabels()
        # [label.set_fontname('Times New Roman') for label in labels]
        # plt.savefig('fig3.png', format='png', bbox_inches='tight', dpi=600)
        #
        # plt.figure(4, figsize=(16,8))
        # ax = plt.subplot(1, 2, 1)
        # plt.scatter(self.clean_data[:, 0], self.clean_data[:, 2])
        # plt.xlabel('风速', size=9, fontproperties=SimSun)
        # plt.ylabel('功率', size=9, fontproperties=SimSun)
        # plt.tick_params(labelsize=9)
        # labels = ax.get_xticklabels() + ax.get_yticklabels()
        # [label.set_fontname('Times New Roman') for label in labels]
        #
        # colors =['coral','lightcoral','darkcyan']#三种不同颜色
        # color_index = self.clean_index*0
        # color_index=color_index.tolist()
        # for i in range(len(color_index)):
        #     color_index[i]=colors[self.clean_index[i]]
        # ax = plt.subplot(1, 2, 2)
        # plt.scatter(self.norm_data[:, 0], self.norm_data[:, 2], c=color_index)
        # plt.xlabel('风速', size=9, fontproperties=SimSun)
        # plt.ylabel('功率', size=9, fontproperties=SimSun)
        # plt.tick_params(labelsize=9)
        # labels = ax.get_xticklabels() + ax.get_yticklabels()
        # [label.set_fontname('Times New Roman') for label in labels]
        # plt.tight_layout()
        # plt.savefig('fig4.png', format='png', bbox_inches='tight', dpi=600)
        #

        # plt.figure(6, figsize=(16,8))
        # ax = plt.subplot(1, 2, 1)
        # plt.scatter(self.data[:, 0], self.data[:, 2])
        # plt.xlabel('风速', size=9, fontproperties=SimSun)
        # plt.ylabel('功率', size=9, fontproperties=SimSun)
        # plt.tick_params(labelsize=9)
        # labels = ax.get_xticklabels() + ax.get_yticklabels()
        # [label.set_fontname('Times New Roman') for label in labels]
        #
        # ax = plt.subplot(1, 2, 2)
        # plt.scatter(self.norm_data[:, 0], self.norm_data[:, 2])
        # plt.xlabel('风速', size=9, fontproperties=SimSun)
        # plt.ylabel('功率', size=9, fontproperties=SimSun)
        # plt.tick_params(labelsize=9)
        # labels = ax.get_xticklabels() + ax.get_yticklabels()
        # [label.set_fontname('Times New Roman') for label in labels]
        # plt.tight_layout()
        # plt.savefig('fig6.png', format='png', bbox_inches='tight', dpi=600)

        plt.figure(7, figsize=(16, 8))
        plt1size=9
        ax = plt.subplot(2, 2, 1)
        sns.distplot(self.class1[:,0],color="r",bins=30,kde=True)
        plt.tick_params(labelsize=plt1size)
        plt.title(u'$\mathrm{(a)}$：第一类风速直方图', size=plt1size, fontproperties=SimSun)
        plt.xlabel('风速', size=plt1size, fontproperties=SimSun)
        plt.ylabel('频次',size=plt1size, fontproperties=SimSun)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        #
        ax = plt.subplot(2, 2, 2)
        sns.distplot(self.class1[:,1],color="g",bins=30,kde=True)
        plt.tick_params(labelsize=plt1size)
        plt.title(u'$\mathrm{(b)}$：第一类风向直方图', size=plt1size, fontproperties=SimSun)
        plt.xlabel('风向', size=plt1size, fontproperties=SimSun)
        plt.ylabel('频次',size=plt1size, fontproperties=SimSun)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]

        ax = plt.subplot(2, 2, 3)
        sns.distplot(self.class2[:,0],color="r",bins=30,kde=True)
        plt.tick_params(labelsize=plt1size)
        plt.title(u'$\mathrm{(c)}$：第二类风速直方图', size=plt1size, fontproperties=SimSun)
        plt.xlabel('风速', size=plt1size, fontproperties=SimSun)
        plt.ylabel('频次',size=plt1size, fontproperties=SimSun)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]

        ax = plt.subplot(2, 2, 4)
        sns.distplot(self.class2[:,1],color="g",bins=30,kde=True)
        plt.tick_params(labelsize=plt1size)
        plt.title(u'$\mathrm{(d)}$：第二类风速直方图', size=plt1size, fontproperties=SimSun)
        plt.xlabel('风向', size=plt1size, fontproperties=SimSun)
        plt.ylabel('频次',size=plt1size, fontproperties=SimSun)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        plt.tight_layout()
        plt.savefig('fig11.png', format='png', bbox_inches='tight', dpi=600)


        plt.figure(7, figsize=(16, 8))
        plt1size=9
        ax = plt.subplot(2, 2, 1)
        sns.distplot(self.data[:,0],color="r",bins=30,kde=True)
        plt.tick_params(labelsize=plt1size)
        plt.title(u'$\mathrm{(a)}$：原始风速直方图', size=plt1size, fontproperties=SimSun)
        plt.xlabel('风速', size=plt1size, fontproperties=SimSun)
        plt.ylabel('频次',size=plt1size, fontproperties=SimSun)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        #
        ax = plt.subplot(2, 2, 2)
        sns.distplot(self.data[:,1],color="g",bins=30,kde=True)
        plt.tick_params(labelsize=plt1size)
        plt.title(u'$\mathrm{(b)}$：原始风向直方图', size=plt1size, fontproperties=SimSun)
        plt.xlabel('风向', size=plt1size, fontproperties=SimSun)
        plt.ylabel('频次',size=plt1size, fontproperties=SimSun)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]

        ax = plt.subplot(2, 2, 3)
        sns.distplot(self.clean_data[:,0],color="r",bins=30,kde=True)
        plt.tick_params(labelsize=plt1size)
        plt.title(u'$\mathrm{(c)}$：清洗后风速直方图', size=plt1size, fontproperties=SimSun)
        plt.xlabel('风速', size=plt1size, fontproperties=SimSun)
        plt.ylabel('频次',size=plt1size, fontproperties=SimSun)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]

        ax = plt.subplot(2, 2, 4)
        sns.distplot(self.clean_data[:,1],color="g",bins=30,kde=True)
        plt.tick_params(labelsize=plt1size)
        plt.title(u'$\mathrm{(d)}$：清洗后风速直方图', size=plt1size, fontproperties=SimSun)
        plt.xlabel('风向', size=plt1size, fontproperties=SimSun)
        plt.ylabel('频次',size=plt1size, fontproperties=SimSun)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        plt.tight_layout()
        plt.savefig('fig7.png', format='png', bbox_inches='tight', dpi=600)

        # 去除离群点
        def Data_Clean(data):  # 根据箱型图去除异常值
            outlier_index = []
            outlier_index = list(set(outlier_index + Outlier_Detect(data)))

            clean_data = np.delete(data, outlier_index, axis=0)
            return clean_data

        def Outlier_Detect(bc_data):
            percentile = np.percentile(bc_data, (25, 50, 75), interpolation='midpoint')
            # print("分位数：", percentile)
            # 以下为箱线图的五个特征值
            Q1 = percentile[0]  # 上四分位数
            Q3 = percentile[2]  # 下四分位数
            IQR = Q3 - Q1  # 四分位距
            ulim = Q3 + 1.5 * IQR  # 上限 非异常范围内的最大值
            llim = Q1 - 1.5 * IQR  # 下限 非异常范围内的最小值

            outlier_index = []
            for i in range(len(bc_data)):
                if bc_data[i] < llim or bc_data[i] > ulim:
                    outlier_index.append(i)
            return outlier_index

        clean_data = Data_Clean(self.data[:,0])

        plt.figure(2, figsize=(7,3))
        sns.set(style='darkgrid')
        # curve

        ax = plt.subplot(1, 2, 1)
        plt.boxplot(self.data[:,0], showmeans=True, meanline=True)
        plt.title(u'$\mathrm{(a)}$：未清洗数据箱型图', size=9, fontproperties=SimSun)
        plt.tick_params(labelsize=9)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]

        # Boxplot
        ax = plt.subplot(1, 2, 2)
        plt.boxplot(clean_data, showmeans=True, meanline=True)
        plt.title(u'$\mathrm{(b)}$：已清洗数据箱型图', size=9, fontproperties=SimSun)
        plt.tick_params(labelsize=9)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        plt.tight_layout()
        plt.savefig('fig8.png', format='png', bbox_inches='tight', dpi=600)
        plt.close()

        plt.figure(5, figsize=(16,8))
        ax = plt.subplot(1, 2, 1)
        plt.scatter(self.clean_data[:, 0], self.clean_data[:, 2])
        plt.xlabel('风速', size=9, fontproperties=SimSun)
        plt.ylabel('功率', size=9, fontproperties=SimSun)
        plt.tick_params(labelsize=9)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]

        colors =['coral','darkcyan','lightcoral']#三种不同颜色
        color_index = self.cat*0
        color_index=color_index.tolist()
        for i in range(len(color_index)):
            color_index[i]=colors[self.cat[i]]
        ax = plt.subplot(1, 2, 2)
        plt.scatter(self.clean_data[:, 0], self.clean_data[:, 2],c=color_index)
        plt.xlabel('风速', size=9, fontproperties=SimSun)
        plt.ylabel('功率', size=9, fontproperties=SimSun)
        plt.tick_params(labelsize=9)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        plt.tight_layout()
        plt.savefig('fig5.png', format='png', bbox_inches='tight', dpi=600)

        plt.figure(6, figsize=(16, 8))
        eps = [0.02,0.03,0.02,0.04,0.08,0.01]
        minpts = [80,350,300,300,300,80]
        for i in range(6):
            cat = DB_Index1(self.clean_data,eps[i],minpts[i] )
            colors =['cornflowerblue','limegreen','lightcoral','orange','darkcyan']#三种不同颜色
            color_index = cat*0
            color_index=color_index.tolist()
            for j in range(len(color_index)):
                color_index[j]=colors[cat[j]]
            ax = plt.subplot(2, 3, i+1)

            plt.scatter(self.clean_data[:, 0], self.clean_data[:, 2],c=color_index)
            plt.xlabel('风速', size=9, fontproperties=SimSun)
            plt.title(u'$\mathrm{Eps=%.2f, MinPts=%d}$' %(eps[i],minpts[i]), size=9, fontproperties=SimSun)
            plt.ylabel('功率', size=9, fontproperties=SimSun)
            plt.tick_params(labelsize=9)
            labels = ax.get_xticklabels() + ax.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]
        plt.tight_layout()
        plt.savefig('fig10.png', format='png', bbox_inches='tight', dpi=600)


if __name__ == '__main__':
    data = ROP_Data()
    data.Print_Data()
    plt.show()
