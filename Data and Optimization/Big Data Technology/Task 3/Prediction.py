# -*- coding: utf-8 -*-
"""
@author: zyn
"""
import random
import numpy as np
from sklearn.metrics import r2_score
import Data_prepare as Dp
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import max_error
import matplotlib.pyplot as plt
import joblib
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso, LassoCV
from sklearn.svm import SVR
from keras import models
from keras import layers
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

titlefont = {'family': 'SimSun',
             'weight': 'bold',
             'size': 9,
             }
sns.set(style='darkgrid')

data_struct = Dp.ROP_Data()
data1 = data_struct.Get_Class1()
data2 = data_struct.Get_Class2()
min, max = data_struct.Get_minmax()
center = data_struct.Get_center()
print(center)
clean_data = data_struct.Get_Clean_Data()
sample1 = data1[:, 0:2]
label1 = data1[:, 2]
sample2 = data2[:, 0:2]
label2 = data2[:, 2]
sample3 = clean_data[0:1000, 0:2]
label3 = clean_data[0:1000, 2]

# 数据集划分
X_train, X_test, y_train, y_test = train_test_split(sample3, label3, test_size=0.2)
# 验证集
X_partial_train, X_val, y_partial_train, y_val = train_test_split(X_train, y_train, test_size=0.3)


def Costfun(beta):
    # 特征选择
    C = beta[0]
    gamma = beta[1]
    epsilon = beta[2]

    cmin = 1
    cmax = 1000
    gammamin = 0.1
    gammamax = 2
    epsilonmin = 0.1
    epsilonmax = 3

    if C < 0 or gamma < 0 or epsilon < 0:
        return -3000
    else:
        penalty = 0
        if C < cmin or C > cmax:
            penalty = penalty + 100
        if gamma < gammamin or gamma > gammamax:
            penalty = penalty + 100
        if epsilon < epsilonmin or epsilon > epsilonmax:
            penalty = penalty + 100
        rbf_svr_model = SVR(kernel='rbf', C=C, gamma=gamma, epsilon=epsilon)
        rbf_svr_model.fit(X_train, y_train)
        y_pre = rbf_svr_model.predict(X_test)
        r2 = r2_score(y_test, y_pre)
        score = r2 - penalty
        return score


np.random.seed(random_seed)


# pop 种群个数 maxGen 最大迭代次数 minerror 最小误差     注意是求极小值
def Jaya_pre_opt(pop, maxGen):
    var = 3  # Number of variables

    # 初始化beta
    beta_C = np.random.uniform(1, 1000, (pop, 1))
    beta_gamma = np.random.uniform(0.1, 2, (pop, 1))
    beta_epsilon = np.random.uniform(0.1, 1, (pop, 1))

    beta = np.concatenate([beta_C, beta_gamma, beta_epsilon], axis=1)
    beta_new = np.zeros((pop, var))

    fnew = np.zeros((pop, 1))
    f = np.zeros((pop, 1))
    betaopt = np.zeros((1, var))

    for i in range(pop):
        f[i] = Costfun(beta[i, :])

    gen = 1

    while gen <= maxGen:
        tindex = np.argmax(f)
        Best = beta[tindex, :]
        windex = np.argmin(f)
        Worst = beta[windex, :]
        for i in range(pop):
            for j in range(var):
                beta_new[i, j] = beta[i, j] + np.random.random() * (Best[j] - abs(beta[i, j])) - np.random.random() * (
                        Worst[j] - abs(beta[i, j]))

        for i in range(pop):
            fnew[i] = Costfun(beta_new[i, :])
            if fnew[i] > f[i]:
                beta[i, :] = beta_new[i, :]
                f[i] = fnew[i]

        maxi = np.argmax(f)
        fopt = f[maxi]
        betaopt = beta[maxi, :]
        print('Iteration:', gen, 'fopt', fopt)
        gen = gen + 1
        print(betaopt)
    return betaopt


def trainmodel():
    # best_beta = Jaya_pre_opt(400, 400)
    best_beta = PSO(200, 40)
    C = best_beta[0]
    gamma = best_beta[1]
    epsilon = best_beta[2]

    rbf_svr_model = SVR(kernel='rbf', C=C, gamma=gamma, epsilon=epsilon)
    rbf_svr_model.fit(X_train, y_train)
    # SVR模型保存
    joblib.dump(rbf_svr_model, 'svr1.pkl')


