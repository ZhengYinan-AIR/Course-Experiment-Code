# -*- coding: utf-8 -*-
"""
@author: zyn
"""
import seaborn as sns
import scipy.io as scio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wavelet
from sklearn.preprocessing import StandardScaler
random_seed = 13

font = {'family': 'Times New Roman',
        'weight': 'bold',
        'size': 9.5,
        }

dataFile = 'ROP_sn.mat'
data = scio.loadmat(dataFile)
ROP_sn = data['ROP_sn']


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


def Data_Clean(data, ncols):  # 根据箱型图去除异常值
    outlier_index = []
    clean_data = data
    for i in range(ncols):
        outlier_index = list(set(outlier_index + Outlier_Detect(data[:, i])))

    clean_data = np.delete(clean_data, outlier_index, axis=0)
    return clean_data


def Data_Filter(data, ncols):
    """
    wavelet filter
    """
    data_noisereduc = np.array(np.zeros(data.shape))
    for i in range(ncols):
        data_noisereduc[:, i] = wavelet.wavelet_noising(data[:, i])
    return data_noisereduc


class ROP_Data:
    """
    ROP Data preparation
    """

    def __init__(self):
        self.data = []
        self.input_feature = 0
        self.nrows = len(ROP_sn)
        self.ncols = len(ROP_sn[0])
        self.input_feature = self.ncols - 1
        for i in range(self.nrows):
            row_data = ROP_sn[i].tolist()
            self.data.append(row_data)
        self.data = np.array(self.data)

        # df = pd.DataFrame(data=data, columns=)
        self.df = pd.DataFrame(data=self.data, columns=['Depth', 'WOB', 'RPM', 'Torque', 'Q', 'VP',
                                                        'ROP'])  # ['井深', '钻压', '转速','扭矩','泵量','立压','钻速']['井深', '钻压',
        # '转速', '泵量','钻速']

        self.clean_data = Data_Clean(self.data, self.ncols)
        self.filter_data = Data_Filter(self.data, self.ncols)
        self.clean_filter = Data_Filter(self.clean_data,self.ncols)

        scaler = StandardScaler()  # 标准化转换
        scaler.fit(self.data)
        self.norm_data = scaler.transform(self.clean_filter)

        self.cf = pd.DataFrame(data=self.norm_data, columns=['Depth', 'WOB', 'RPM', 'Torque', 'Q', 'VP','ROP'])

    def Get_Data(self):
        return self.data

    def Get_Clean_Data(self):
        return self.clean_data

    def Get_Clean_Filter_Data(self):
        return self.clean_filter

    def Corre_Analy(self):
        # matrix output
        Coef_matrix = np.corrcoef(self.df, rowvar=False)
        print('Coef_matrix:', Coef_matrix)

    def Print_Data(self):
        """
        plot the data, basic visualization
        """
        # Features curve
        plt.figure(1, figsize=(16, 8))
        title = ['Depth', 'WOB', 'RPM', 'Torque', 'Q', 'VP', 'ROP']
        for i in range(7):
            ax = plt.subplot(2, 4, i + 1)
            plt.plot(self.data[:, i])
            plt.plot(self.filter_data[:, i])
            plt.title(title[i], font)
            plt.tick_params(labelsize=9.5)
            labels = ax.get_xticklabels() + ax.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]

        # Boxplot before cleaning
        plt.figure(2, figsize=(16, 8))
        plt.title("Boxplot before cleaning")
        title = ['Depth', 'WOB', 'RPM', 'Torque', 'Q', 'VP', 'ROP']
        for i in range(self.ncols):
            ax = plt.subplot(2, 4, i + 1)
            plt.boxplot(self.data[:, i], showmeans=True, meanline=True)
            plt.title(title[i], fontproperties='Times New Roman', size=9)
            plt.tick_params(labelsize=9.5)
            labels = ax.get_xticklabels() + ax.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]
            plt.grid(True)

        # Boxplot after cleaning
        plt.figure(3, figsize=(16, 8))
        plt.title("Boxplot after cleaning")
        title = ['Depth', 'WOB', 'RPM', 'Torque', 'Q', 'VP', 'ROP']
        for i in range(self.ncols):
            ax = plt.subplot(2, 4, i + 1)
            plt.boxplot(self.clean_data[:, i], showmeans=True, meanline=True)
            plt.title(title[i], fontproperties='Times New Roman', size=9)
            plt.tick_params(labelsize=9.5)
            labels = ax.get_xticklabels() + ax.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]
            plt.grid(True)

        # cleaned data
        plt.figure(4, figsize=(16, 8))
        title = ['Depth', 'WOB', 'RPM', 'Torque', 'Q', 'VP']
        for i in range(self.input_feature):
            ax = plt.subplot(2, 3, i + 1)
            plt.plot(self.clean_data[:, i])
            plt.title(title[i], font)
            plt.tick_params(labelsize=9.5)
            labels = ax.get_xticklabels() + ax.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]

        # # Scatter plot
        # sns.pairplot(self.df)
        #
        # Heatmap
        figure, ax = plt.subplots(figsize=(7, 7))
        sns.heatmap(self.cf.corr(), square=True, annot=True, ax=ax, xticklabels=True, yticklabels=True)
        plt.tick_params(labelsize=9.5)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]

        # cleaned data
        plt.figure(6, figsize=(16, 8))
        title = ['Depth', 'WOB', 'RPM', 'Torque', 'Q', 'VP','ROP']
        for i in range(self.ncols):
            ax = plt.subplot(2, 4, i + 1)
            plt.plot(self.clean_filter[:, i])
            plt.title(title[i], font)
            plt.tick_params(labelsize=9.5)
            labels = ax.get_xticklabels() + ax.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]

        sns.pairplot(self.cf)

def PCA_Data(sample):
    a = 1

if __name__ == '__main__':
    data = ROP_Data()
    data.Print_Data()
    plt.show()
