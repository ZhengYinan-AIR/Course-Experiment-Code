% clear all
% close all
% clc

% M���С������źŲ���������ʾ���� 
L=60;%��λ��λ������������M���е�����
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
stem(u),grid on%����M���������ź�
randn('seed',100)
v=randn(1,60); %����һ��N��0,1�����������
v = v*sqrt(0.5)
%���������С���˱�ʶ
z(2)=0;z(1)=0;
theat0=[0.001 0.001 0.001 0.001 0.001 0.001 0.001]';%ֱ�Ӹ�������ʶ�����ĳ�ʼֵ,��һ�����С��ʵ����
p0=10^4*eye(7,7);%��ʼ״̬P0
theat444=[theat0,zeros(7,59)];%����ʶ��������ĳ�ʼֵ����С
e=zeros(4,60);%������ĳ�ʼֵ����С
for k=3:60; 
    z(k)=-1.6*z(k-1)-0.7*z(k-2)+u(k-1)+0.4*u(k-2)+1.1*v(k)+1.4*v(k-1)+0.3*v(k-2);
    h1=[-z(k-1),-z(k-2),u(k-1),u(k-2),v(k),v(k-1),v(k-2)]';
    x=h1'*p0*h1+1;
    x1=inv(x); 
    k1=p0*h1*x1; %K
    d1=z(k)-h1'*theat0; 
    theat1=theat0+k1*d1;%��ʶ����c 
    theat0=theat1;%����һ����
    theat444(:,k)=theat1;%�ѱ�ʶ����c �����������ʶ�������� 
    
    p1=p0-k1*k1'*[h1'*p0*h1+1];%find p(k)
    p0=p1;%���´���
   end%ѭ������


%�������
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
plot(i,a1,'r',i,a2,'b',i,b1,'k',i,b2,'y',i,c1,'g',i,c2,'c',i,c3,'m')%������������ʶ����
title('N(0,0.5)���������������С���˱�ʶ����')%����
grid on
subplot(2,2,3)
i=1:60; 
plot(i,ea1,i,ea2,i,eb1,i,eb2,i,ec1,i,ec2,i,ec3) %������ʶ������������
legend('a1','a2','b1','b2','c1','c2','c3');
title('N(0,0.5)��������ʶ����')
grid on

