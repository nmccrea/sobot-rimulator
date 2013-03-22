classdef K3Supervisor < simiam.controller.Supervisor
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
    
        prev_ticks          % Previous tick count on the left and right wheels
        goal
        v
        theta_d
    end
    
    methods
    %% METHODS
        
        function obj = K3Supervisor()
        %% SUPERVISOR Constructor
            obj = obj@simiam.controller.Supervisor();
            
            % initialize the controllers
            obj.controllers{1} = simiam.controller.AvoidObstacles();
            obj.controllers{2} = simiam.controller.GoToGoal();
            obj.controllers{3} = simiam.controller.GoToAngle();
            
            % set the initial controller
            obj.current_controller = obj.controllers{3};
            
            obj.prev_ticks = struct('left', 0, 'right', 0);
            
            obj.goal = [1;0];
            
            %% BEGIN CODE BLOCK %%
            obj.theta_d = pi/4;
            obj.v = 0.1;
            %% END CODE BLOCK %%
        end
        
        function execute(obj, dt)
        %% EXECUTE Selects and executes the current controller.
        %   execute(obj, robot) will select a controller from the list of
        %   available controllers and execute it.
        %
        %   See also controller/execute
                                        
            inputs = obj.current_controller.inputs;
            inputs.theta_d = obj.theta_d;
            inputs.v = obj.v;

            outputs = obj.current_controller.execute(obj.robot, obj.state_estimate, inputs, dt);

            [vel_r, vel_l] = obj.robot.dynamics.uni_to_diff(outputs.v, outputs.w);
            obj.robot.set_wheel_speeds(vel_r, vel_l);
            
            obj.update_odometry();
%             [x, y, theta] = obj.state_estimate.unpack();
%             fprintf('current_pose: (%0.3f,%0.3f,%0.3f)\n', x, y, theta);
        end
        
        function set_current_controller(obj, k)
            obj.current_controller = obj.controllers{k};
        end
        
        function update_odometry(obj)
        %% UPDATE_ODOMETRY Approximates the location of the robot.
        %   obj = obj.update_odometry(robot) should be called from the
        %   execute function every iteration. The location of the robot is
        %   updated based on the difference to the previous wheel encoder
        %   ticks. This is only an approximation.
        %
        %   state_estimate is updated with the new location and the
        %   measured wheel encoder tick counts are stored in prev_ticks.
        
            % Get wheel encoder ticks from the robot
            right_ticks = obj.robot.encoders(1).ticks;
            left_ticks = obj.robot.encoders(2).ticks;
            
            % Recal the previous wheel encoder ticks
            prev_right_ticks = obj.prev_ticks.right;
            prev_left_ticks = obj.prev_ticks.left;
            
            % Previous estimate 
            [x, y, theta] = obj.state_estimate.unpack();
            
            % Compute odometry here
            R = obj.robot.wheel_radius;
            L = obj.robot.wheel_base_length;
            m_per_tick = (2*pi*R)/obj.robot.encoders(1).ticks_per_rev;
            
            
            %% START CODE BLOCK %%
            x_dt = 0;
            y_dt = 0;
            theta_dt = 0;
            
            theta_new = theta + theta_dt;
            x_new = x + x_dt;
            y_new = y + y_dt;                           
%             fprintf('Estimated pose (x,y,theta): (%0.3g,%0.3g,%0.3g)\n', x_new, y_new, theta_new);

            %% END CODE BLOCK %%
            
            % Save the wheel encoder ticks for the next estimate
            obj.prev_ticks.right = right_ticks;
            obj.prev_ticks.left = left_ticks;
            
            % Update your estimate of (x,y,theta)
            obj.state_estimate.set_pose([x_new, y_new, theta_new]);
        end
    end
end
