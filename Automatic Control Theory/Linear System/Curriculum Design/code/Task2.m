clc
clear

a = 9;
b = 14.28;
c = 1;
m0 = -1/7;
m1 = 2/7;
A = [-a*m1, a, 0;
    1, -1, 1;
    0, -b, 0];
H = [-a*(m0-m1); 0; 0];
C = [1, 0, 0];
D = C;
W = 1;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 实验指导书P33 35 36,用YALMP求解LMI
P = sdpvar(3,3,'symmetric');
V = sdpvar(3,1,'full');
T = sdpvar(1,1,'symmetric');
Z = [P*A-V*C+A'*P-C'*V', P*H+D'*W*T;
    T'*W'*D+H'*P, -2*T];
Fcond = [P>=0, T>=0, Z<=0];
ops = sdpsettings('verbose',0,'solver','sedumi');
diagnostics = solvesdp(Fcond, [], ops);
[m, p] = checkset(Fcond);
tmin = min(m);
if tmin > 0
    disp('system is stable');
    P = double(P);
    V = double(V);
    K = inv(P)*V
else
    disp('system is unstable');
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%