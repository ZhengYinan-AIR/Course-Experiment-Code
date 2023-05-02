function createfigure(X1, YMatrix1, YMatrix2, YMatrix3, YMatrix4)
%CREATEFIGURE(X1, YMatrix1, YMatrix2, YMatrix3, YMatrix4)
%  X1:  x 数据的向量
%  YMATRIX1:  y 数据的矩阵
%  YMATRIX2:  y 数据的矩阵
%  YMATRIX3:  y 数据的矩阵
%  YMATRIX4:  y 数据的矩阵

%  由 MATLAB 于 22-Dec-2021 16:58:07 自动生成

% 创建 figure
figure1 = figure('WindowState','maximized');

% 创建 subplot
subplot1 = subplot(2,2,1,'Parent',figure1);
hold(subplot1,'on');

% 使用 plot 的矩阵输入创建多行
plot1 = plot(X1,YMatrix1,'Parent',subplot1,'LineWidth',2,'MarkerSize',2);
set(plot1(1),'DisplayName','a1',...
    'Color',[0.188235294117647 0.592156862745098 0.643137254901961],...
    'MarkerSize',6);
set(plot1(2),'DisplayName','a2','LineStyle','--',...
    'Color',[0.941176470588235 0.392156862745098 0.286274509803922]);
set(plot1(3),'DisplayName','b1','LineStyle',':',...
    'Color',[1 0.666666666666667 0.196078431372549],...
    'MarkerSize',6);
set(plot1(4),'DisplayName','b2','LineStyle','-.',...
    'Color',[0.301960784313725 0.745098039215686 0.933333333333333],...
    'MarkerSize',6);
set(plot1(5),'DisplayName','c1','Marker','pentagram',...
    'Color',[0.211764705882353 0.764705882352941 0.788235294117647]);
set(plot1(6),'DisplayName','c2','Marker','>',...
    'Color',[0.576470588235294 0.72156862745098 0.474509803921569]);
set(plot1(7),'DisplayName','c3','Marker','o',...
    'Color',[0.850980392156863 0.325490196078431 0.0980392156862745]);

% 创建 ylabel
ylabel({'幅值'});

% 创建 xlabel
xlabel({'时间'});

% 创建 title
title('N(0,0.1)白噪声增广递推最小二乘辨识方法');

box(subplot1,'on');
grid(subplot1,'on');
hold(subplot1,'off');
% 创建 legend
legend1 = legend(subplot1,'show');
set(legend1,...
    'Position',[0.491888889325989 0.794641187821119 0.0429999997317789 0.129848225707081]);

% 创建 subplot
subplot2 = subplot(2,2,3,'Parent',figure1);
hold(subplot2,'on');

% 使用 plot 的矩阵输入创建多行
plot2 = plot(X1,YMatrix2,'Parent',subplot2,'LineWidth',2);
set(plot2(1),'DisplayName','a1',...
    'Color',[0.188235294117647 0.592156862745098 0.643137254901961]);
set(plot2(2),'DisplayName','a2','LineStyle','--',...
    'Color',[0.941176470588235 0.392156862745098 0.286274509803922]);
set(plot2(3),'DisplayName','b1','LineStyle',':',...
    'Color',[1 0.666666666666667 0.196078431372549]);
set(plot2(4),'DisplayName','b2','LineStyle','-.',...
    'Color',[0.301960784313725 0.745098039215686 0.933333333333333]);
set(plot2(5),'DisplayName','c1','MarkerSize',2,'Marker','pentagram',...
    'Color',[0.211764705882353 0.764705882352941 0.788235294117647]);
set(plot2(6),'DisplayName','c2','MarkerSize',2,'Marker','>',...
    'Color',[0.576470588235294 0.72156862745098 0.474509803921569]);
set(plot2(7),'DisplayName','c3','MarkerSize',2,'Marker','o',...
    'Color',[0.850980392156863 0.325490196078431 0.0980392156862745]);

% 创建 ylabel
ylabel({'幅值'});

% 创建 xlabel
xlabel({'时间'});

% 创建 title
title('N(0,0.1)白噪声辨识精度');

box(subplot2,'on');
grid(subplot2,'on');
hold(subplot2,'off');
% 创建 subplot
subplot3 = subplot(2,2,2,'Parent',figure1);
hold(subplot3,'on');

% 使用 plot 的矩阵输入创建多行
plot3 = plot(X1,YMatrix3,'Parent',subplot3,'LineWidth',2);
set(plot3(1),...
    'Color',[0.188235294117647 0.592156862745098 0.643137254901961]);
set(plot3(2),'LineStyle','--',...
    'Color',[0.941176470588235 0.392156862745098 0.286274509803922]);
set(plot3(3),'LineStyle',':',...
    'Color',[1 0.666666666666667 0.196078431372549]);
set(plot3(4),'LineStyle','-.',...
    'Color',[0.301960784313725 0.745098039215686 0.933333333333333]);
set(plot3(5),'MarkerSize',2,'Marker','pentagram',...
    'Color',[0.211764705882353 0.764705882352941 0.788235294117647]);
set(plot3(6),'MarkerSize',2,'Marker','>',...
    'Color',[0.576470588235294 0.72156862745098 0.474509803921569]);
set(plot3(7),'MarkerSize',2,'Marker','o',...
    'Color',[0.850980392156863 0.325490196078431 0.0980392156862745]);

% 创建 ylabel
ylabel({'幅值'});

% 创建 xlabel
xlabel({'时间'});

% 创建 title
title('N(0,0.5)白噪声增广递推最小二乘辨识方法');

box(subplot3,'on');
grid(subplot3,'on');
hold(subplot3,'off');
% 创建 subplot
subplot4 = subplot(2,2,4,'Parent',figure1);
hold(subplot4,'on');

% 使用 plot 的矩阵输入创建多行
plot4 = plot(X1,YMatrix4,'Parent',subplot4,'LineWidth',2);
set(plot4(1),'DisplayName','a1',...
    'Color',[0.188235294117647 0.592156862745098 0.643137254901961]);
set(plot4(2),'DisplayName','a2','LineStyle','--',...
    'Color',[0.941176470588235 0.392156862745098 0.286274509803922]);
set(plot4(3),'DisplayName','b1','LineStyle',':',...
    'Color',[1 0.666666666666667 0.196078431372549]);
set(plot4(4),'DisplayName','b2','LineStyle','-.',...
    'Color',[0.301960784313725 0.745098039215686 0.933333333333333]);
set(plot4(5),'DisplayName','c1','MarkerSize',2,'Marker','pentagram',...
    'Color',[0.211764705882353 0.764705882352941 0.788235294117647]);
set(plot4(6),'DisplayName','c2','MarkerSize',2,'Marker','>',...
    'Color',[0.576470588235294 0.72156862745098 0.474509803921569]);
set(plot4(7),'DisplayName','c3','MarkerSize',2,'Marker','o',...
    'Color',[0.850980392156863 0.325490196078431 0.0980392156862745]);

% 创建 ylabel
ylabel({'幅值'});

% 创建 xlabel
xlabel({'时间'});

% 创建 title
title('N(0,0.5)白噪声辨识精度');

box(subplot4,'on');
grid(subplot4,'on');
hold(subplot4,'off');