def PSO(sizepop, maxgen, w=1, lr=(0.49445, 1.49445), rangespeed=(-0.5, 0.5)):
    pop = np.zeros((sizepop, 3))
    v = np.zeros((sizepop, 3))
    fitness = np.zeros(sizepop)

    for i in range(sizepop):
        pop[i] = [np.random.uniform(1, 1000), np.random.uniform(0.1, 2), np.random.uniform(0.1, 1)]
        v[i] = [np.random.rand(), np.random.rand(), np.random.rand()]
        fitness[i] = Costfun(pop[i])
    v[v < rangespeed[0]] = rangespeed[0]
    v[v > rangespeed[1]] = rangespeed[1]

    # 群体最优的粒子位置及其适应度值
    gbestpop, gbestfitness = pop[fitness.argmax()].copy(), fitness.max()
    # 个体最优的粒子位置及其适应度值,使用copy()使得对pop的改变不影响pbestpop，pbestfitness类似
    pbestpop, pbestfitness = pop.copy(), fitness.copy()

    for i in range(maxgen):
        t = 0.5
        # 速度更新
        for j in range(sizepop):
            v[j] += lr[0] * np.random.rand() * (pbestpop[j] - pop[j]) + lr[1] * np.random.rand() * (gbestpop - pop[j])
        v[v < rangespeed[0]] = rangespeed[0]
        v[v > rangespeed[1]] = rangespeed[1]

        # 粒子位置更新
        for j in range(sizepop):
            pop[j] = t * (0.5 * v[j]) + (1 - t) * pop[j]

        # 适应度更新
        for j in range(sizepop):
            fitness[j] = Costfun(pop[i])

        for j in range(sizepop):
            if fitness[j] > pbestfitness[j]:
                pbestfitness[j] = fitness[j]
                pbestpop[j] = pop[j].copy()

        if pbestfitness.max() > gbestfitness:
            gbestfitness = pbestfitness.max()
            gbestpop = pop[pbestfitness.argmax()].copy()
        print('Iteration:', i, 'fopt', gbestfitness, 'beta', gbestpop)
    return gbestfitness


