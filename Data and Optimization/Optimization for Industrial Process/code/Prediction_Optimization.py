# -*- coding: utf-8 -*-
"""
@author: zyn
"""
import joblib
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import numpy as np
from sklearn.svm import SVR
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import Data_prepare as Dp
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

random_seed = 13

data_struct = Dp.ROP_Data()
data = data_struct.Get_Clean_Filter_Data()
# data = data_struct.Get_Data()

sample = np.delete(data, [3, 5, 6], axis=1)
label = data[:, 6]
scaler = StandardScaler()  # 标准化转换
scaler.fit(sample)
sample = scaler.transform(sample)

# scaler = StandardScaler()  # 标准化转换
# scaler.fit(data)
# data = scaler.transform(data)
# sample = np.delete(data, [3, 5, 6], axis=1)
# label = data[:, 6]

# 数据集划分
X_train, X_test, y_train, y_test = train_test_split(sample, label, test_size=0.3, random_state=40)

# 数据集掷乱
X_train, y_train = shuffle(X_train, y_train, random_state=13)


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
    best_beta = Jaya_pre_opt(400, 400)
    C = best_beta[0]
    gamma = best_beta[1]
    epsilon = best_beta[2]

    rbf_svr_model = SVR(kernel='rbf', C=C, gamma=gamma, epsilon=epsilon)
    rbf_svr_model.fit(X_train, y_train)
    # SVR模型保存
    joblib.dump(rbf_svr_model, 'svr1.pkl')


mean = scaler.mean_
scale = scaler.scale_


# 最大化钻速，处理约束
def MaxROP(Depth, WOB, RPM, Q, model):
    WOB_min = 1.0
    WOB_max = 23.14
    RPM_min = 88.0
    RPM_max = 102
    Q_min = 15.5
    Q_max = 18.0
    ROP_min = 0.0
    ROP_max = 5.0
    K = 1657.45
    T = 200.0
    C1 = 2.0
    h = 0.0
    D2 = 5.59
    D1 = 0.0162
    Af = 7.8805e-4
    a1 = 0.5
    a2 = 2.18e-5
    input = [Depth, WOB, RPM, Q]
    for i in range(4):
        input[i] = (input[i] - mean[i]) / scale[i]
    input = np.array(input).reshape(1, -1)
    ROP = model.predict(input)

    if WOB >= WOB_max or WOB <= WOB_min:
        WOB_param = -100
    else:
        WOB_param = 0.0

    if RPM >= RPM_max or RPM <= RPM_min:
        RPM_param = -100
    else:
        RPM_param = 0.0

    if Q >= Q_max or Q <= Q_min:
        Q_param = -100
    else:
        Q_param = 0.0

    if ROP >= ROP_max or ROP <= ROP_min:
        ROP_param = -100
    else:
        ROP_param = 0.0

    if WOB == WOB_max and RPM == RPM_max:
        P_param = -100
    else:
        P_param = 0.0

    if WOB * RPM >= K:
        K_param = -100
    else:
        K_param = 0.0

    if (Af * (a1 * RPM + a2 * pow(RPM, 3))) == 0:
        Tf = 100.0
    else:
        Tf = ((C1 / 2 + 1) - ((C1 * pow(h, 2)) / 2 + h)) * (D2 - D1 * WOB) / (Af * (a1 * RPM + a2 * pow(RPM, 3)))

    if Tf < T:
        T_param = -100.0
    else:
        T_param = 0.0

    # Penalty = WOB_param * WOB + RPM_param * RPM + Q_param * Q + ROP_param * ROP + K_param * WOB * RPM + P_param *
    # WOB * RPM + T_param * T_param
    Penalty = WOB_param + RPM_param + Q_param + ROP_param + K_param + P_param + T_param

    return ROP + Penalty


# pop 种群个数 maxGen 最大迭代次数 minerror 最小误差     注意是求极小值
def Jaya_opt(pop, maxGen, Depth, model):
    var = 3  # Number of variables

    # 初始化beta
    beta_WOB = np.random.uniform(1, 23.14, (pop, 1))
    beta_RPM = np.random.uniform(88, 102, (pop, 1))
    beta_Q = np.random.uniform(15.5, 18, (pop, 1))

    beta = np.concatenate([beta_WOB, beta_RPM, beta_Q], axis=1)
    beta_new = np.zeros((pop, var))

    fnew = np.zeros((pop, 1))
    f = np.zeros((pop, 1))
    betaopt = np.zeros((1, var))

    for i in range(pop):
        f[i] = MaxROP(Depth, beta[i, 0], beta[i, 1], beta[i, 2], model)

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
            fnew[i] = MaxROP(Depth, beta_new[i, 0], beta_new[i, 1], beta_new[i, 2], model)
            if fnew[i] > f[i]:
                beta[i, :] = beta_new[i, :]
                f[i] = fnew[i]

        maxi = np.argmax(f)
        fopt = f[maxi]
        # betaopt = beta[maxi, :]
        gen = gen + 1
        # print(betaopt)
    return fopt


def PSO(sizepop, maxgen, Depth, Model, w=1, lr=(0.49445, 1.49445), rangespeed=(-0.5, 0.5)):
    pop = np.zeros((sizepop, 3))
    v = np.zeros((sizepop, 3))
    fitness = np.zeros(sizepop)

    for i in range(sizepop):
        pop[i] = [np.random.uniform(1, 23.14), np.random.uniform(88, 102), np.random.uniform(15.5, 18)]
        v[i] = [np.random.rand(), np.random.rand(), np.random.rand()]
        fitness[i] = MaxROP(Depth, pop[i, 0], pop[i, 1], pop[i, 2], Model)
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
            fitness[j] = MaxROP(Depth, pop[i, 0], pop[i, 1], pop[i, 2], Model)

        for j in range(sizepop):
            if fitness[j] > pbestfitness[j]:
                pbestfitness[j] = fitness[j]
                pbestpop[j] = pop[j].copy()

        if pbestfitness.max() > gbestfitness:
            gbestfitness = pbestfitness.max()
            gbestpop = pop[pbestfitness.argmax()].copy()

        return gbestfitness


