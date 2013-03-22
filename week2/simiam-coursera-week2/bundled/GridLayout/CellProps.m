% Helper class for GridLayout
classdef CellProps < handle
    
    properties
        HAlign = 'Stretch'
        VAlign = 'Stretch'
        LMargin = 0
        RMargin = 0
        TMargin = 0
        BMargin = 0
    end
    properties (Hidden, Dependent)
        Margin
    end
    
    methods (Static)
        function Names = GetCellParamNames()
            Names = cellfun(@(x)(['Cell' x]),CellProps.GetParamNames(), ...
                'UniformOutput',false);
        end
        function Names = GetParamNames()
            Names = { ...
                'HAlign' ...
                'VAlign' ...
                'Margin' ...
                'LMargin' ...
                'RMargin' ...
                'TMargin' ...
                'BMargin'};
        end
    end

    methods
        function Obj = CellProps(varargin)
            if length(varargin) == 1 && isstruct(varargin{1})
                P = varargin{1};
                FieldNames = fieldnames(P);
                for i = 1:length(FieldNames)
                    FieldName = FieldNames{i};
                    if strcmp(FieldName(1:4),'Cell')
                        ObjFieldName = FieldName(5:end);
                    else
                        ObjFieldName = FieldName;
                    end
                    Field = P.(FieldName);
                    if ~isempty(Field)
                        Obj.(ObjFieldName) = Field;
                    end
                end
            else
                for i = 1:2:length(varargin)
                    Obj.(varargin{i}) = varargin{i+1};
                end
            end
            
        end
        
        function set.HAlign(Obj, Value)
            Set = {'Left','Center','Right','Stretch'};
            assert(any(strcmp(Value,Set)), ...
                'HAlign must be one of: ''Left'',''Center'',''Right'',''Stretch''.');
            Obj.HAlign = Value;
        end
        function set.VAlign(Obj, Value)
            Set = {'Top','Center','Bottom','Stretch'};
            assert(any(strcmp(Value,Set)), ...
                'VAlign must be one of: ''Top'',''Center'',''Bottom'',''Stretch''.');
            Obj.VAlign = Value;
        end
        
        function set.Margin(Obj, Value)
            Obj.LMargin = Value;
            Obj.RMargin = Value;
            Obj.TMargin = Value;
            Obj.BMargin = Value;
        end
        
        function set.LMargin(Obj, Value)
            assert(isscalar(Value) && Value >= 0, ...
                'LMargin must a non-negative scalar.');
            Obj.LMargin = Value;
        end
        function set.RMargin(Obj, Value)
            assert(isscalar(Value) && Value >= 0, ...
                'RMargin must a non-negative scalar.');
            Obj.RMargin = Value;
        end
        function set.TMargin(Obj, Value)
            assert(isscalar(Value) && Value >= 0, ...
                'TMargin must a non-negative scalar.');
            Obj.TMargin = Value;
        end
        function set.BMargin(Obj, Value)
            assert(isscalar(Value) && Value >= 0, ...
                'BMargin must a non-negative scalar.');
            Obj.BMargin = Value;
        end
    end
    
end

% EOF
