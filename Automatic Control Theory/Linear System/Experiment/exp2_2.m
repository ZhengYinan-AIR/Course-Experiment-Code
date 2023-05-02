clc
clear

A=[-4 1 0 0 0 0;0 -4 0 0 0 0;0 0 3 1 0 0;0 0 0 3 0 0;0 0 0 0 -1 1;0 0 0 0 0 -1];
B=[1 3;5 7;4 3;0 0;1 6;0 0];
C=[3 1 0 5 0 0;1 4 0 2 0 0];

n=size(A,1);
Qc=ctrb(A,B);
Qo=obsv(A,C);

if rank(Qc)==n
    'ϵͳ�ܿ�'
else
    'ϵͳ���ܿ�'
end

if rank(Qo)==n
    'ϵͳ�ܹ�'
else 
    'ϵͳ���ܹ�'
    [A2,B2,C2,T,k]=obsvf(A,B,C)
end

% %�ڶ����ֵڶ��⣬�ж�ϵͳ�ܿ��ܹ���
% clc
% A=[-4 1 0 0 0 0 ;0 -4 0 0 0 0 ;0 0 3 1 0 0;0 0 0 3 0 0;0 0 0 0 -1 1;0 0 0 0 0 -1];
% B=[1 3;5 7;4 3;0 0 ;1 6;0 0];
% C=[3 1 0 5 0 0;1 4 0 2 0 0];
% n=size(A,1);
% Qc=ctrb(A,B);
% nc=rank(Qc)
% if rank(Qc)==n
%     str='ϵͳ��ȫ�ܿ�'
% else
%     str='ϵͳ����ȫ�ܿ�'
%     [A1,B1,C1,T,k]=ctrbf(A,B,C);
% end
% Ac = A1((n-nc+1):n,(n-nc+1):n);
% Bc = B1((n-nc+1):n,:);
% Cc = C1(:,(n-nc+1):n);
% n1=size(Ac,1);
% Qo=obsv(Ac,Cc);
% no=rank(Qo)
% if rank(Qo)==n1
%     str='ϵͳ��ȫ�ܹ�'
% else
%     str='ϵͳ����ȫ�ܹ�'
%     [A2,B2,C2,T2,k2]=obsvf(Ac,Bc,Cc);
% end
% Ao = A2((n1-no+1):n1,(n1-no+1):n1)
% Bo = B2((n1-no+1):n1,:)
% Co = C2(:,(n1-no+1):n1)