def SA(Depth, Model, L=200, S=0.01,T=100,K = 0.999,YZ = 1e-2):
    D = 3  # 变量维数
    min = [1.0,88,15.5]
    max = [23.14,102,18]
    next = [np.random.uniform(1, 23.14),np.random.uniform(88, 102),np.random.uniform(15.5, 18)]
    pre = [np.random.uniform(1, 23.14),np.random.uniform(88, 102),np.random.uniform(15.5, 18)]
    prebest = pre  # t时刻的全局最优X
    best = next

    deta = 100
    gen = 1
    while T>0.1 and deta>YZ:  # 如果能量差大于允许能量差 或者温度大于阈值
        print('gen',gen,'T',T,'deta',deta)
        T = K * T  # 降温
        gen = gen + 1
        # 在当前温度T下迭代次数
        for j in range(L):  #
            # 在此点附近随机选下一点
            for i in range(D):
                next[i] = pre[i]+S*(np.random.uniform(-1,1) * (max[i] - min[i]))
                while next[i] > max[i] or next[i] < min[i]:
                    next[i] = pre[i]+S*(np.random.uniform(-1,1) * (max[i] - min[i]))
            # ===是否全局最优解 ===
            if MaxROP(Depth,best[0],best[1],best[2],Model) < MaxROP(Depth,next[0],next[1],next[2],Model):
                prebest = best
                # 此为新的最优解
                best = next

            # ====Metropolis过程====
            if MaxROP(Depth,next[0],next[1],next[2],Model)>MaxROP(Depth,pre[0],pre[1],pre[2],Model):  # 后一个比前一个好
                # 接受新解
                pre = next
            else:
                changer = -1 * (MaxROP(Depth,pre[0],pre[1],pre[2],Model)-MaxROP(Depth,next[0],next[1],next[2],Model)) / T
                p1 = np.exp(changer)
                # 接受较差的解
                if p1 > np.random.random():
                    pre = next
        deta = np.abs(MaxROP(Depth, best[0], best[1], best[2], Model) - MaxROP(Depth, prebest[0], prebest[1], prebest[2], Model))
    return MaxROP(Depth,best[0],best[1],best[2],Model)


if __name__ == "__main__":
    # trainmodel()  # 已训练
    # data_struct.Print_Data()
    # SVR模型加载
    svr = joblib.load('svr1.pkl')

    # SVR模型测试
    y_hat = svr.predict(X_test)
    y_train_hat = svr.predict(X_train)
    mse_jayasvr_nf = mean_squared_error(y_test, y_hat)
    r2_jayasvr_nf = r2_score(y_test, y_hat)
    print('mse', mse_jayasvr_nf, 'r2', r2_jayasvr_nf)

    # plt.figure(8)
    # plt.plot(y_hat)
    # plt.plot(y_test)
    # plt.xlabel('Data Point')
    # plt.ylabel('ROP(m/s)')
    # plt.legend(['Jaya-SVR', 'True'])
    # plt.title("Jaya-SVR-Prediction")  # 标题
    # plt.show()
    #
    # plt.figure(9)
    # plt.plot(y_train_hat)
    # plt.plot(y_train)
    # plt.legend(['Jaya-SVR', 'True'])
    # plt.title("Jaya-SVR-train")  # 标题
    # plt.show()

    # 根据优化目标和约束条件最大化转速
    optdata = data_struct.Get_Clean_Filter_Data()
    depthdata = optdata[:, 0]
    ROP_act = optdata[:, 6]
    ROP_opt = []
    j = 1
    for i in depthdata:
        # ROP = Jaya_opt(200, 200, i, svr)
        ROP = PSO(200, 200, i, svr)
        #ROP = SA(i,svr)
        ROP_opt.append(ROP)
        # ROP_opt.append(ROP[0])

        print('Iteration:', j, 'fopt', ROP)
        j = j + 1
    plt.figure(2)
    plt.plot(depthdata, ROP_act)
    plt.plot(depthdata, ROP_opt)
    plt.legend(['ROP_act', 'ROP_opt'])
    plt.title("Optimization")  # 标题
    plt.show()
    # 保存文件
    dataframe = pd.DataFrame({'Depth': depthdata, 'actual value': ROP_act, 'Jaya': ROP_opt})
    dataframe.to_csv("OPTsa1.csv")


    dataframe = pd.read_csv('OPT.csv')
    depthdata = np.array(dataframe['Depth'])
    actualvalue = np.array(dataframe['actual value'])
    jayadata = np.array(dataframe['Jaya'])
    psodata = np.array(np.array(dataframe['pso']))
    plt.figure(10)
    plt.plot(actualvalue,depthdata)
    plt.plot(jayadata,depthdata)
    plt.plot(psodata,depthdata)
    # plt.plot(depthdata, actualvalue)
    # plt.plot(depthdata, jayadata)
    # plt.plot(depthdata, psodata)
    plt.legend(['actual value', 'Jaya','PSO'])
    plt.xlabel('ROP(m/s)')
    plt.ylabel('Depth')
    plt.title("Optimization Result")  # 标题
    plt.show()

