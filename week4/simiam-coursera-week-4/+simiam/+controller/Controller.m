classdef Controller < handle
%% CONTROLLER is a template for all user-defined controllers.
% 
% controller Properties:
%   type            - Name of the controller
%   state_estimate  - Current estimate of the robot's state
%   prev_ticks      - Previous tick count on the left and right wheels
%
% controller Methods:
%   execute         - Executes the control loop (one iteration).
%   update_odometry - Approximates the location of the robot.
%   uni_to_diff     - Converts from unicycle to differential drive model.
%   deg2rad         - Converts from degrees to radians.
    
    properties
        %% PROPERTIES Controller memory banks
        
        type                % Name of the controller
    end % properties
    
    methods
        %% METHODS
        
        function obj = Controller(type)
        %% CONTROLLER Constructor
        %   obj = controller() is the default constructor that sets the
        %   name of the controller to 'basic', the state estimate to 0, and
        %   the previous tick count to 0.
        
            % initialize memory banks
            obj.type = type;
        end
    end
    
    methods
        
        function outputs = execute(obj, robot, state_estimate, inputs)
        %% EXECUTE Executes the control loop (one iteration).
        %   [...] = obj.execute(robot, ...) is called by the supervisor once every
        %   iteration. This function should compute the control for one
        %   time step only.
        %
        %   This function accepts a variable number of input and output
        %   arguments that allow the user to define any set of inputs and
        %   outputs for the control loop.
            outputs = [];
        end
        
    end % methods
    
end