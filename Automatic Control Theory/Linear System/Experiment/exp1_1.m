%第一部分建模部分：作业一利用Matlab给出系统的传递函数模型、状态空间模型


clc
clear
%负反馈单位J1取1，Kn取1
num1=[0 1];
den1=[1 0];
num2=[0 1];
den2=[1 0];

[num_s,den_s]=feedback(num1,den1,num2,den2,-1)

%串联单位Kp取1，K1取1
num3=[1 1];
den3=[1 0];

[num_s,den_s]=series(num3,den3,num_s,den_s)

%将上述单位负反馈

num4=[0,1];
den4=[0 1];

[num_s,den_s]=feedback(num_s,den_s,num4,den4,-1)

%总串联Kb取1,J2取1

num5=[0 1];
den5=[1 1];
num6=[0 0 1];
den6=[1 0 0];

[num_s,den_s]=series(num5,den5,num_s,den_s)
[num_s,den_s]=series(num6,den6,num_s,den_s)

sys1=tf(num_s,den_s)
[A,B,C,D]=tf2ss(num_s,den_s)

%总负反馈

num7=[0 1];
den7=[0 1];

[num_s,den_s]=feedback(num_s,den_s,num7,den7,-1)

sys2=tf(num_s,den_s)
[A,B,C,D]=tf2ss(num_s,den_s)






