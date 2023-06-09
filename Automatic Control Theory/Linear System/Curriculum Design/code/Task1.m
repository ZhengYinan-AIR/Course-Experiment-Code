clear
clc

M = 1;
m = 0.1;
l = 0.5;
g = 9.8;

%%
% 1.线性模型建立
A = [0,1,0,0;0,0,-m*g/M,0;0,0,0,1;0,0,(M+m)*g/(M*l),0];
b = [0;1/M;0;-1/(M*l)];
c = [1,0,0,0];
d = 0;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P13 给出对应的传递函数模型
[num,den] = ss2tf(A,b,c,d);
G = tf(num,den);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%
% 2.分析
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P16 基于传递函数模型分析稳定性，基于传递函数模型分析性能
% 2.1绘制G零极点图
figure(1)
pzmap(G)

% 2.2 绘制G伯德图,并输出性能，计算幅值裕度、相角裕度、截止频率
figure(2)
bode(num,den)
[Gm,Pm,Wcp,wcgain] = margin(G)

% 2.3绘制GNyquist曲线
figure(3)
nyquist(G)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P16 基于状态空间模型分析状态稳定性，写了多种方法，只展示了一种其余注释
% 2.4李氏方法
% 2.4.1判断特征根
Lambda = eig(A);
judge = real(Lambda)<0;
if(all(judge(:)==1))
    disp("系统稳定")
else
    disp("系统不稳定")
end

% 2.4.2 直接法：正能量是否衰减?
% P = eye(size(A,1));
% Q = -P*A-A'*P;
% Lambda1 = eig(Q)
% judge1 = real(Lambda1)>0
% if(all(judge1(:)==1))
%     disp("系统稳定")
% else
%     disp("系统不稳定")
% end

% 2.4.3 指定Q反求P
%注意A要转置，不转置也可以，求特征值或者顺序主子式效果一样
% A = A';
% Q = eye(size(A,1));
% P = lyap(A,Q);
% Lambda2 = eig(Q);
% judge2 = real(Lambda2)>0
% if(all(judge2(:)==1))
%     disp("系统稳定")
% else
%     disp("系统不稳定")
% end

% 2.4.4 YALMIP toolbox, LMI:线性矩阵不等式
% P = sdpvar(size(A,1),size(A,1),'symmetric');%建立矩阵
% Fcond = [P>0,A'*P+P*A<0];%待求解LMI
% 
% ops = sdpsettings('verbose',0,'solver','sedumi');
% diagnostics = solvesdp(Fcond,[],ops);
% [m,p] = checkset(Fcond);
% tmin = min(m);
% %残差为正代表解可行即存在P
% if tmin>0
%     disp('系统稳定')
% else
%     disp('系统不稳定')
% end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P16 绘制开环系统响应曲线
% 2.5单位阶跃响应
sys = ss(A, b, c, d);
t=0: 0.01: 5;
[y, t, x] = step(sys, t);
figure(4)
subplot(2, 2, 1);
plot(t, x(:,1)); grid
xlabel('t(s)'); ylabel('x_1');
subplot(2, 2, 2);
plot(t, x(:, 2)); grid
xlabel('t(s)'); ylabel('x_2');
subplot(2, 2, 3);
plot(t, x(:, 3)); grid
xlabel('t(s)'); ylabel('x_3');
subplot(2, 2, 4);
plot(t, x(:, 4)); grid
xlabel('t(s)'); ylabel('x_4');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P17 分析系统的能控性能观性，采用秩判据和约旦标准型判定
% 2.6 能控能观判断
% 2.6.1秩判据
Qc = ctrb(A, b);
Qo = obsv(A, c);
rc = rank(Qc);
ro = rank(Qo);
L = size(A);
if rc == L
    str = '系统能控'
else
    str = '系统不能控'
end
if ro == L
    str = '系统能观'
else 
    str = '系统不能观'
end

% 2.6.2约旦标准型判断
[V,J] = jordan(A);
T = inv(V);
[An,Bn,Cn,Dn] = ss2ss(A,b,c,d,T);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%
% 3 设计
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P19 设计状态反馈控制器
% 3.1 设计状态反馈控制器
disp('原系统特征根如下：')
eig(A)
P1 = [-1 -3 -4 -5];
K = place(A,b,P1);
ABK=A-b*K;
%%配置检验
disp('经过状态反馈后，系统特征根如下：')
eig(A-b*K)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P20 设计状态观测器的状态反馈
% 3.2 设计状态跟随器
P2 = [-5 -5 -5 -5];
a1 = A';
b1 = c';
K2 = acker(a1,b1,P2) ;
G = K2';
AGC = A-G*c;
disp('经过状态观测器反馈后，系统特征根如下：')
eig(A-G*c)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% 3.3 设计位移跟随
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P21 引入单位增益比例输出反馈的状态反馈
% 3.3.1 单位增益输出反馈
%系统镇定设计但是存在稳态误差，可以直接拿之前状态反馈矩阵减去c即可
KH = K-c;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P22 引入积分校正，给定超调量和过渡时间
% 3.3.2 积分项输出反馈
% %配置主导极点
%设置超调量为10%
syms k wn
k = solve(exp(-pi*k/sqrt(1-k*k))==0.10, k);
k = double(k)
%设置调节时间为3s
wn = solve(3/(max(k)*wn)==3, wn);
wn = double(wn)
%G=tf([wn*wn],[1 2*max(k)*wn wn*wn]);
[z, p, k]=tf2zp([1], [1/(wn*wn), 2*max(k)/wn, 1]);
sys1 = zpk(z, p, k);
disp('主导极点：')
p%主导极点
% 带积分项
p = [-1.0000-1.3644i -1.0000+1.3644i  -6  -6 -6];
AH = zeros(5,5);
AH(1:4,1:4) = A;
AH(5,1:4) = -c;
BH = zeros(5,1);
BH(1:4,1) = b;
K3 = acker(AH,BH,p);
ABK2=AH-BH*K3;
%%配置检验
disp('经过状态反馈后，带积分项系统特征根如下：')
eig(ABK2)
KH1 = K3(1,1:4);
KH2 = -K3(1,5);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P23 基于状态观测器添加积分矫正，K，G矩阵可以直接使用以上求得矩阵进行搭建
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%s