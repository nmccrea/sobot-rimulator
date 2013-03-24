classdef GoToGoal < simiam.controller.Controller
%% GOTOGOAL steers the robot towards a goal with a constant velocity using PID
%
% Properties:
%   none
%
% Methods:
%   execute - Computes the left and right wheel speeds for go-to-goal.

% Copyright (C) 2013, Georgia Tech Research Corporation
% see the LICENSE file included with this software
    
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
            obj.Kp = 5;
            obj.Ki = 0.01;
            obj.Kd = 0.1;
                        
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
            
            % 1. Calculate the heading (angle) to the goal.
            
            % distance between goal and robot in x-direction
            u_x = x_g-x;     
                
            % distance between goal and robot in y-direction
            u_y = y_g-y;
                
            % angle from robot to goal. Hint: use ATAN2, u_x, u_y here.
            theta_g = atan2(u_y,u_x);
            
            % 2. Calculate the heading error.
            
            % error between the goal angle and robot's angle
            % Hint: Use ATAN2 to make sure this stays in [-pi,pi].
            e_k = theta_g-theta;
            e_k = atan2(sin(e_k),cos(e_k));
            
                
            % 3. Calculate PID for the steering angle 
            
            % error for the proportional term
            e_P = e_k;
            
            % error for the integral term. Hint: Approximate the integral using
            % the accumulated error, obj.E_k, and the error for
            % this time step, e_k.
            e_I = obj.E_k + e_k*dt;
                     
            % error for the derivative term. Hint: Approximate the derivative
            % using the previous error, obj.e_k_1, and the
            % error for this time step, e_k.
            e_D = (e_k-obj.e_k_1)/dt;    
                  
            w = obj.Kp*e_P + obj.Ki*e_I + obj.Kd*e_D;
            
            % 4. Save errors for next time step
            obj.E_k = e_I;
            obj.e_k_1 = e_k;
            
            % plot
            [obj.h,obj.g] = obj.p.plot_2d_ref(obj.h, obj.g, dt, theta, theta_g);
            
            outputs = obj.outputs;  % make a copy of the output struct
            outputs.v = v;
            outputs.w = w;
        end
        
    end
    
end

