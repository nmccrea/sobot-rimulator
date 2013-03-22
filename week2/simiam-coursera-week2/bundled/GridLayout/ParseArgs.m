function varargout = ParseArgs(Args, varargin)

% Check input arguments
assert(nargin >= 2, ...
    'Function takes at least two arguments.');
assert(nargout == nargin-1, ...
    'Number of output arguments must be equal with the number of input arguments minus 1.');
assert(iscell(Args) && (isempty(Args) || isvector(Args)), ...
    'Args must be a cell vector.');
for i = 1:length(varargin)
    assert(iscellstr(varargin{i}) && isvector(varargin{i}), ...
        'All input arguments except the first one must be cell vectors of strings.');
end

% Convert Args to structure
if numel(Args) == 1
    if isstruct(Args{1})
        ArgStruct = Args{1};
    else
        error('If Args has only one element, that element must be a structure.');
    end
else
    ArgStruct = NameValue2Struct(Args{:});
end

% Make a cell array with all names in varargin
NumNames = sum(cellfun(@length,varargin));
AllNames = cell([1 NumNames]);
k = 0;
for i = 1:length(varargin)
    for j = 1:length(varargin{i})
        k = k + 1;
        AllNames{k} = varargin{i}{j};        
    end
end
assert(k == NumNames);

% Check if Args contains only arguments with names that are not among those in varargin
ArgNames = fieldnames(ArgStruct);
for i = 1:length(ArgNames)
    if ~any(strcmp(ArgNames{i},AllNames))
        error('Unknown parameter: ''%s''',ArgNames{i});
    end
end

% Create output structures
for i = 1:nargout
    ParamStruct = struct();
    for j = 1:length(varargin{i})
        ParamName = varargin{i}{j};
        if isfield(ArgStruct,ParamName)
            ParamStruct.(ParamName) = ArgStruct.(ParamName);
        else
            ParamStruct.(ParamName) = [];
        end
    end
    varargout{i} = ParamStruct;
end

    function Struct = NameValue2Struct(varargin)
        for n = 2:2:nargin
            if iscell(varargin{n})
                % Put cell arrays in another cell array so that we don't get a
                % structure vector after the conversion
                varargin{n} = {varargin{n}};
            end
        end
        Struct = struct(varargin{:});
    end

end