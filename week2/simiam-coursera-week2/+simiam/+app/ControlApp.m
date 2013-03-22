classdef ControlApp < handle

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software
    
    properties
        supervisors
        timeout
        time
        goals
        index
        root
    end
    
    methods
        function obj = ControlApp(root)
            obj.supervisors = mcodekit.list.dl_list();
            obj.time = 0;
            obj.root = root;
        end
        
        function run(obj, dt)
            
        end
    end
    
end

