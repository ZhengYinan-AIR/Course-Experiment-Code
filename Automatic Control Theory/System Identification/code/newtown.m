clear all
close all;

%%%%%%%%%产生仿真数据%%%%%%%%%%
n=2;
total=10;
sigma=0.1;   %噪声变量的均方根
N = 200;
 
%M序列作为输入
z1=1;z2=1;z3=1;z4=0;
for i=1:total+2
    x1=xor(z3,z4);
    x2=z1;
    x3=z2;
    x4=z3;
    z(i)=z4;
    if z(i)>0.5
        u(i)=-1;
    else
        u(i)=1;
    end
    z1=x1;z2=x2;z3=x3;z4=x4;
end
%figure(1);
%stem(u),grid on
%%%%%%%%%%系统输出%%%%%%%%%%%%
y(1)=0;y(2)=0;
epsi=sigma*randn(N+3,1);  %噪声
y(1)=1;y(2)=0.01;
for k=3:total+2
    y(k)=0.5*y(k-1)+0.2*y(k-2)+1.0*u(k-1)+1.5*u(k-2)+epsi(k)-0.8*epsi(k-1)+0.3*epsi(k-2);
end
%%%%%%%%%初始化%%%%%%%%%%%%%%%%%%
%最小二乘初始化
fai = zeros(total,2*n+1);
for k = 1:total
    fai(k,:) = [-y(1,(k-1)+n),-y(1,k),u(1,k+n),u(1,k-1+n),u(1,k)];
end
yhat = y(1,n+1:n+total)';
thita = inv(fai'*fai)*fai'*yhat;
a1=thita(1);
a2=thita(2);
b1=thita(3);
b2=thita(4);
d1 = 0.1;
d2 = 0.1;
thita0 = [a1,a2,b1,b2,d1,d2]';
epsi(1)=0;epsi(2)=0;
epsida1(1)=0;epsida2(1)=0;epsidb1(1)=0;epsidb2(1)=0;epsidd1(1)=0;epsidd2(1)=0;
epsida1(2)=0;epsida2(2)=0;epsidb1(2)=0;epsidb2(2)=0;epsidd1(2)=0;epsidd2(2)=0;

j=1;
thita1=zeros(6,1);
epsidtheda=zeros(6,1);
while j<=1000
    a1value(j)=a1;  
    a2value(j)=a2;
    b1value(j)=b1;   
    b2value(j)=b2;
    d1value(j)=d1;  
    d2value(j)=d2;
    a1e(j)=-0.5-a1;  
    a2e(j)=-0.2-a2;
    b1e(j)=1.0-b1;   
    b2e(j)=1.5-b2;
    d1e(j)=-0.8-d1;  
    d2e(j)=0.3-d2;
    
    for i=1:N+2
        x1=xor(z3,z4);
        x2=z1;
        x3=z2;
        x4=z3;
        z(i)=z4;
        if z(i)>0.5
            u(i)=-1;
        else
            u(i)=1;
        end
        z1=x1;z2=x2;z3=x3;z4=x4;
    end
    %figure(1);
    %stem(u),grid on
    %%%%%%%%%%系统输出%%%%%%%%%%%%
    y(1)=0;y(2)=0;
    epsi=sigma*randn(N+3,1);  %噪声
    y(1)=1;y(2)=0.01;
    for k=3:N+2
        y(k)=0.5*y(k-1)+0.2*y(k-2)+1.0*u(k-1)+1.5*u(k-2)+epsi(k)-0.8*epsi(k-1)+0.3*epsi(k-2);
    end
    gradmat = 0;
    hessianmat = 0;
    a1=thita0(1);a2=thita0(2);b1=thita0(3);b2=thita0(4);d1=thita0(5);d2=thita0(6);

    for k=3:N+2
        epsi(k)=y(k)+a1*y(k-1)+a2*y(k-2)-b1*u(k-1)-b2*u(k-2)-d1*epsi(k-1)-d2*epsi(k-2);%
        epsida1(k)=y(k-1)-d1*epsida1(k-1)-d2*epsida1(k-2);
        epsida2(k)=y(k-2)-d1*epsida2(k-1)-d2*epsida2(k-2);
        epsidb1(k)=-u(k-1)-d1*epsidb1(k-1)-d2*epsidb1(k-2);
        epsidb2(k)=-u(k-2)-d1*epsidb2(k-1)-d2*epsidb2(k-2);
        epsidd1(k)=-epsi(k-1)-d1*epsidd1(k-1)-d2*epsidd1(k-2);
        epsidd2(k)=-epsi(k-2)-d1*epsidd2(k-1)-d2*epsidd2(k-2);
        epsidtheda=[epsida1(k),epsida2(k),epsidb1(k),epsidb2(k),epsidd1(k),epsidd2(k)]';
        gradmat=gradmat+epsi(k)*epsidtheda;
        hessianmat=hessianmat+epsidtheda'*epsidtheda;
    end
    
    thita1=thita0;
    thita0=thita0-inv(hessianmat)*gradmat;
    a1=thita0(1);a2=thita0(2);b1=thita0(3);b2=thita0(4);d1=thita0(5);d2=thita0(6);
    
    
    epsi(1)=epsi(N+1);epsi(2)=epsi(N+2);
    epsida1(1)=epsida1(N+1);epsida2(1)=epsida2(N+1);epsidb1(1)=epsidb1(N+1);
    epsidb2(1)=epsidb2(N+1);epsidd1(1)=epsidd1(N+1);epsidd2(1)=epsidd2(N+1);
    epsida1(2)=epsida1(N+2);epsida2(2)=epsida2(N+2);epsidb1(2)=epsidb1(N+2);
    epsidb2(2)=epsidb2(N+2);epsidd1(2)=epsidd1(N+2);epsidd2(2)=epsidd2(N+2);
    j = j+1;
end

figure(2)
plot(a1value);
hold on
plot(a2value);
hold on
plot(b1value);
hold on 
plot(b2value);
hold on 
plot(d1value);
hold on
plot(d2value);
grid on
 
figure(3)
plot(a1e);
hold on
plot(a2e);
hold on
plot(b1e);
hold on 
plot(b2e);
hold on 
plot(d1e);
hold on
plot(d2e);
grid on




