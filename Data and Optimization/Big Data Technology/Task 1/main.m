clc;
clear;
close all;

%% Load Data

data=load('data1');
T=data.T;

%% FP-Growth
MST=2;    % Minimum Suppport Threshold֧�ֶ�
tic
out=FPGrowth(T,MST);
toc
disp(['����ʱ��: ',num2str(toc)]);
%% Results
Tree=out.Node;
PlotTree(Tree);
