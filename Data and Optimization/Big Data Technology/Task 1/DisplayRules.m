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

function DisplayRules(Rules)

    for i=1:size(Rules,1)
        disp(['Rule #' num2str(i) ': ' mat2str(Rules{i,1}) ' --> ' mat2str(Rules{i,2})]);
        disp(['       Support = ' num2str(Rules{i,3})]);
        disp(['    Confidenec = ' num2str(Rules{i,4})]);
        disp(['          Lift = ' num2str(Rules{i,5})]);
        disp(' ');
    end

end