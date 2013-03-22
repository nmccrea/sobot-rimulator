classdef AvoidObstacles < simiam.controller.Controller
    %AVOID_OBSTACLES Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        R
        RT
        sensor_angles
    end
    
    properties (Constant)
        inputs = struct('v', 0);
        outputs = struct('v', 0, 'w', 0)
    end
    
    methods
        
        function obj = AvoidObstacles()
            obj = obj@simiam.controller.Controller('avoid_obstacles');
            
            obj.R = @(theta)([cos(theta) -sin(theta); sin(theta) cos(theta)]);
            obj.RT = @(x,y,theta)([cos(theta) -sin(theta) x; sin(theta) cos(theta) y; 0 0 1]);
            
            import simiam.ui.Pose2D;
            obj.sensor_angles = [Pose2D.deg2rad(128); Pose2D.deg2rad(75); Pose2D.deg2rad(42); ...
                                 Pose2D.deg2rad(13); Pose2D.deg2rad(-13); Pose2D.deg2rad(-42);
                                 Pose2D.deg2rad(-75); Pose2D.deg2rad(-128); Pose2D.deg2rad(180)];
        end
        
        function outputs = execute(obj, robot, state_estimate, inputs, dt)
            
            % Poll the current IR sensor values 1-9
            ir_array_values = [robot.ir_array.get_range()];
            
            % Update the odometry
            [x, y, theta] = state_estimate.unpack();
            
            % Interpret the IR sensor measurements geometrically
            
            % Compute the heading vector
            theta_d = 0;
            
            % Compute the control
            v = inputs.v;
            w = 0;
            
%             fprintf('(v,w) = (%0.4g,%0.4g)\n', v,w);
            
            % Transform from v,w to v_r,v_l and set the speed of the robot
            outputs.v = v;
            outputs.w = w;
        end
        
        
    end
    
end

