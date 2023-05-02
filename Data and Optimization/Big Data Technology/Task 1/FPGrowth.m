function out=FPGrowth(Data_Set,min_sup)
    treeNode.Name=[];
    treeNode.Count=0;
    treeNode.Parent=[];
    treeNode.Children=[];
    treeNode.Path=[];
    treeNode.Patterns={};
    treeNode.PatternCount=[];

    %% ����Ƶ�ν�������
    Elements=[];
    for i=1:numel(Data_Set) % ��ȡ�����Ԫ�ظ���
        Elements=union(Elements,Data_Set{i});
    end
    Elements=reshape(Elements,1,[]); % �洢���ֹ��ı��

    Count=zeros(size(Elements));
    for i=1:numel(Data_Set)
        Count=Count+ismember(Elements,Data_Set{i});
    end
    % �޳�����������
    Elements=Elements(Count>=min_sup);
    Count=Count(Count>=min_sup);
    [~, SortOrder]=sort(Count,'descend');
    Elements=Elements(SortOrder);

    %% ����FP��
    % �������ڵ�
    Node(1)=treeNode;
    Node(1).Name='N';
    Node(1).Parent=0;

    LastIndex=1;

    for i=1:numel(Data_Set)

        A=[];
        for item=Elements
            if ismember(item,Data_Set{i})
                A=[A item];	% �������У�����������
            end
        end

        CurrentNode=1;
        Node(CurrentNode).Count=Node(CurrentNode).Count+1; 
        %����ڵ�
        for a=A
            ChildNodeExists=false;
            %�����һ��a����ĸ��ڵ�����һ��a����ķ�֧��������ڵ������һ�ֲ洦
            for c=Node(CurrentNode).Children
                if Node(c).Name==a
                    ChildNodeExists=true;
                    break;
                end
            end
            if ChildNodeExists
                CurrentNode=c;
            else
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

    %% ��ھ�
    for i=2:numel(Node)
        S=GetPowerSet(Node(i).Path(1:end-1))';
        Node(i).Patterns=cell(size(S));       
        Node(i).PatternCount=zeros(size(S)); 
        for j=1:numel(Node(i).Patterns)
            Node(i).Patterns{j}=[S{j} Node(i).Name];
            Node(i).PatternCount(j)=Node(i).Count;
        end

        k=i;
        while true

            p=Node(k).Parent;
            if p==0
                break;
            end

            for j=1:numel(Node(i).Patterns)
                Pj=Node(i).Patterns{j};

                PatternFound=false;
                for l=1:numel(Node(p).Patterns)
                    Pl=Node(p).Patterns{l};
                    if IsSame(Pj,Pl)
                        PatternFound=true;
                        break;
                    end
                end

                if ~PatternFound
                    l=numel(Node(p).Patterns)+1;
                    Node(p).Patterns{l}=Pj;
                    Node(p).PatternCount(l)=0;
                end

                Node(p).PatternCount(l)=Node(p).PatternCount(l)+Node(i).PatternCount(j);

            end

            k=p;

        end

    end

    Patterns=Node(1).Patterns;
    PatternCount=Node(1).PatternCount;

    Patterns=Patterns(PatternCount>=min_sup);
    PatternCount=PatternCount(PatternCount>=min_sup);

    for j=1:size(Patterns,2)
        Patterns{2,j}=PatternCount(j);
    end

    out.Node=Node;
    out.Patterns=Patterns;
    out.PatternCount=PatternCount;
end

function b=IsSame(A,B)

    b=numel(A)==numel(B) && all(sort(A)==sort(B));

end

function S=GetPowerSet(A)

    n=numel(A);
    
    S=cell(2^n,1);
    for i=1:numel(S)
        f=dec2binvec(i-1); 

        f=[f zeros(1,n-numel(f))];
        S{i}=A(logical(f));
    end

end