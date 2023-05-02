function PlotTree(Node)

    [x, y]=treelayout([Node.Parent]);
    
    for i=1:numel(Node)
        j=Node(i).Parent;
        if j~=0
            plot([x(i) x(j)],[y(i) y(j)],'k','LineWidth',1);
        end
        hold on;
    end
    
    for i=1:numel(Node)
        plot(x(i),y(i),'ko','MarkerFaceColor','w','MarkerSize',28,'LineWidth',1);
        text(x(i),y(i),...
            [num2str(Node(i).Name) ':' num2str(Node(i).Count)],...
            'HorizontalAlignment','center');
    end
    
    axis off;

end