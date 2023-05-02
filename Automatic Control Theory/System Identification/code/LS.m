clear all
close all
clc
randn('seed',100)
v=randn(1,16);
%v = v.*sqrt(0.1);
%v = v.*sqrt(0.5);
L=15;
y1=1;y2=1;y3=1;y4=0;
%M序列
for i=1:L
    x1=xor(y3,y4);
    x2=y1;
    x3=y2;
    x4=y3;
    y(i)=y4;
    if y(i)>0.5,u(i)=-1;
    else u(i)=1;
    end
    y1=x1;y2=x2;y3=x3;y4=x4;
end
figure(1);
stem(u),grid on
title('输入信号M序列');
%最小辨识程序
z=zeros(1,16);
for k=3:16
    z(k)=-1.6*z(k-1)-0.7*z(k-2)+u(k-1)+0.4*u(k-2)+1*v(k);   %求系统不同时刻的输出
end
figure(2);
plot([1:16],z);
title('输出观测值')
grid on
figure(3);
stem(z),grid on
title('输出观测值z的经线图形');
grid on
H=[-z(2) -z(1) u(2) u(1);-z(3) -z(2) u(3) u(2);-z(4) -z(3) u(4) u(3);-z(5) -z(4) u(5) u(4);
   -z(6) -z(5) u(6) u(5); -z(7) -z(6) u(7) u(6);-z(8) -z(7) u(8) u(7);-z(9) -z(8) u(9) u(8);
   -z(10) -z(9) u(10) u(9);-z(11) -z(10) u(11) u(10);-z(12) -z(11) u(12) u(11);
 -z(13) -z(12) u(13) u(12);-z(14) -z(13) u(14) u(13);-z(15) -z(14) u(15) u(14)];
Z=[z(3);z(4);z(5);z(6);z(7);z(8);z(9);z(10);z(11);z(12);z(13);z(14);z(15);z(16)]
% 求解系数矩阵
c=inv(H'*H)*H'*Z;
disp("估计参数值为")
a1=c(1),a2=c(2),b1=c(3),b2=c(4)
disp("存在估计误差")
a1e=1.6-a1
a2e=0.7-a2
b1e=1.0-b1
b2e=0.4-b2


