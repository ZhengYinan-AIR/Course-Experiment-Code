clc;
clear;
close all;
%% 加载数据
load Data.mat
%% 定义节点
treeNode.Name=[];
treeNode.Count=0;
treeNode.Parent=[];
treeNode.Children=[];
treeNode.Path=[];
treeNode.Patterns={};
treeNode.PatternCount=[];
%% FP-Growth
L={};
min_sup=2;    % Minimum Suppport Threshold支持度
result = FP_Growth(Data,min_sup,treeNode,L);
%% FP-Growth递归算法
function result = FP_Growth(Data_Set,min_sup,treeNode)
    % 终止条件
    if isempty(Data_Set)
        return
    end
    [Elements,Node] = CreateTree(Data_Set,min_sup,treeNode);
    for i = 1:numel(Elements)
        % 从项头表末尾开始取
        New_Data_Set = {};
        item = Elements(end-i+1);
        for j = 1:numel(Node)
            if Node(j).Name == item
                for k = 1:Node(j).Count
                    itemset = Node(j).Path;
                    New_Data_Set{numel(New_Data_Set)+1} = item(1:end-1);
                end
            end
        end
        % 开始递归
        result = FP_Growth(New_Data_Set,min_sup,treeNode);
        % 更新频繁项集
        if isempty(result)
            result{1} = [item];
        else
            for k = 1:numel(result)
                result{k} = [result,item];
            end
            result{end+1} = [item]; 
        end
    end
end

%% 生成FP-Tree和条件FP-Tree
function [Elements,Node] = CreateTree(Data_Set,min_sup,treeNode)
    Elements=[];
    for i=1:numel(Data_Set) % 获取矩阵的元素个数
        Elements=union(Elements,Data_Set{i});
    end
    Elements=reshape(Elements,1,[]); % 存储出现过的标号

    Count=zeros(size(Elements));
    for i=1:numel(Data_Set)
        Count=Count+ismember(Elements,Data_Set{i});
    end
    % 剔除并降序排列
    Elements=Elements(Count>=min_sup);
    Count=Count(Count>=min_sup);
    [~, SortOrder]=sort(Count,'descend');
    Elements=Elements(SortOrder);

    %% 创建FP树
    % 创建根节点
    Node(1)=treeNode;
    Node(1).Name='N';
    Node(1).Parent=0;
    LastIndex=1;
    % 扫描数据集
    for i=1:numel(Data_Set)
        A=[];
        for item=Elements
            if ismember(item,Data_Set{i})
                A=[A item];	% 降序排列，用于生成树
            end
        end
        CurrentNode=1;
        Node(CurrentNode).Count=Node(CurrentNode).Count+1;
        %分配节点
        for a=A
            ChildNodeExists=false;
            %如果下一个a矩阵的根节点是上一个a矩阵的分支，则后续节点接在上一分叉处
            for c=Node(CurrentNode).Children
                if Node(c).Name==a
                    ChildNodeExists=true;
                    break;
                end
            end
            if ChildNodeExists
                CurrentNode=c;
            else
                % 没有相同子节点则生成新的节点
                NewNode=treeNode;
                NewNode.Name=a;
                NewNode.Parent=CurrentNode;
                NewNode.Path=[Node(CurrentNode).Path NewNode.Name];
                LastIndex=LastIndex+1;
                Node(LastIndex)=NewNode;
                Node(CurrentNode).Children=[Node(CurrentNode).Children LastIndex];
                CurrentNode=LastIndex;
            end
            Node(CurrentNode).Count=Node(CurrentNode).Count+1;
        end
    end
end






