clc;
clear;
close all;

%% Load Data

data=load('data1');
T=data.T;

%% FP-Growth
MST=2;    % Minimum Suppport Threshold支持度
tic
out=FPGrowth(T,MST);
toc
disp(['运行时间: ',num2str(toc)]);
%% Results
Tree=out.Node;
PlotTree(Tree);
