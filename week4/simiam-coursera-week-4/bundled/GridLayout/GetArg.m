function Value = GetArg(S, Name, Default)

try
    Value = S.(Name);
catch
    error('GetArg: unknown parameter ''%s''.',Name);
end

if isempty(Value)
    if nargin < 3
        error('Parameter ''%s'' must be assigned a value.',Name);
    end
    Value = Default;
end

