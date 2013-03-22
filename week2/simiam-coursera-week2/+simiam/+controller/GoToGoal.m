classdef GoToGoal < simiam.controller.Controller
%% GOTOGOAL steers the robot towards a goal with a constant velocity using PID
%
% Properties:
%   none
%
% Methods:
%   execute - Computes the left and right wheel speeds for go-to-goal.
    
    properties
        %% PROPERTIES
        
        % memory banks
        E_k
        e_k_1
        
        % gains
        Kp
        Ki
        Kd
        
        % plot support
        p
        h
        g
    end
    
    properties (Constant)
        % I/O
        inputs = struct('x_g', 0, 'y_g', 0, 'v', 0);
        outputs = struct('v', 0, 'w', 0);
    end
    
    methods
    %% METHODS
        
        function obj = GoToGoal()
            %% GOTOGOAL Constructor
            obj = obj@simiam.controller.Controller('go_to_goal');
            
            % initialize memory banks
            obj.Kp = 10;
            obj.Ki = 0;
            obj.Kd = 0;
                        
            % errors
            obj.E_k = 0;
            obj.e_k_1 = 0;
            
            % plot support
            obj.p = simiam.util.Plotter();
            obj.h = -1;
            obj.g = -1;
        end
        
        function outputs = execute(obj, robot, state_estimate, inputs, dt)
        %% EXECUTE Computes the left and right wheel speeds for go-to-goal.
        %   [v, w] = execute(obj, robot, x_g, y_g, v) will compute the
        %   necessary linear and angular speeds that will steer the robot
        %   to the goal location (x_g, y_g) with a constant linear velocity
        %   of v.
        %
        %   See also controller/execute
        
            % Retrieve the (relative) goal location
            x_g = inputs.x_g; 
            y_g = inputs.y_g;
            
            % Get estimate of current pose
            [x, y, theta] = state_estimate.unpack();
            
            % Compute the v,w that will get you to the goal
            v = inputs.v;
            
            % desired (goal) heading
            dx = x_g-x;
            dy = y_g-y;
            
            theta_d = atan2(dy,dx);
            
            % heading error
            e_k = theta_d-theta;
            e_k = atan2(sin(e_k), cos(e_k));
            
            % PID for heading
            w = obj.Kp*e_k + obj.Ki*(obj.E_k+e_k*dt) + obj.Kd*(e_k-obj.e_k_1)/dt;
            
            % save errors
            obj.E_k = obj.E_k+e_k*dt;
            obj.e_k_1 = e_k;
            
            % stop when sufficiently close
            delta = sqrt(dx^2+dy^2);
            
            if (delta < 0.02)
               v=0;
               w=0;
            end
            
            % plot
            [obj.h,obj.g] = obj.p.plot_2d_ref(obj.h, obj.g, dt, theta, theta_d);
            
            outputs = obj.outputs;  % make a copy of the output struct
            outputs.v = v;
            outputs.w = w;
        end
        
    end
    
end

