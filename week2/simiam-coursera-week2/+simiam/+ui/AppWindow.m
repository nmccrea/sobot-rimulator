classdef AppWindow < handle

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software

    properties
        parent_
        layout_
        view_
        
        ui_colors_
        ui_size_
        ui_buttons_
        
        click_src_
        center_
        
        zoom_level_
        boundary_
        ratio_
        
        simulator_
        
        target_marker_
        is_tracking_
        tracked_pose_
        
        logo_
        
        is_ready_
        
        ticks_
        time_
        
        root_
    end
    
    methods
        
        function obj = AppWindow(root)
            obj.root_ = root;
            obj.ui_colors_ = struct('gray',  [220 220 220]/255, ...
                                    'green', [ 57 200  67]/255, ...
                                    'red',   [221  23  31]/255, ...
                                    'lgray', [183 183 183]/255, ...
                                    'dgray', [242 242 242]/255, ...
                                    'black', [ 48  48  48]/255);
            
            obj.ui_size_ = [0 0 800 600];
            
            obj.is_tracking_ = false;
            obj.center_ = simiam.ui.Pose2D(0,0,0);
            
            obj.click_src_ = [0;0];
            obj.is_ready_ = false;
            
            obj.ticks_ = [];
            
            obj.time_ = 0;
        end
        
        function load_ui(obj)
            obj.create_layout();
        end
        
        function create_simulator(obj, settings_file)
            world = simiam.simulator.World(obj.view_);
            world.build_from_file(obj.root_, settings_file);
            
            token_k = world.robots.head_;
            while(~isempty(token_k))
                robot = token_k.key_.robot;
                set(robot.surfaces.head_.key_.handle_, 'ButtonDownFcn', {@obj.ui_focus_view,robot});
                set(robot.surfaces.tail_.key_.handle_, 'ButtonDownFcn', {@obj.ui_focus_view,robot});
                token_k = token_k.next_;
            end
            
            obj.simulator_ = simiam.simulator.Simulator(obj, world, 0.01);
            obj.simulator_.step([],[]);
        end
        
        function create_layout(obj)
            
            % Create MATLAB figure
            obj.parent_ = figure('MenuBar', 'none', ...
                                 'NumberTitle', 'off', ...
                                 'Name', 'Sim.I.am', ...
                                 'Color', obj.ui_colors_.gray);
            ui_size = get(obj.parent_, 'Position');
            ui_size(3:4) = obj.ui_size_(3:4);
            screen_size = get(0, 'ScreenSize');
            margins = (screen_size(3:4)-obj.ui_size_(3:4))/2;
            ui_size(1:2) = margins;
            set(obj.parent_, 'Position', ui_size);

                                  
            set(obj.parent_, 'Renderer', 'zBuffer');

            % Create user interface (ui) layout
            obj.layout_ = GridLayout(obj.parent_, 'RowHeight', {24,'*','*',36}, ....
                                                  'ColWidth', {48, 48, 48, '*' ,64, 96, 64,'*', 48 , 48, 48}, ...,
                                                  'LMargin', 10, 'RMargin', 6, ...
                                                  'Gap', 5, ...
                                                  'CellColor', obj.ui_colors_.gray);

            set(obj.layout_.Container, 'BackgroundColor', obj.ui_colors_.gray);
            MergeCells(obj.layout_, [2 3], [1 11]);            
            Update(obj.layout_);

            
            % Create UI buttons
            icon_file = fullfile(obj.root_, 'resources/splash/simiam_splash.png');
            if(isunix)
                icon_url = ['file://' icon_file];
            else
                icon_url = strrep(['file:/' icon_file],'\','/');
            end
            button_string = ['<html><div style="text-align: center"><img src="' icon_url '"/>' ...
                   '<br>Welcome to <b>Sim.I.am</b>, a robot simulator.' ...
                   '<br>This is <em>Sim the First</em>, your companion for robotics in this Coursera course.' ...
                   '</html>'];
            ui_args = {'Style','pushbutton', 'String', button_string, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'BackgroundColor', obj.ui_colors_.gray, 'Callback', @obj.ui_button_start};
            ui_parent = obj.layout_.Cell(2,1);
            obj.logo_ = uicontrol(ui_parent, ui_args{:});
            set(obj.logo_, 'Enable', 'off');
            set(findjobj(obj.logo_), 'Border', []);
            set(obj.logo_, 'BackgroundColor', [96 184 206]/255);
            
            ui_args = {'Style','pushbutton', 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @obj.ui_button_start};
            ui_parent = obj.layout_.Cell(4,6);
            play = uicontrol(ui_parent, ui_args{:});
            obj.ui_set_button_icon(play, 'ui_control_play.png');
            obj.ui_toggle_control(play, true);
            
            ui_args = {'Style','pushbutton', 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @obj.ui_reset_simulation};
            ui_parent = obj.layout_.Cell(4,5);
            refresh = uicontrol(ui_parent, ui_args{:});
            obj.ui_set_button_icon(refresh, 'ui_control_reset.png');
            obj.ui_toggle_control(refresh, false);

            ui_args = {'Style','pushbutton', 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @obj.ui_button_home};
            ui_parent = obj.layout_.Cell(4,1);
            load = uicontrol(ui_parent, ui_args{:});
            obj.ui_set_button_icon(load, 'ui_control_home.png');
            obj.ui_toggle_control(load, false);
            
            ui_args = {'Style', 'pushbutton', 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @obj.ui_button_zoom_in};
            ui_parent = obj.layout_.Cell(4,11);
            zoom_in = uicontrol(ui_parent, ui_args{:});
            obj.ui_set_button_icon(zoom_in, 'ui_control_zoom_in.png');
            obj.ui_toggle_control(zoom_in, false);
            
            ui_args = {'Style', 'pushbutton', 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @obj.ui_button_zoom_out};
            ui_parent = obj.layout_.Cell(4,10);
            zoom_out = uicontrol(ui_parent, ui_args{:});
            obj.ui_set_button_icon(zoom_out, 'ui_control_zoom_out.png');
            obj.ui_toggle_control(zoom_out, false);
            
            
            ui_args = {'Style', 'pushbutton', 'BackgroundColor', obj.ui_colors_.gray};
            ui_parent = obj.layout_.Cell(1,9);
            status = uicontrol(ui_parent, ui_args{:});
            set(status, 'Enable', 'off');
            set(findjobj(status), 'Border', []);
            obj.ui_set_button_icon(status, 'ui_status_ok.png');
            
            ui_args = {'Style', 'pushbutton', 'BackgroundColor', obj.ui_colors_.gray};
            ui_parent = obj.layout_.Cell(1,10);
            clock = uicontrol(ui_parent, ui_args{:});
            set(clock, 'Enable', 'off');
            set(findjobj(clock), 'Border', []);
            obj.ui_set_button_icon(clock, 'ui_status_clock.png');
            
            ui_args = {'Style', 'togglebutton', 'BackgroundColor', obj.ui_colors_.gray};
            time = uicontrol(obj.layout_.Cell(1,11), ui_args{:});
            set(findjobj(time), 'Border', []);
            set(time, 'Value', true);

            obj.ui_buttons_ = struct('play', play, 'play_state', false, ...
                         'refresh', refresh, ...
                         'load', load, ...
                         'status', status, ...
                         'time', time, ...
                         'zoom_in', zoom_in, ...
                         'zoom_out', zoom_out); 
            obj.ui_update_clock(0);

            % Set minimum size for figure
            jFrame = get(handle(obj.parent_), 'JavaFrame');
            jClient = jFrame.fHG1Client;
            drawnow;
            jWindow = jClient.getWindow;
            jWindow.setMinimumSize(java.awt.Dimension(800, 600));
                              
            Update(obj.layout_);
            
        end
        
        function create_callbacks(obj)

            % Create UI callbacks    
            set(obj.view_, 'ButtonDownFcn', @obj.ui_press_mouse);
            set(obj.parent_,'ResizeFcn', @obj.ui_resize_view);
            set(obj.parent_,'WindowScrollWheelFcn', @obj.ui_zoom_view);
            set(obj.parent_,'KeyPressFcn', @obj.ui_press_key);
            set(obj.parent_, 'CloseRequestFcn', @obj.ui_close);
        end
        
        
        % UI functions
        
        function ui_toggle_control(obj, ui_control_button, is_state_on)
            if(is_state_on)
                set(ui_control_button, 'Enable', 'on');
                set(ui_control_button, 'BackgroundColor', obj.ui_colors_.dgray);
            else
                set(ui_control_button, 'Enable', 'off');
                set(ui_control_button, 'BackgroundColor', obj.ui_colors_.lgray);
            end
        end
        
        function ui_set_button_icon(obj, ui_button, icon)
            icon_file = fullfile(obj.root_, 'resources/icons', icon);
            if(isunix)
                icon_url = ['file://' icon_file];
            else
                icon_url = strrep(['file:/' icon_file],'\','/');
            end
            button_string = ['<html><img src="' icon_url '"/></html>'];
            set(ui_button, 'String', button_string);
        end
        
        function ui_update_clock(obj, dt)
            obj.time_ = obj.time_ + dt;
            clock_string = sprintf('%02d:%02d', floor(obj.time_/60), floor(mod(obj.time_,60)));
            set(obj.ui_buttons_.time, 'String', clock_string);
        end
        
        function ui_update(obj, dt, is_state_crashed)
            
            if (is_state_crashed)
                obj.simulator_.stop();
                obj.ui_set_button_icon(obj.ui_buttons_.status, 'ui_status_error.png');
                obj.ui_toggle_control(obj.ui_buttons_.refresh, true);
                obj.ui_toggle_control(obj.ui_buttons_.play, false);
            end
            
            if(obj.is_tracking_)
                obj.ui_set_axes();
            end
            
            obj.ui_update_clock(dt);
        end
        
        function ui_reset_simulation(obj, src, event)
            obj.ui_toggle_control(obj.ui_buttons_.refresh, false);
            obj.ui_set_button_icon(obj.ui_buttons_.status, 'ui_status_ok.png');
            obj.time_ = 0;
            obj.ui_update_clock(0);
            obj.ui_button_home(src, event);
            obj.ui_button_start(src, event);
        end
        
        function ui_button_start(obj, src, event)
%             [filename, pathname] = uigetfile({'*.xml', 'XML file'}, 'Load a world for the simulator.');
%             if (isequal(filename, 0) || isequal(pathname, 0))
% %                 delete(obj.parent_);
%                 warning('No file was selected.');
%                 return
%             end          
%             simiam.ui.AppWindow().load_ui(fullfile(pathname, filename));
%             delete(obj.parent_);

            % Create ui main view
            delete(obj.logo_);
            view_parent = obj.layout_.Cell(2,1);
            set(view_parent, 'Children', []);
            Update(obj.layout_);
            
            obj.view_ = axes('Parent', obj.layout_.Cell(2,1), ...
                        'ActivePositionProperty','Position', ...
                        'Box', 'on');
            Update(obj.layout_);            
                    
            % Target Marker
            obj.target_marker_ = plot(obj.view_, inf, inf, ...
                'Marker', 'o', ...
                'MarkerFaceColor', obj.ui_colors_.green, ...
                'MarkerEdgeColor', obj.ui_colors_.green, ...
                'MarkerSize', 10);
            
            set(obj.view_, 'XGrid', 'on');
            set(obj.view_, 'YGrid', 'on');
            set(obj.view_, 'XTickMode', 'manual');
            set(obj.view_, 'YTickMode', 'manual');
            set(obj.view_, 'Units', 'pixels');
            view_quad = get(obj.view_, 'Position');
            set(obj.view_, 'Units', 'normal');
            
            width = view_quad(3); 
            height = view_quad(4);
            
            obj.ratio_ = width/height;          
            obj.zoom_level_ = 1;
            obj.boundary_ = 2.5;
            
            obj.ui_set_axes();
            
            % Change ui controls
            obj.ui_toggle_control(obj.ui_buttons_.play, true);
            obj.ui_toggle_control(obj.ui_buttons_.load, false);
            
            obj.create_callbacks();
%             obj.create_simulator(fullfile(pathname, filename));
            obj.create_simulator(fullfile(obj.root_, 'settings.xml'));
            
            obj.ui_buttons_.play_state = true;
            obj.ui_set_button_icon(obj.ui_buttons_.play, 'ui_control_pause.png');
            set(obj.ui_buttons_.play, 'Callback', @obj.ui_button_play);
            
            obj.is_ready_ = true;
            obj.ui_toggle_control(obj.ui_buttons_.load, true);
            obj.ui_toggle_control(obj.ui_buttons_.zoom_in, true);
            obj.ui_toggle_control(obj.ui_buttons_.zoom_out, true);
            obj.time_ = 0;
            obj.ui_update_clock(0);
            obj.simulator_.start();
        end
        
        function ui_button_home(obj, src, event)
            obj.is_ready_ = false;
            obj.center_ = simiam.ui.Pose2D(0,0,0);
            
            obj.ui_toggle_control(obj.ui_buttons_.zoom_in, false);
            obj.ui_toggle_control(obj.ui_buttons_.zoom_out, false);
            obj.ui_toggle_control(obj.ui_buttons_.refresh, false);
            obj.ui_set_button_icon(obj.ui_buttons_.status, 'ui_status_ok.png');
            obj.time_ = 0;
            obj.ui_update_clock(0);
            
            obj.ui_toggle_control(obj.ui_buttons_.play, true);
            
            obj.simulator_.shutdown();
            delete(obj.simulator_);
            delete(obj.view_);
            
            view_parent = obj.layout_.Cell(2,1);
            set(view_parent, 'Children', []);
            Update(obj.layout_);
            icon_file = fullfile(obj.root_, 'resources/splash/simiam_splash.png');
            if(isunix)
                icon_url = ['file://' icon_file];
            else
                icon_url = strrep(['file:/' icon_file],'\','/');
            end
            button_string = ['<html><div style="text-align: center"><img src="' icon_url '"/>' ...
                             '<br>Welcome to <b>Sim.I.am</b>, a robot simulator.' ...
                             '<br>This is <em>Sim the First</em>, your companion for robotics in this Coursera course.' ...
                             '</html>'];
            ui_args = {'Style','pushbutton', 'String', button_string, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'BackgroundColor', obj.ui_colors_.gray, 'Callback', @obj.ui_button_start};
            ui_parent = obj.layout_.Cell(2,1);
            obj.logo_ = uicontrol(ui_parent, ui_args{:});
            set(obj.logo_, 'Enable', 'off');
            set(findjobj(obj.logo_), 'Border', []);
            set(obj.logo_, 'BackgroundColor', [96 184 206]/255);
            
            ui_parent_size = get(ui_parent, 'Position');
            set(obj.logo_, 'Position', [0 0 ui_parent_size(3:4)]);
            
%             set(obj.view_, 'ButtonDownFcn', @obj.ui_no_op);

            % Remove callbacks from figure
            set(obj.parent_,'ResizeFcn', @obj.ui_no_op);
            set(obj.parent_,'WindowScrollWheelFcn', @obj.ui_no_op);
            set(obj.parent_,'KeyPressFcn', @obj.ui_no_op);
            
            obj.ui_set_button_icon(obj.ui_buttons_.play, 'ui_control_play.png');
            obj.ui_buttons_.play_state = false;
            set(obj.ui_buttons_.play, 'Callback', @obj.ui_button_start);
            obj.ui_toggle_control(obj.ui_buttons_.load, false);
        end
        
        function ui_focus_view(obj, src, event, robot)
%             disp('clicked robot');
            
            switch(get(obj.parent_, 'SelectionType'))
                case 'normal'
%                     disp('single click')
                case 'open'
%                     disp('double click')
                otherwise
            end
            
            pose = simiam.ui.Pose2D(0,0,0);
            
            token_k = obj.simulator_.world.robots.head_;
            while(~isempty(token_k))
                if(token_k.key_.robot == robot)
                    pose = token_k.key_.pose;
                    break;
                end
                token_k = token_k.next_;
            end
            
            obj.center_ = pose;
            obj.ui_set_axes();
            obj.is_tracking_ = true;
        end
        
        function ui_button_play(obj, src, event)
            obj.ui_buttons_.play_state = ~obj.ui_buttons_.play_state;
            if(obj.ui_buttons_.play_state)
                obj.ui_set_button_icon(obj.ui_buttons_.play, 'ui_control_pause.png');
                obj.simulator_.start();
            else
                obj.ui_set_button_icon(obj.ui_buttons_.play, 'ui_control_play.png');
                obj.simulator_.stop();
            end
        end
        
        function ui_close(obj, src, event)
            if(obj.is_ready_)
                obj.simulator_.shutdown();
            end
            delete(src);
        end
        
        function ui_set_axes(obj)
            set(obj.view_, 'XLim', [-1 1]*obj.zoom_level_+obj.center_.x);
            set(obj.view_, 'YLim', ([-1 1]*obj.zoom_level_/obj.ratio_)+obj.center_.y);
             
            tickd = obj.zoom_level_*0.1;
            if(isempty(obj.ticks_))
                obj.ticks_ = [-fliplr(0:tickd:obj.boundary_*2) tickd:tickd:obj.boundary_*2];
            end
            
            set(obj.view_, 'XTick', obj.ticks_);
            set(obj.view_, 'YTick', obj.ticks_);
            set(obj.view_, 'XTickLabel', []);
            set(obj.view_, 'YTickLabel', []);
        end
        
        function ui_zoom_view(obj, src, event, varargin)
            zoom_level_factor = 0.25;
            obj.zoom_level_ = obj.zoom_level_+zoom_level_factor*event.VerticalScrollCount;
            obj.zoom_level_ = min(max(obj.zoom_level_,0.1), obj.boundary_);
            
            if (~obj.is_tracking_)
                if(obj.zoom_level_+obj.center_.x > obj.boundary_)
                    obj.center_.x = obj.boundary_-obj.zoom_level_;
                elseif(-obj.zoom_level_+obj.center_.x < -obj.boundary_)
                    obj.center_.x = -obj.boundary_+obj.zoom_level_;
                end

                if(obj.zoom_level_/obj.ratio_+obj.center_.y > obj.boundary_)
                    obj.center_.y = obj.boundary_-obj.zoom_level_/obj.ratio_;
                elseif(-obj.zoom_level_/obj.ratio_+obj.center_.y < -obj.boundary_)
                    obj.center_.y = -obj.boundary_+obj.zoom_level_/obj.ratio_;
                end
            end
            
            obj.ui_set_axes();
        end
        
        function ui_button_zoom_in(obj, src, event)
            event.VerticalScrollCount = -1;
            obj.ui_zoom_view(src, event);
        end
        
        function ui_button_zoom_out(obj, src, event)
            event.VerticalScrollCount = 1;
            obj.ui_zoom_view(src, event);
        end
        
        function ui_press_mouse(obj, src, event, handles)
            click = get(obj.view_, 'CurrentPoint');
            obj.click_src_ = click(1,1:2)';
            switch(get(obj.parent_, 'SelectionType'))
                case 'extend'
%                     set(obj.parent_, 'WindowButtonMotionFcn', @obj.ui_zoom_view);
                case 'normal'
                    setptr(obj.parent_, 'closedhand');
                    set(obj.parent_, 'WindowButtonMotionFcn', @obj.ui_pan_view);
                case 'open'
%                     set(obj.target_marker_, 'XData', obj.click_src_(1));
%                     set(obj.target_marker_, 'YData', obj.click_src_(2));
%                     obj.simulator_.world.apps.head_.key_.ui_press_mouse(obj.click_src_);
                otherwise
                    % noop
            end
            set(obj.parent_, 'WindowButtonUpFcn', @obj.ui_release_mouse);
        end
        
        function ui_press_key(obj, src, event, handles)
%             disp(event.Key);
        end
        
        function ui_release_mouse(obj, src, event, handles)
%             disp('released')
            setptr(obj.parent_, 'arrow');
            set(obj.parent_, 'WindowButtonMotionFcn', @obj.ui_no_op);
        end
        
        function ui_pan_view(obj, src, event, handles)
            [x, y, theta] = obj.center_.unpack();
            obj.center_ = simiam.ui.Pose2D(x,y,theta);
            
            obj.is_tracking_ = false;
            
            click = get(obj.view_, 'CurrentPoint');
            click_pose = click(1,1:2)';
            diff = (obj.click_src_-click_pose);
            obj.center_.x = obj.center_.x + diff(1);
            obj.center_.y = obj.center_.y + diff(2);
            
            % don't pan out of view
            
            if(obj.zoom_level_+obj.center_.x > obj.boundary_)
                obj.center_.x = obj.boundary_-obj.zoom_level_;
            elseif(-obj.zoom_level_+obj.center_.x < -obj.boundary_)
                obj.center_.x = -obj.boundary_+obj.zoom_level_;
            end
            
            if(obj.zoom_level_/obj.ratio_+obj.center_.y > obj.boundary_)
                obj.center_.y = obj.boundary_-obj.zoom_level_/obj.ratio_;
            elseif(-obj.zoom_level_/obj.ratio_+obj.center_.y < -obj.boundary_)
                obj.center_.y = -obj.boundary_+obj.zoom_level_/obj.ratio_;
            end
            
            obj.ui_set_axes();
        end
        
        function ui_no_op(obj, src, event, handles)
            % do nothing
        end
        
        function ui_resize_view(obj, src, event, handles)
            set(obj.view_, 'Units', 'pixels');
            view_quad = get(obj.view_, 'Position');
            set(obj.view_, 'Units', 'normal');
            width = view_quad(3);
            height = view_quad(4);
            obj.ratio_ = width/height;
            obj.ui_set_axes();
        end
    end
end
