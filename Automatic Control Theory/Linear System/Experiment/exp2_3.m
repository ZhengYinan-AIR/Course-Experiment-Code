%�����󴫵ݺ���
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


%��ӷ�

%Lembda=eig(A)

%if real(Lembda)<0
 %   'ϵͳ�ȶ�'
%else
  %  'ϵͳ���ȶ�'
%end


%ֱ�ӷ�1(�����ã�

P=eye(size(A,1));
Q=-P*A-A'*P;

det1=det(Q(1,1));
det2=det(Q(1:2,1:2));
det3=det(Q(1:3,1:3));

Det=[det1;det2;det3]

if min(Det)>0
    'ϵͳ�ȶ�'
end

%ֱ�ӷ�2
Q=eye(size(A,1));
P=lyap(A,Q);

det1=det(P(1,1));
det2=det(P(1:2,1:2));
det3=det(P(1:3,1:3));

Det=[det1;det2;det3]

if min(Det)>0
    'ϵͳ�ȶ�'
else
    'ϵͳ���ȶ�'
end


% %�ڶ����֣��ж��ȶ�����ҵ1
% clc
% sys1=tf([5],[1,1]);
% sys2=tf([1],[1,2]);
% sys3=tf([1],[1,0]);
% sys_new1=series(sys1,sys2);
% sys_new2=series(sys_new1,sys3);
% sys=feedback(sys_new2,1,-1);
% num=sys.num{1};      %�õ�����
% den=sys.den{1};      %�õ���ĸ
% [A,B,C,D]=tf2ss(num,den);
% %�������ж�
% Lembda=eig(A)
% L1=real(Lembda(1));
% L2=real(Lembda(2));
% L3=real(Lembda(3));
% if L1<0 && L2<0 && L3<0
%     str='ϵͳ�ȶ�'
% else
%     str='ϵͳ���ȶ�'
% end
% %������ŵ�򷽷��ж�
% Q=eye(size(A,1));%size(A1,1)A1��ʾ����A1��1��ʾ������2��ʾ������eye(n)��ʾn�׵�λ��
% P=lyap(A,Q);     %A'��ʾA��ת��
% det1=det(P(1,1));%det��A����ʾ��������ʽA
% det2=det(P(1:2,1:2));
% det3=det(P);
% Det=[det1;det2;det3]
% if min(Det) > 0
%    'ϵͳ�ȶ�'
% else
%    'ϵͳ���ȶ�'
% end



