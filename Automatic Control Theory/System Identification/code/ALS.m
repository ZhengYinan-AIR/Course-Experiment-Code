% clear all
% close all
% clc

% M序列、噪声信号产生及其显示程序 
L=60;%四位移位积存器产生的M序列的周期
y1=1;y2=1;y3=1;y4=0;
for i=1:L;
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
stem(u),grid on%画出M序列输入信号
randn('seed',100)
v=randn(1,60); %产生一个N（0,1）的随机噪声
v = v*sqrt(0.5)
%增广递推最小二乘辨识
z(2)=0;z(1)=0;
theat0=[0.001 0.001 0.001 0.001 0.001 0.001 0.001]';%直接给出被辨识参数的初始值,即一个充分小的实向量
p0=10^4*eye(7,7);%初始状态P0
theat444=[theat0,zeros(7,59)];%被辨识参数矩阵的初始值及大小
e=zeros(4,60);%相对误差的初始值及大小
for k=3:60; 
    z(k)=-1.6*z(k-1)-0.7*z(k-2)+u(k-1)+0.4*u(k-2)+1.1*v(k)+1.4*v(k-1)+0.3*v(k-2);
    h1=[-z(k-1),-z(k-2),u(k-1),u(k-2),v(k),v(k-1),v(k-2)]';
    x=h1'*p0*h1+1;
    x1=inv(x); 
    k1=p0*h1*x1; %K
    d1=z(k)-h1'*theat0; 
    theat1=theat0+k1*d1;%辨识参数c 
    theat0=theat1;%给下一次用
    theat444(:,k)=theat1;%把辨识参数c 列向量加入辨识参数矩阵 
    
    p1=p0-k1*k1'*[h1'*p0*h1+1];%find p(k)
    p0=p1;%给下次用
   end%循环结束


%分离变量
    a1=theat444(1,:); a2=theat444(2,:); b1=theat444(3,:); b2=theat444(4,:);
    c1=theat444(5,:); c2=theat444(6,:); c3=theat444(7,:); 
    ea1 = 1.6-a1;
    ea2 = 0.7-a2;
    eb1 = 1-b1;
    eb2 = 0.4-b2;
    ec1 = 1.1-c1;
    ec2 = 1.4-c2;
    ec3 = 0.3-c3;
    theataa444 = [ea1;ea2;eb1;eb2;ec1;ec2;ec3];
    
i=1:60;    
figure(4)
%createfigure(i,theat,theataa)
% figure(3)
subplot(2,2,2)
plot(i,a1,'r',i,a2,'b',i,b1,'k',i,b2,'y',i,c1,'g',i,c2,'c',i,c3,'m')%画出各个被辨识参数
title('N(0,0.5)白噪声增广递推最小二乘辨识方法')%标题
grid on
subplot(2,2,3)
i=1:60; 
plot(i,ea1,i,ea2,i,eb1,i,eb2,i,ec1,i,ec2,i,ec3) %画出辨识结果的收敛情况
legend('a1','a2','b1','b2','c1','c2','c3');
title('N(0,0.5)白噪声辨识精度')
grid on

