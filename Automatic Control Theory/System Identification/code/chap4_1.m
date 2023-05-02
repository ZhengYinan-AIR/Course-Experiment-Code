clear all
close all;

%%%%%%%%%产生仿真数据%%%%%%%%%%
n=2;
total=1000;
sigma=0.1;   %噪声变量的均方根
 
 
%M序列作为输入
z1=1;z2=1;z3=1;z4=0;
for i=1:total
    x1=xor(z3,z4);
    x2=z1;
    x3=z2;
    x4=z3;
    z(i)=z4;;
    if z(i)>0.5 
        u(i)=-1;
    else u(i)=1;
    end
    z1=x1;z2=x2;z3=x3;z4=x4;
end
figure(1);
stem(u),grid on
%%%%%%%%%%系统输出%%%%%%%%%%%%
y(1)=0;y(2)=0;
v=sigma*randn(total,1);  %噪声
y(1)=1;y(2)=0.01;
for k=3:total
    y(k)=0.5*y(k-1)+0.2*y(k-2)+u(k-1)+1.5*u(k-2)+v(k)-0.8*v(k-1)+0.3*v(k-2);
end
%%%%%%%%%初始化%%%%%%%%%%%%%%%%%%
theta0=0.001*ones(6,1);                      %参数
e1(1)=-0.5-theta0(1);   e2(1)=-0.2-theta0(2);   %误差初始化
e3(1)=1.0-theta0(3);    e4(1)=1.5-theta0(4);
e5(1)=-0.8-theta0(5);   e6(1)=0.3-theta0(6);
a_hat(1)=theta0(1);a_hat(2)=theta0(2);       %参数分离
b_hat(1)=theta0(3);b_hat(2)=theta0(4);
c_hat(1)=theta0(5);c_hat(2)=theta0(6);
  
P0=eye(6,6);                                %矩阵P初始化 
 for i=1:n
    yf(i)=0.1;uf(i)=0.1;vf(i)=0.1;
    fai0(i,1)=-yf(i);
    fai0(n+i,1)=-uf(i);
    fai0(2*n+i,1)=-vf(i);
 end
 e(1)=1.0;
 e(2)=1.0;
 
%%%% 递推算法%%%%%%%%%%%%
for i=n+1:total
  pusai=[-y(i-1);-y(i-2);u(i-1);u(i-2);e(i-1);e(i-2)];    
 
  C=zeros(n*3,n*3);
  Q=zeros(3*n,1);          
  Q(1)=-y(i-1);
  Q(n+1)=u(i-1);
  Q(2*n+1)=e(i-1);
   for j=1:n                 
       C(1,j)=c_hat(j);
       C(n+1,n+j)=c_hat(j);
       C(2*n+1,2*n+j)=c_hat(j);
       if j>1
         C(j,j-1)=1.0;
         C(n+j,n+j-1)=1.0;
         C(2*n+j,2*n+j-1)=1.0;
       end        
   end
   fai=C*fai0+Q;
   K=P0*fai*inv(fai'*P0*fai+1);
   P=[eye(6,6)-K*fai']*P0;
 
   e(i)=y(i)-pusai'*theta0;
   theta=theta0+K*e(i); 
  
   P0=P;
   theta0=theta;
   fai0=fai;
    a_hat(1)=theta(1);a_hat(2)=theta(2);
    b_hat(1)=theta(3);b_hat(2)=theta(4);
    c_hat(1)=theta(5);c_hat(2)=theta(6);
    
    e1(i)=-0.5-a_hat(1);  e2(i)=-0.2-a_hat(2);
    e3(i)=1.0-b_hat(1);   e4(i)=1.5-b_hat(2);
    e5(i)=-0.8-c_hat(1);  e6(i)=0.3-c_hat(2);
    
end
 
figure(2)
plot(e1);
hold on
plot(e2);
hold on
plot(e3);
hold on 
plot(e4);
hold on 
plot(e5);
hold on
plot(e6);
title('Parameter Estimation Error ');
xlabel('times');
ylabel('error');
hold off
figure(3)
plot(e);
title('Output Error ');
xlabel('times');
ylabel('error');