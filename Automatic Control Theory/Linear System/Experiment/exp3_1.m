clc
clear
%%设计状态反馈控制器
A=[-1 0 0 0;2 -3 0 0;0 0 2 0;4 -1 2 -4];
B=[0;0;1;2];
C=[3 0 1 0];
D=0;
n=size(A,1);
%%能控性判断
Qc=ctrb(A,B);
nc=rank(Qc);
if rank(Qc)==n
    str ='系统完全能控'
else
    str ='系统不完全能控'
    [A1,B1,C1,T1,k1]=ctrbf(A,B,C);
    Auc=A1((1:(n-nc)),(1:(n-nc)));
    eig(Auc);
    if max(real(eig(Auc)))>0
      disp('由于不可控部分特征根为正，通过状态反馈不能使系统镇定')
    else
      disp('不可控部分渐进稳定，通过状态反馈能使系统镇定，且系统不可控部分特征根为：')
      eig(Auc)
   end
end

%%能控性提取
disp('原系统能控性部分提取如下：')
Ac = A1((n-nc+1):n,(n-nc+1):n)
Bc = B1((n-nc+1):n,:)
Cc = C1(:,(n-nc+1):n)
disp('能控部分配置以下极点：')
P1=[-1 -2]
disp('能控部分的状态反馈增益为')
K1=place(Ac,Bc,P1)

%%对于原系统而言状态反馈增益计算
disp('原系统的状态反馈增益为')
K1=[0 0 K1];
K1=K1*T1
ABK=A-B*K1
%%配置检验
disp('经过状态反馈后，系统特征根如下：')
eig(A-B*K1)

%能观性检验
Qo=obsv(A,C);
no=rank(Qo);
if no==n
    str ='系统完全能观'
else
    str ='系统不完全能观'
    [A2,B2,C2,T2,k2]=obsvf(A,B,C);
    Auo=A2((1:(n-no)),(1:(n-no)));
    eig(Auo);
    if max(real(eig(Auo)))>0
      disp('由于不能观部分特征根为正，通过状态观测器不能使系统镇定')
    else
      disp('不能观部分渐进稳定，通过状态观测器能使系统镇定，且系统不能观部分特征根为：')
      eig(Auo)
   end
end

%%能观性提取
disp('原系统能观性部分提取如下：')
Ao = A2((n-no+1):n,(n-no+1):n)
Bo = B2((n-no+1):n,:)
Co = C2(:,(n-no+1):n)
disp('能观部分配置以下极点：')
P2=[-1 -1]
Ao1=Ao';
Bo1=Co';
K2=acker(Ao1,Bo1,P2) ;
G=K2'
G=[0;0;G]
AGC=A-G*C

%%配置检验
disp('经过状态观测器后，系统特征根如下：')
eig(AGC)