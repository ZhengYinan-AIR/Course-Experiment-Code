%��һ���ֽ�ģ���֣���ҵһ����Matlab����ϵͳ�Ĵ��ݺ���ģ�͡�״̬�ռ�ģ��


clc
clear
%��������λJ1ȡ1��Knȡ1
num1=[0 1];
den1=[1 0];
num2=[0 1];
den2=[1 0];

[num_s,den_s]=feedback(num1,den1,num2,den2,-1)

%������λKpȡ1��K1ȡ1
num3=[1 1];
den3=[1 0];

[num_s,den_s]=series(num3,den3,num_s,den_s)

%��������λ������

num4=[0,1];
den4=[0 1];

[num_s,den_s]=feedback(num_s,den_s,num4,den4,-1)

%�ܴ���Kbȡ1,J2ȡ1

num5=[0 1];
den5=[1 1];
num6=[0 0 1];
den6=[1 0 0];

[num_s,den_s]=series(num5,den5,num_s,den_s)
[num_s,den_s]=series(num6,den6,num_s,den_s)

sys1=tf(num_s,den_s)
[A,B,C,D]=tf2ss(num_s,den_s)

%�ܸ�����

num7=[0 1];
den7=[0 1];

[num_s,den_s]=feedback(num_s,den_s,num7,den7,-1)

sys2=tf(num_s,den_s)
[A,B,C,D]=tf2ss(num_s,den_s)






