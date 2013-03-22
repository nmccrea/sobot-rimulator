classdef dl_list_iterator < handle

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software
    
    properties
        list_
        index_
    end
    
    methods
        function obj = dl_list_iterator(list)
            obj.list_ = list;
            obj.index_ = obj.list_.head_;
        end
        
        function bool = has_next(obj)
%             if(isa(obj.index_, 'dl_list_node') && ~isvalid(obj.index_))
%                 warning('dl_list:MutatedList', 'List was mutated. Resetting iterator');
%                 obj.reset();
%             end
            bool = ~isempty(obj.index_);
%             bool = ~(obj.index_ == []);
        end
        
        function reset(obj)
            obj.index_ = obj.list_.head_;
        end
        
        function key = next(obj)
            key = [];
            if(~obj.has_next())
                warning('dl_list:NoSuchElement', 'There is no next element.');
                return;
            end
            
            key = obj.index_.key_;
            obj.index_ = obj.index_.next_;
        end
    end
    
end

