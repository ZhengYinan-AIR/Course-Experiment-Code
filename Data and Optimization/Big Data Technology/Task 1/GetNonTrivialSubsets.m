%
% Copyright (c) 2015, Yarpiz (www.yarpiz.com)
% All rights reserved. Please read the "license.txt" for license terms.
%
% Project Code: YPML115
% Project Title: Apriori Algorithm for Association Rule Mining
% Publisher: Yarpiz (www.yarpiz.com)
% 
% Developer: S. Mostapha Kalami Heris (Member of Yarpiz Team)
% 
% Contact Info: sm.kalami@gmail.com, info@yarpiz.com
%

function S=GetNonTrivialSubsets(A)

    n=numel(A);
    
    S=cell(2^n-2,1);
    for i=1:numel(S)
        f=dec2binvec(i);
        f=[f zeros(1,n-numel(f))]; %#ok
        S{i}=A(logical(f));
    end

end