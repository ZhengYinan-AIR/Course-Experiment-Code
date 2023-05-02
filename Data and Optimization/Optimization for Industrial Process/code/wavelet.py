import pywt
import numpy as np
import math


# sgn函数构建
def sgn(num):
    if num > 0.0:
        return 1.0
    elif num == 0.0:
        return 0.0
    else:
        return -1.0


# 小波去噪函数构建
def wavelet_noising(new_df):
    data = new_df
    data = data.T.tolist()
    # print(np.size(data))
    w = pywt.Wavelet('dB10')  # 选择dB10小波基
    ca1, cd1 = pywt.wavedec(data, w, level=1)  # 3层小波分解
    length1 = len(cd1)
    length0 = len(data)

    abs_cd1 = np.abs(np.array(cd1))
    median_cd1 = np.median(abs_cd1)

    sigma = (1.0 / 0.6745) * median_cd1
    lamda = sigma * math.sqrt(2.0 * math.log(float(length0), math.e))
    usecoeffs = [ca1]

    # 软阈值方法
    for k in range(length1):
        if abs(cd1[k]) >= lamda / np.log2(2):
            cd1[k] = sgn(cd1[k]) * (abs(cd1[k]) - lamda / np.log2(2))
        else:
            cd1[k] = 0.0

    usecoeffs.append(cd1)
    recoeffs = pywt.waverec(usecoeffs, w)  # 信号重构
    if recoeffs.shape[0]==new_df.shape[0]:
        return recoeffs
    else:
        return recoeffs[0:-1]
