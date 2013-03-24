classdef GoToAngle < simiam.controller.Controller
%% GOTOANGLE steers the robot towards a angle with a constant velocity using PID
%
% Properties:
%   none
%
% Methods:
%   execute - Computes the left and right wheel speeds for go-to-angle.
    
    properties
        %% PROPERTIES
        
        % memory banks
        
        % gains
        Kp
        
        % plot support
        p
        h
        g
    end
    
    properties (Constant)
        % I/O
        inputs = struct('theta_d', 0, 'v', 0);
        outputs = struct('v', 0, 'w', 0);
    end
    
    methods
    %% METHODS
        
        function obj = GoToAngle()
            %% GOTOANGLE Constructor
            obj = obj@simiam.controller.Controller('go_to_angle');
            
            % initialize memory banks
            obj.Kp = 10;
            
            % plot support
            obj.p = simiam.util.Plotter();
            obj.h = -1;
            obj.g = -1;
        end
        
        function outputs = execute(obj, robot, state_estimate, inputs, dt)
        %% EXECUTE Computes the left and right wheel speeds for go-to-angle.
        %   [v, w] = execute(obj, robot, x_g, y_g, v) will compute the
        %   necessary linear and angular speeds that will steer the robot
        %   to the angle location (x_g, y_g) with a constant linear velocity
        %   of v.
        %
        %   See also controller/execute
        
            % Retrieve the (relative) angle location
            theta_d = inputs.theta_d;
            
            % Get estimate of current pose
            [x, y, theta] = state_estimate.unpack();
            
            % Compute the v,w that will get you to the angle
            v = inputs.v;
            
            % heading error
            e_k = theta_d-theta;
            e_k = atan2(sin(e_k), cos(e_k));
            
            % PID for heading
            w = obj.Kp*e_k;
            
            % plot
            [obj.h,obj.g] = obj.p.plot_2d_ref(obj.h, obj.g, dt, theta, theta_d);
            
            % print IR measured distances
            ir_distances = robot.get_ir_distances();
%             for i=1:9
%                 fprintf('IR %d: %0.3fm\n', i, ir_distances(i));
%             end
            
            outputs = obj.outputs;  % make a copy of the output struct
            outputs.v = v;
            outputs.w = w;
        end
        
    end
    
end

