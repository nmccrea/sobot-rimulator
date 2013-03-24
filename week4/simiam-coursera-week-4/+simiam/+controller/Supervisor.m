classdef Supervisor < handle
%% SUPERVISOR switches between controllers and handles their inputs/outputs.
%
% Properties:
%   current_controller      - Currently selected controller
%   controllers             - List of available controllers
%   goal_points             - Set of goal points
%   goal_index              - Pointer to current goal point
%   v                       - Robot velocity
%
% Methods:
%   execute - Selects and executes the current controller.

    properties
    %% PROPERTIES
    
        current_controller  % Currently selected controller
        controllers         % List of available controllers
        robot               % The robot
        state_estimate      % Current estimate of the robot's state
    end
    
    methods
    %% METHODS
        
        function obj = Supervisor()
        %% SUPERVISOR Constructor
            
            % initialize the controllers
            obj.controllers{1} = simiam.controller.Controller('default');
            
            % set the initial controller
            obj.current_controller = obj.controllers{1};
            
            obj.robot = [];
            obj.state_estimate = simiam.ui.Pose2D(0,0,0);
        end
        
        function attach_robot(obj, robot, pose)
            obj.robot = robot;
            [x, y, theta] = pose.unpack();
            obj.state_estimate.set_pose([x, y, theta]);
        end
        
        function execute(obj, dt)
        %% EXECUTE Selects and executes the current controller.
        %   execute(obj, dt) will select a controller from the list of
        %   available controllers and execute it.
        %
        %   See also controller/execute
        end
    end
end
