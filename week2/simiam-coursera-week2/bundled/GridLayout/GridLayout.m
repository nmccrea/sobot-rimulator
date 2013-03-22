% Main layout-manager class
classdef GridLayout < handle

    properties
        Container
        
        NumRows
        NumCols
        RowHeight
        ColWidth
        HGap
        VGap
        LMargin
        RMargin
        TMargin
        BMargin
        
        % Sizing policies
        % 0: Absolute
        % 1: Proportional
        % 2: Automatic

        RowHeightPolicy
        RowHeightAbsolute
        RowHeightWeight
        
        ColWidthPolicy
        ColWidthAbsolute
        ColWidthWeight
    end
    
    properties (Constant)
        MinRowHeight = 5
        MinColWidth = 5
    end
    
    properties (Dependent)
        ActualWidth
        ActualHeight
        RequiredWidth
        RequiredHeight
    end
    
    properties (SetAccess = private)
        Cell  % Cell container
    end
    
    methods
        function Obj = GridLayout(Parent, varargin)
            Names = { ...
                'NumRows' ...
                'NumCols' ...
                'RowHeight' ...
                'ColWidth' ...
                'CellColor' ...
                'Gap' ...
                'HGap' ...
                'VGap' ...
                'Margin' ...
                'LMargin' ...
                'RMargin' ...
                'TMargin' ...
                'BMargin'};
            NamesCell = CellProps.GetCellParamNames();
            [P, PC] = ParseArgs(varargin, Names, NamesCell);
            
            assert(~isempty(Parent), ...
                'Parent handle cannot be empty.');

            Obj.Container = uicontainer( ...
                'Parent', Parent, ...
                'ResizeFcn', @(hsrc,ev)Update(Obj,true), ...
                'BackgroundColor', P.CellColor);
            Position = getpixelposition(Obj.Container);
            setappdata(Obj.Container,'Position',Position);

            % NumRows
            DefaultNumRows = 1;
            if ~isempty(P.RowHeight) && iscell(P.RowHeight)
                DefaultNumRows = length(P.RowHeight);
            end
            Obj.NumRows = GetArg(P,'NumRows',DefaultNumRows);
            % NumCols
            DefaultNumCols = 1;
            if ~isempty(P.ColWidth) && iscell(P.ColWidth)
                DefaultNumCols = length(P.ColWidth);
            end
            Obj.NumCols = GetArg(P,'NumCols',DefaultNumCols);
            % RowHeight
            Value = GetArg(P,'RowHeight','*');
            if ~iscell(Value)
                Obj.RowHeight = cell(1,Obj.NumRows);
                [Obj.RowHeight{1:end}] = deal(Value);
            else
                Obj.RowHeight = P.RowHeight;
            end
            % ColWidth
            Value = GetArg(P,'ColWidth','*');
            if ~iscell(Value)
                Obj.ColWidth = cell(1,Obj.NumCols);
                [Obj.ColWidth{1:end}] = deal(Value);
            else
                Obj.ColWidth = P.ColWidth;
            end
            % HGap
            Obj.HGap = GetArg(P,'HGap',5);
            % VGap
            Obj.VGap = GetArg(P,'VGap',5);
            % Gap (overrides HGap, VGap)
            if ~isempty(P.Gap)
                Obj.HGap = P.Gap;
                Obj.VGap = P.Gap;
            end
            % Margin
            if isempty(P.Margin)
                DefaultLMargin = Obj.HGap;
                DefaultRMargin = Obj.HGap;
                DefaultTMargin = Obj.VGap;
                DefaultBMargin = Obj.VGap;
            else
                DefaultLMargin = P.Margin;
                DefaultRMargin = P.Margin;
                DefaultTMargin = P.Margin;
                DefaultBMargin = P.Margin;
            end
            Obj.LMargin = GetArg(P,'LMargin',DefaultLMargin);
            Obj.RMargin = GetArg(P,'RMargin',DefaultRMargin);
            Obj.TMargin = GetArg(P,'TMargin',DefaultTMargin);
            Obj.BMargin = GetArg(P,'BMargin',DefaultBMargin);
            
            % Create array of cell containers
            Obj.Cell = zeros(Obj.NumRows,Obj.NumCols);
            for RIdx = 1:Obj.NumRows
                for CIdx = 1:Obj.NumCols
                    ThisCell = uicontainer( ...
                        'Parent', Obj.Container, ...
                        'Units', 'pixels');
                    if ~isempty(P.CellColor)
                        set(ThisCell, 'BackgroundColor', P.CellColor);
                    end
                    Props = CellProps(PC);
                    setappdata(ThisCell,'Props',Props);
                    setappdata(ThisCell,'RSpan',[RIdx RIdx]);
                    setappdata(ThisCell,'CSpan',[CIdx CIdx]);
                    Obj.Cell(RIdx,CIdx) = ThisCell;
                end
            end

            % RowHeightPolicy
            Obj.RowHeightPolicy   = zeros(1,Obj.NumRows);
            Obj.RowHeightAbsolute = zeros(1,Obj.NumRows);
            Obj.RowHeightWeight   = zeros(1,Obj.NumRows);
            for RIdx = 1:Obj.NumRows
                RHeight = Obj.RowHeight{RIdx};
                if isnumeric(RHeight)
                    % Absolute
                    Obj.RowHeightPolicy(RIdx) = 0;
                    Obj.RowHeightAbsolute(RIdx) = max(RHeight,Obj.MinRowHeight);
                elseif ischar(RHeight) && RHeight(end) == '*'
                    % Proportional
                    Obj.RowHeightPolicy(RIdx) = 1;
                    Weight = RHeight(1:end-1);
                    if isempty(Weight)
                        Weight = '1';
                    end
                    Obj.RowHeightWeight(RIdx) = str2double(Weight);
                elseif ischar(RHeight) && isequal(RHeight,'a')
                    % Automatic
                    Obj.RowHeightPolicy(RIdx) = 2;
                else
                    error('Illegal RowHeight definition.');
                end
            end
            
            % ColWidthPolicy
            Obj.ColWidthPolicy   = zeros(1,Obj.NumCols);
            Obj.ColWidthAbsolute = zeros(1,Obj.NumCols);
            Obj.ColWidthWeight   = zeros(1,Obj.NumCols);
            for CIdx = 1:Obj.NumCols
                CWidth = Obj.ColWidth{CIdx};
                if isnumeric(CWidth)
                    % Absolute
                    Obj.ColWidthPolicy(CIdx) = 0;
                    Obj.ColWidthAbsolute(CIdx) = max(CWidth,Obj.MinColWidth);
                elseif ischar(CWidth) && CWidth(end) == '*'
                    % Proportional
                    Obj.ColWidthPolicy(CIdx) = 1;
                    Weight = CWidth(1:end-1);
                    if isempty(Weight)
                        Weight = '1';
                    end
                    Obj.ColWidthWeight(CIdx) = str2double(Weight);
                elseif ischar(CWidth) && isequal(CWidth,'a')
                    % Automatic
                    Obj.ColWidthPolicy(CIdx) = 2;
                else
                    error('Illegal ColWidth definition.');
                end
            end
            
            if ~isempty(Obj.RequiredHeight)
                HeightDiff = Obj.RequiredHeight-Obj.ActualHeight;
                Position = getpixelposition(Parent);
                Position(4) = Position(4) + HeightDiff;
                setpixelposition(Parent, Position);
            end
        end

        function MergeCells(Obj, RSpan, CSpan)
            if isempty(RSpan)
                RSpan = [1 Obj.NumRows];
            end
            if isscalar(RSpan)
                RSpan = [RSpan RSpan];
            end
            if isempty(CSpan)
                CSpan = [1 Obj.NumCols];
            end
            if isscalar(CSpan)
                CSpan = [CSpan CSpan];
            end
            for RIdx = RSpan(1):RSpan(2)
                for CIdx = CSpan(1):CSpan(2)
                    ThisCell = Obj.Cell(RIdx,CIdx);
                    if RIdx == RSpan(1) && CIdx == CSpan(1)
                        setappdata(ThisCell,'RSpan',RSpan);
                        setappdata(ThisCell,'CSpan',CSpan);
                    else
                        delete(ThisCell);
                    end
                end
            end
        end

        function RemoveCells(Obj, RSpan, CSpan)
            if isempty(RSpan)
                RSpan = [1 Obj.NumRows];
            end
            if isscalar(RSpan)
                RSpan = [RSpan RSpan];
            end
            if isempty(CSpan)
                CSpan = [1 Obj.NumCols];
            end
            if isscalar(CSpan)
                CSpan = [CSpan CSpan];
            end
            for RIdx = RSpan(1):RSpan(2)
                for CIdx = CSpan(1):CSpan(2)
                    ThisCell = Obj.Cell(RIdx,CIdx);
                    if ishghandle(ThisCell)
                        delete(ThisCell);
                    end
                end
            end
        end

        function FormatCells(Obj, RSpan, CSpan, varargin)
            if isscalar(RSpan)
                RSpan = [RSpan RSpan];
            end
            if isscalar(CSpan)
                CSpan = [CSpan CSpan];
            end
            for RIdx = RSpan(1):RSpan(2)
                for CIdx = CSpan(1):CSpan(2)
                    ThisCell = Obj.Cell(RIdx,CIdx);
                    if ~ishghandle(ThisCell)
                        continue; % Cell is removed
                    end
                    GridLayout.FormatCell(ThisCell, varargin{:});
                end
            end
        end

        function Update(Obj, IsCallback)
            if nargin < 2
                IsCallback = false;
            end
            % Layout size
            NewPosition = getpixelposition(Obj.Container);
            OldPosition = getappdata(Obj.Container,'Position');
            if isequal(NewPosition,OldPosition) && IsCallback
                return;
            end
            setappdata(Obj.Container,'Position',NewPosition);
            LayoutWidth  = NewPosition(3);
            LayoutHeight = NewPosition(4);

            % Get children cells; as a vector!
            Cells = get(Obj.Container,'Children');
            % Get their row and column spans
            RSpan = zeros(length(Cells),2);
            CSpan = zeros(length(Cells),2);
            for i = 1:length(Cells)
                RSpan(i,:) = getappdata(Cells(i),'RSpan');
                CSpan(i,:) = getappdata(Cells(i),'CSpan');
            end
            
            % Determine column widths
            CWidthSum = LayoutWidth-(Obj.NumCols-1)*Obj.VGap-Obj.LMargin-Obj.RMargin;
            CWidth = zeros(1,Obj.NumCols);
            % 1. Absolute
            CMask = Obj.ColWidthPolicy == 0;
            CWidth(CMask) = Obj.ColWidthAbsolute(CMask);
            % 2. Automatic
            for CIdx = find(Obj.ColWidthPolicy == 2)
                MaxWidth = 0;
                Mask = CSpan(:,1) == CIdx & CSpan(:,2) == CIdx;
                assert(sum(Mask) > 0, ...
                    'Any column with automatic width must have at least one non-merged cell.');
                for MyCell = Cells(Mask)'
                    Props = getappdata(MyCell,'Props');
                    Width = Props.LMargin+Props.RMargin;
                    Child = get(MyCell,'Children');
                    if ~isempty(Child)
                        ChildSize = get(Child,'Position');
                        Width = Width + ChildSize(3);
                    end
                    MaxWidth = max(MaxWidth,Width);
                end
                CWidth(CIdx) = MaxWidth;
            end
            % 3. Proportional
            CWidthProportionalMask = Obj.ColWidthPolicy == 1;
            CWidthSumProportional = CWidthSum - sum(CWidth);
            CWidthSumProportional = max(CWidthSumProportional,0);
            CWidthWeight = Obj.ColWidthWeight(CWidthProportionalMask);
            CWidth(CWidthProportionalMask) = CWidthSumProportional*CWidthWeight/sum(CWidthWeight);
            CWidth = max(CWidth, Obj.MinColWidth);

            % Determine row heights
            RHeightSum = LayoutHeight-(Obj.NumRows-1)*Obj.HGap-Obj.TMargin-Obj.BMargin;
            RHeight = zeros(1,Obj.NumRows);
            % 1. Absolute
            RMask = Obj.RowHeightPolicy == 0;
            RHeight(RMask) = Obj.RowHeightAbsolute(RMask);
            % 2. Automatic
            for RIdx = find(Obj.RowHeightPolicy == 2)
                MaxHeight = 0;
                Mask = RSpan(:,1) == RIdx & RSpan(:,2) == RIdx;
                assert(sum(Mask) > 0, ...
                    'Any row with automatic height must have at least one non-merged cell.');
                for MyCell = Cells(Mask)'
                    Props = getappdata(MyCell,'Props');
                    Height = Props.TMargin+Props.BMargin;
                    Child = get(MyCell,'Children');
                    if ~isempty(Child)
                        ChildSize = get(Child,'Position');
                        Height = Height + ChildSize(4);
                    end
                    MaxHeight = max(MaxHeight,Height);
                end
                RHeight(RIdx) = MaxHeight;
            end
            % 3. Proportional
            RMask = Obj.RowHeightPolicy == 1;
            RHeightSumProportional = RHeightSum - sum(RHeight);
            RHeightSumProportional = max(RHeightSumProportional,0);
            Weight = Obj.RowHeightWeight(RMask);
            RHeight(RMask) = RHeightSumProportional*Weight/sum(Weight);
            RHeight = max(RHeight, Obj.MinRowHeight);
            
            % Horizontal and vertical offsets for each cell
            CellOffsetH = cumsum([Obj.LMargin CWidth(1:end-1)+Obj.VGap]);
            CellOffsetV = LayoutHeight-cumsum([RHeight(1)+Obj.BMargin RHeight(2:end)+Obj.HGap]);

            % Set cell positions
            for i = 1:length(Cells)
                RIdx  = RSpan(i,1):RSpan(i,2);
                CIdx  = CSpan(i,1):CSpan(i,2);

                set(Cells(i), ...
                    'Position', [ ...
                        CellOffsetH(CIdx(1)) ...
                        CellOffsetV(RIdx(end)) ...
                        sum(CWidth(CIdx))+Obj.VGap*(length(CIdx)-1) ...
                        sum(RHeight(RIdx))+Obj.HGap*(length(RIdx)-1)]);
                    
                GridLayout.ResizeCell(Cells(i));
            end
        end
        
        function Value = get.ActualWidth(Obj)
            Position = getpixelposition(Obj.Container);
            Value = Position(3);
        end
        function Value = get.ActualHeight(Obj)
            Position = getpixelposition(Obj.Container);
            Value = Position(4);
        end
        
        function Value = get.RequiredWidth(Obj)
            if any(Obj.ColWidthPolicy == 1)
                Value = [];
                return;
            end
            Mask = Obj.ColWidthPolicy == 0;
            Value = sum(Obj.ColWidthAbsolute(Mask)) + Obj.HGap*(Obj.NumCols-1) + Obj.LMargin + Obj.RMargin;
        end
        function Value = get.RequiredHeight(Obj)
            if any(Obj.RowHeightPolicy == 1)
                Value = [];
                return;
            end
            Mask = Obj.RowHeightPolicy == 0;
            Value = sum(Obj.RowHeightAbsolute(Mask)) + Obj.VGap*(Obj.NumRows-1) + Obj.TMargin + Obj.BMargin;
        end
    end
    
    methods (Static)
        function FormatCell(Cell, varargin)
            assert(isscalar(Cell) && ishghandle(Cell), ...
                'Cell must be a hghandle.');
            Props = getappdata(Cell,'Props');
            for i = 1:2:length(varargin)
                Props.(varargin{i}) = varargin{i+1};
            end
            setappdata(Cell,'Props',Props);
        end
    end
    
    methods (Static, Access = private)
        function ResizeCell(Src)
            Child = get(Src,'Children');
            if isempty(Child)
                return;
            end
            
            % Special case for axes with legend
            % The legend has the same parent as the axes!
            if ~isscalar(Child)
                assert(numel(Child) == 2 && ...
                    ishghandle(Child(1),'axes') && strcmp(get(Child(1),'Tag'),'legend') && ...
                    ishghandle(Child(2),'axes'), ...
                    'If Cell has two children, they must be an ''axes'' and its legend.');
                Child = Child(2);
            end
            
            % Special treatment for axes objects
            IsChildAxes = ishghandle(Child,'axes');
            if IsChildAxes
                OldAxesUnits = get(Child,'Units');
                set(Child,'Units','Pixels');
                UseOuterPosition = strcmp(get(Child,'ActivePositionProperty'),'outerposition');
                if UseOuterPosition
                    ChildPosition = get(Child,'OuterPosition');
                else
                    ChildPosition = get(Child,'Position');
                end
            else
                ChildPosition = get(Child,'Position');
            end
            
            % Child offset and size
            ChildOffset = ChildPosition(1:2);
            ChildSize = ChildPosition(3:4);
            % Cell size
            CellPosition = getpixelposition(Src);
            CellSize = CellPosition(3:4);
            % Cell propoerties
            Props = getappdata(Src,'Props');
            % Horizontal alignment
            HAlign  = Props.HAlign;
            LMargin = Props.LMargin;
            RMargin = Props.RMargin;
            if strcmp(HAlign,'Left')
                ChildOffset(1) = LMargin;
            elseif strcmp(HAlign,'Right')
                ChildOffset(1) = CellSize(1)-ChildSize(1)-RMargin;
            elseif strcmp(HAlign,'Center')
                ChildOffset(1) = (CellSize(1)-ChildSize(1))/2;
            else % Stretch
                ChildOffset(1) = LMargin;
                ChildSize(1) = CellSize(1)-LMargin-RMargin;
            end
            % Vertical alignment
            VAlign  = Props.VAlign;
            TMargin = Props.TMargin;
            BMargin = Props.BMargin;
            if strcmp(VAlign,'Bottom')
                ChildOffset(2) = BMargin;
            elseif strcmp(VAlign,'Top')
                ChildOffset(2) = CellSize(2)-ChildSize(2)-TMargin;
            elseif strcmp(VAlign,'Center')
                ChildOffset(2) = (CellSize(2)-ChildSize(2))/2;
            else % Stretch
                ChildOffset(2) = BMargin;
                ChildSize(2) = CellSize(2)-TMargin-BMargin;
            end
            % Prevent non-positive sizes
            ChildSize = max(ChildSize,.1);

            % Update child position
            ChildPosition = [ChildOffset ChildSize];
            if IsChildAxes
                if UseOuterPosition
                    set(Child,'OuterPosition',ChildPosition);
                else
                    set(Child,'Position',ChildPosition);
                end
                set(Child,'Units',OldAxesUnits);
            else
                set(Child,'Position',ChildPosition);
            end
        end
        
    end
end

% EOF