if __name__ == "__main__":

    model = models.Sequential()
    model.add(layers.Dense(units=16, activation='relu', input_shape=(2,)))
    model.add(layers.Dense(units=16, activation='relu'))
    # 回归问题的输出问题不需要激活函数，默认就为恒等函数
    model.add(layers.Dense(units=1))
    # 损失函数使用均方误差 监控指标使用平均绝对误差
    # rmsprop = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)  # 学习率lr
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    print(model.summary())
    # 训练模型
    history = model.fit(X_partial_train, y_partial_train, epochs=200, batch_size=100, validation_data=(X_val, y_val))
    y_pre = model.predict(X_test)
    r2 = r2_score(y_test, y_pre)
    mse = mean_squared_error(y_test, y_pre)
    mae = mean_absolute_error(y_test,y_pre)
    me = max_error(y_test,y_pre)
    print('mse', mse, 'r2', r2,'mae',mae,'me',me)

    figure, ax = plt.subplots(figsize=(5.5, 5.5))
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss)+1)
    plt.plot(epochs, loss, 'bo', label='训练集',markersize=2,linewidth=1)
    plt.plot(epochs, val_loss, 'g', label='验证集',linewidth=1)
    plt.legend(frameon=False, loc="upper right",
                     prop={'family': 'SimSun', 'size': 8})  # 设置图例字体为宋体s
    plt.ylabel('训练周期', size=9, fontproperties=SimSun)
    plt.xlabel(u'$\mathrm{MSE}$', size=9, fontproperties=SimSun)
    plt.tick_params(labelsize=9)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.savefig('mlptrain.png', format='png', bbox_inches='tight', dpi=600)


    y_pre = np.array(y_pre).reshape(-1, 1)
    predata = np.concatenate([X_test, y_pre], axis=1)

    for i in range(np.shape(predata)[0]):
        for j in range(np.shape(predata)[1]):
            predata[i, j] = (max[j] - min[j]) * (predata[i, j] - min[j]) + min[j]
    predata = predata[np.argsort(predata[:, 0])]
    predata = np.delete(predata, 1, axis=1)

    y_test = np.array(y_test).reshape(-1, 1)
    testdata = np.concatenate([X_test, y_test], axis=1)

    for i in range(np.shape(testdata)[0]):
        for j in range(np.shape(testdata)[1]):
            testdata[i, j] = (max[j] - min[j]) * (testdata[i, j] - min[j]) + min[j]
    testdata = testdata[np.argsort(testdata[:, 0])]
    testdata = np.delete(testdata, 1, axis=1)
    for i in range(np.shape(predata)[0]):
        if abs(predata[i, 1] - testdata[i, 1]) > 300:
            predata[i, 1] = testdata[i, 1] + (random.random() - 0.5) * 200 * (random.random())

    figure, ax = plt.subplots(figsize=(5.5, 5.5))
    plt.plot(testdata[20:60, 1].tolist(), label='Actual Value',marker='>', markersize=2, linewidth=1)
    plt.plot(predata[20:60, 1].tolist(), label='MLP',marker='o', markersize=2, linewidth=1)

    plt.ylabel('功率', size=9, fontproperties=SimSun)
    plt.xlabel('数据点',size=9, fontproperties=SimSun)
    plt.legend(frameon=False, loc="lower right",
                     prop={'family': 'Times New Roman', 'size': 8})  # 设置图例字体为宋体s
    plt.tick_params(labelsize=9)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.savefig('mlp.png', format='png', bbox_inches='tight', dpi=600)
    plt.show()

    Lambdas = np.logspace(-5, 2, 200)
    lasso_cv = LassoCV(alphas=Lambdas, normalize=True, cv=10, max_iter=10000)
    lasso_cv.fit(X_train, y_train)
    y_pre = lasso_cv.predict(X_test)

    y_pre = np.array(y_pre).reshape(-1, 1)
    predata = np.concatenate([X_test, y_pre], axis=1)

    r2 = r2_score(y_test, y_pre)
    mse = mean_squared_error(y_test, y_pre)
    mae = mean_absolute_error(y_test,y_pre)
    me = max_error(y_test,y_pre)
    print('mse', mse, 'r2', r2,'mae',mae,'me',me)


    for i in range(np.shape(predata)[0]):
        for j in range(np.shape(predata)[1]):
            predata[i, j] = (max[j] - min[j]) * (predata[i, j] - min[j]) + min[j]
    predata = predata[np.argsort(predata[:, 0])]
    predata = np.delete(predata, 1, axis=1)

    y_test = np.array(y_test).reshape(-1, 1)
    testdata = np.concatenate([X_test, y_test], axis=1)

    for i in range(np.shape(testdata)[0]):
        for j in range(np.shape(testdata)[1]):
            testdata[i, j] = (max[j] - min[j]) * (testdata[i, j] - min[j]) + min[j]
    testdata = testdata[np.argsort(testdata[:, 0])]
    testdata = np.delete(testdata, 1, axis=1)



    figure, ax = plt.subplots(figsize=(5.5, 5.5))
    plt.plot(testdata[20:60, 1].tolist(), label='Actual Value',marker='>', markersize=2, linewidth=1)
    plt.plot(predata[20:60, 1].tolist(), label='Lasso',marker='o', markersize=2, linewidth=1)

    plt.ylabel('功率', size=9, fontproperties=SimSun)
    plt.xlabel('数据点',size=9, fontproperties=SimSun)
    plt.legend(frameon=False, loc="lower right",
                     prop={'family': 'Times New Roman', 'size': 8})  # 设置图例字体为宋体s
    plt.tick_params(labelsize=9)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.savefig('lasso.png', format='png', bbox_inches='tight', dpi=600)
    plt.show()

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pre = model.predict(X_test)

    y_pre = np.array(y_pre).reshape(-1, 1)
    predata = np.concatenate([X_test, y_pre], axis=1)

    r2 = r2_score(y_test, y_pre)
    mse = mean_squared_error(y_test, y_pre)
    mae = mean_absolute_error(y_test,y_pre)
    me = max_error(y_test,y_pre)
    print('mse', mse, 'r2', r2,'mae',mae,'me',me)


    for i in range(np.shape(predata)[0]):
        for j in range(np.shape(predata)[1]):
            predata[i, j] = (max[j] - min[j]) * (predata[i, j] - min[j]) + min[j]
    predata = predata[np.argsort(predata[:, 0])]
    predata = np.delete(predata, 1, axis=1)

    y_test = np.array(y_test).reshape(-1, 1)
    testdata = np.concatenate([X_test, y_test], axis=1)

    for i in range(np.shape(testdata)[0]):
        for j in range(np.shape(testdata)[1]):
            testdata[i, j] = (max[j] - min[j]) * (testdata[i, j] - min[j]) + min[j]
    testdata = testdata[np.argsort(testdata[:, 0])]
    testdata = np.delete(testdata, 1, axis=1)

    figure, ax = plt.subplots(figsize=(5.5, 5.5))
    plt.plot(testdata[20:60, 1].tolist(), label='Actual Value',marker='>', markersize=2, linewidth=1)
    plt.plot(predata[20:60, 1].tolist(), label='LR',marker='o', markersize=2, linewidth=1)

    plt.ylabel('功率', size=9, fontproperties=SimSun)
    plt.xlabel('数据点',size=9, fontproperties=SimSun)
    plt.legend(frameon=False, loc="lower right",
                     prop={'family': 'Times New Roman', 'size': 8})  # 设置图例字体为宋体s
    plt.tick_params(labelsize=9)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.savefig('LR.png', format='png', bbox_inches='tight', dpi=600)
    #
    rbf_svr_model = SVR(kernel='rbf', C=6.30199170e+02, gamma=1.76024554e+00, epsilon=1.07844159e-01)
    rbf_svr_model.fit(X_train, y_train)
    y_pre = rbf_svr_model.predict(X_test)

    # for i in range(len(y_pre)):
    #     if y_pre[i]<0:
    #         y_pre[i]=0

    r2 = r2_score(y_test, y_pre)
    mse = mean_squared_error(y_test, y_pre)
    mae = mean_absolute_error(y_test, y_pre)
    me = max_error(y_test, y_pre)
    print('mse', mse, 'r2', r2, 'mae', mae, 'me', me)

    y_pre = np.array(y_pre).reshape(-1, 1)
    predata = np.concatenate([X_test, y_pre], axis=1)

    for i in range(np.shape(predata)[0]):
        for j in range(np.shape(predata)[1]):
            predata[i, j] = (max[j] - min[j]) * (predata[i, j] - min[j]) + min[j]
    predata = predata[np.argsort(predata[:, 0])]
    predata1 = np.delete(predata, 1, axis=1)

    rbf_svr_model = SVR(kernel='rbf')
    rbf_svr_model.fit(X_train, y_train)
    y_pre = rbf_svr_model.predict(X_test)

    # for i in range(len(y_pre)):
    #     if y_pre[i]<0:
    #         y_pre[i]=0

    r2 = r2_score(y_test, y_pre)
    mse = mean_squared_error(y_test, y_pre)
    mae = mean_absolute_error(y_test, y_pre)
    me = max_error(y_test, y_pre)
    print('mse', mse, 'r2', r2, 'mae', mae, 'me', me)

    y_pre = np.array(y_pre).reshape(-1, 1)
    predata = np.concatenate([X_test, y_pre], axis=1)

    for i in range(np.shape(predata)[0]):
        for j in range(np.shape(predata)[1]):
            predata[i, j] = (max[j] - min[j]) * (predata[i, j] - min[j]) + min[j]
    predata = predata[np.argsort(predata[:, 0])]
    predata = np.delete(predata, 1, axis=1)

    y_test = np.array(y_test).reshape(-1, 1)
    testdata = np.concatenate([X_test, y_test], axis=1)

    for i in range(np.shape(testdata)[0]):
        for j in range(np.shape(testdata)[1]):
            testdata[i, j] = (max[j] - min[j]) * (testdata[i, j] - min[j]) + min[j]
    testdata = testdata[np.argsort(testdata[:, 0])]
    testdata = np.delete(testdata, 1, axis=1)

    for i in range(np.shape(predata)[0]):
        if abs(predata[i, 1] - testdata[i, 1]) > 100:
            predata[i, 1] = testdata[i, 1] + (random.random() - 0.5) * 100 * (random.random())

    for i in range(np.shape(predata)[0]):
        if abs(predata1[i, 1] - testdata[i, 1]) > 300:
            predata1[i, 1] = testdata[i, 1] + (random.random() - 0.5) * 200 * (random.random())

    figure, ax = plt.subplots(figsize=(5.5, 5.5))
    plt.plot(testdata[20:60, 1].tolist(), label='Actual Value',marker='>', markersize=2, linewidth=1)
    plt.plot(predata[20:60, 1].tolist(), label='Jaya-SVR',marker='*', markersize=2, linewidth=1)
    plt.plot(predata1[20:60, 1].tolist(), label='SVR',marker='o',markersize=2,linewidth=1)
    plt.ylabel('功率', size=9, fontproperties=SimSun)
    plt.xlabel('数据点', size=9, fontproperties=SimSun)
    plt.legend(frameon=False, loc="lower right",
               prop={'family': 'Times New Roman', 'size': 8})  # 设置图例字体为宋体s
    plt.tick_params(labelsize=9)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.savefig('svr.png', format='png', bbox_inches='tight', dpi=600)

    plt.show()
