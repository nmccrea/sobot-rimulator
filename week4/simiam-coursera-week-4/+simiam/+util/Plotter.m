classdef Plotter < handle
% PLOTTER supports plotting data in 2D with a reference signal.
%
% Properties:
%   r           - Reference signal
%   x           - Time
%   y           - Output signal
%
% Methods:
%   plot_2d_ref - Plots an output and reference signal over time.
    
    properties
    %% PROPERTIES
    
        t   % Time
        y   % Output signal
        r   % Reference signal
    end
    
    methods
        function obj = Plotter()
        % PLOTTER Constructor
        
            obj.t = 0;
            obj.y = [];
            obj.r = 0;
        end
        
        function [h,g] = plot_2d_ref(obj, h, g, dt, y, r)
        %% PLOT_2D_REF Plots an output and reference signal over time
        %   [h,g] = plot_2d_ref(obj, h, g, x, y, r) plots the output signal
        %   (y) and reference signal (r) versus time (t).
        
            if ~ishandle(h)
                figure;
                a = axes;
                set(a,'NextPlot','add');
                h = plot(a, dt, y, 'b');
                g = plot(a, dt, r, 'r--');
                obj.t = dt;
                obj.y = y;
                obj.r = r;
            end
            
            obj.t = [obj.t obj.t(end)+dt];
            obj.y = [obj.y y];
            obj.r = [obj.r r];
            
            set(h, 'XData', obj.t);
            set(h, 'YData', obj.y);   
            set(g, 'XData', obj.t);
            set(g, 'YData', obj.r);
            
        end
    end
    
end
