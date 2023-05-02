%串联求传递函数
clc
clear

num1=[0 5];
den1=[1 1];
num2=[0 1];
den2=[1 2];
num3=[0 1];
den3=[1 0];
num4=[0 1];
den4=[0 1];


[num_1,den_1]=series(num1,den1,num2,den2);

[num_2,den_2]=series(num3,den3,num_1,den_1);

[num,den]=feedback(num_2,den_2,num4,den4,-1);

sys=tf(num,den)
[A,B,C,D]=tf2ss(num,den)


%间接法

%Lembda=eig(A)

%if real(Lembda)<0
 %   '系统稳定'
%else
  %  '系统不稳定'
%end


%直接法1(不能用）

P=eye(size(A,1));
Q=-P*A-A'*P;

det1=det(Q(1,1));
det2=det(Q(1:2,1:2));
det3=det(Q(1:3,1:3));

Det=[det1;det2;det3]

if min(Det)>0
    '系统稳定'
end

%直接法2
Q=eye(size(A,1));
P=lyap(A,Q);

det1=det(P(1,1));
det2=det(P(1:2,1:2));
det3=det(P(1:3,1:3));

Det=[det1;det2;det3]

if min(Det)>0
    '系统稳定'
else
    '系统不稳定'
end


% %第二部分，判断稳定性作业1
% clc
% sys1=tf([5],[1,1]);
% sys2=tf([1],[1,2]);
% sys3=tf([1],[1,0]);
% sys_new1=series(sys1,sys2);
% sys_new2=series(sys_new1,sys3);
% sys=feedback(sys_new2,1,-1);
% num=sys.num{1};      %得到分子
% den=sys.den{1};      %得到分母
% [A,B,C,D]=tf2ss(num,den);
% %特征根判断
% Lembda=eig(A)
% L1=real(Lembda(1));
% L2=real(Lembda(2));
% L3=real(Lembda(3));
% if L1<0 && L2<0 && L3<0
%     str='系统稳定'
% else
%     str='系统不稳定'
% end
% %李雅普诺夫方法判断
% Q=eye(size(A,1));%size(A1,1)A1表示矩阵A1，1表示行数，2表示列数，eye(n)表示n阶单位阵
% P=lyap(A,Q);     %A'表示A的转置
% det1=det(P(1,1));%det（A）表示返回行列式A
% det2=det(P(1:2,1:2));
% det3=det(P);
% Det=[det1;det2;det3]
% if min(Det) > 0
%    '系统稳定'
% else
%    '系统不稳定'
% end



