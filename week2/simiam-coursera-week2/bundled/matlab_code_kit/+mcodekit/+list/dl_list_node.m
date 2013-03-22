classdef dl_list_node < handle

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software
    
    properties
        key_
        next_
        prev_
    end
    
    methods
        function obj = dl_list_node(key)
            obj.key_ = key;
            obj.next_ = [];
            obj.prev_ = obj.next_;
        end
    end
    
end

