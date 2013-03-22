classdef dl_list < handle

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software
    
    properties
        head_
        tail_
        size_
        iterator_
    end
    
    methods
        function obj = dl_list()
            obj.head_ = [];
            obj.tail_ = obj.head_;
            obj.size_ = 0;
        end
        
        function insert_key(obj, key, index)
            n = mcodekit.list.dl_list_node(key);
            index = max(min(index, obj.size_+1), 1);
            if (obj.size_ == 0)
                obj.head_ = n;
                obj.tail_ = obj.head_;
            else
                if (index == 1)
                    n.next_ = obj.head_;
                    obj.head_.prev_ = n;
                    obj.head_ = n;
                elseif (index == obj.size_+1)
                    n.prev_ = obj.tail_;
                    obj.tail_.next_ = n;
                    obj.tail_ = n;
                else
                    m = obj.head_;
                    for i = 2:index
                        m = m.next_;
                    end
                    n.prev_ = m.prev_;
                    m.prev_.next_ = n;
                    n.next_ = m;
                    m.prev_ = n;
                end
            end
            obj.size_ = obj.size_+1;
        end
        
        function key = remove_key(obj, index)
            index = max(min(index, obj.size_), 1);
            if (obj.size_ == 0)
                key = [];
            elseif (obj.size_ == 1)
                key = obj.tail_.key_;
                delete(obj.tail_);
                obj.tail_ = [];
                obj.head_ = obj.tail_;
                obj.size_ = 0;
            elseif (index == 1)
                key = obj.head_.key_;
                n = obj.head_;
                obj.head_ = n.next_;
                obj.head_.prev_ = [];
                delete(n);
                obj.size_ = obj.size_-1;
            elseif (index == obj.size_)
                key = obj.tail_.key_;
                n = obj.tail_;
                obj.tail_ = n.prev_;
                obj.tail_.next_ = [];
                delete(n);
                obj.size_ = obj.size_-1;
            else
                m = obj.head_;
                for i = 2:index
                    m = m.next_;
                end
                key = m.key_;
                m.prev_.next_ = m.next_;
                m.next_.prev_ = m.prev_;
                delete(m);
                obj.size_ = obj.size_-1;
            end
        end
        
        function append_key(obj, key)
            obj.insert_key(key, obj.size_+1);
        end
        
        function key = get_key(obj, index)
            assert(index > 0, 'index has to be positive');
            index = max(min(index, obj.size_), 1);
            n = obj.head_;
            for i = 2:index
                n = n.next_;
            end
            key = n.key_;
        end
        
        function key = get_first_key(obj)
            assert(obj.size_ > 0, 'list is empty');
            key = obj.head_.key_;
        end
        
        function key = get_last_key(obj)
            assert(obj.size_ > 0, 'list is empty');
            key = obj.tail_.key_;
        end
        
        function iterator = get_iterator(obj)
            iterator = mcodekit.list.dl_list_iterator(obj);
        end
    end
end