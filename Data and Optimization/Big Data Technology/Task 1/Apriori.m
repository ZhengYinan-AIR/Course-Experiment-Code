clear; 
clc;
close all;
%% 加载数据并完成初始化
load data1.mat
min_sup=2; % 最小支持度
Data = T;
tic
% 生成物品编号
Elements=[];
for i=1:numel(Data) % 获取矩阵的元素个数
    Elements=union(Elements,Data{i});
end
Elements=reshape(Elements,1,[]); % 存储出现过的标号

Count=zeros(size(Elements));
for i=1:numel(Data)
    Count=Count+ismember(Elements,Data{i});
end
m = numel(Elements);
n = numel(Data);
aaaaa = 1;
k=0;
while 1
    disp(aaaaa)
    aaaaa = aaaaa+1;
    if(aaaaa==7)
        aaaaaa = 1;
    end
	k=k+1;
	L{k}={};
	%% 生成候选集C{k}
	if k==1
		C{k}=(1:m)'; % 第一个候选集为全部商品
	else
		[nL,mL]=size(L{k-1});
		cnt=0;
		for i=1:nL
			for j=i+1:nL
				tmp=union(L{k-1}(i,:),L{k-1}(j,:)); % 两集合并集
				if length(tmp)==k
					cnt=cnt+1;
					C{k}(cnt,1:k)=tmp;
				end
			end
		end
		C{k}=unique(C{k},'rows'); % 去掉重复的行
	end
	%% 求候选集的支持度
	[nC,mC]=size(C{k}); % 候选集大小
	for i=1:nC
		cnt=0;
		for j=1:n
			if all(ismember(C{k}(i,:),Data{j}),2)==1 % all函数判断向量是否全为1，参数2表示按行判断
				cnt=cnt+1;
			end
		end
		C_sup{k}(i,1)=cnt; % 每行存候选集对应的支持度
	end
	%% 求频繁项集L{k}
	L{k}=C{k}(C_sup{k}>=min_sup,:);
    C_above_sup{k}=C_sup{k}(C_sup{k}>=min_sup,:);
	if isempty(C{k}(C_sup{k}>=min_sup,:)) % 这次没有找出频繁项集
		break;
    end
	if size(L{k},1)==1 % 频繁项集行数为1，下一次无法生成候选集，直接结束
		break
    end
end
toc
disp(['运行时间: ',num2str(toc)]);