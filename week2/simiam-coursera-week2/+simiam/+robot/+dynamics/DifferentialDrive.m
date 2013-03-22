classdef DifferentialDrive < simiam.robot.dynamics.Dynamics

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software
    
    properties
        wheel_radius
        wheel_base_length
    end
    
    methods
        function obj = DifferentialDrive(wheel_radius, wheel_base_length)
            obj = obj@simiam.robot.dynamics.Dynamics();
            obj.wheel_radius = wheel_radius;
            obj.wheel_base_length = wheel_base_length;
        end
        
        function pose_t_1 = apply_dynamics(obj, pose_t, dt, vel_r, vel_l)
            R = obj.wheel_radius;
            L = obj.wheel_base_length;
            
%             fprintf('(vel_r,vel_l) = (%0.6g,%0.6g)\n', vel_r,vel_l);
            
            v = R/2*(vel_r+vel_l);
            w = R/L*(vel_r-vel_l);
            
%             fprintf('Calculated velocities (v,w): (%0.3g,%0.3g)\n', v, w);

            [x_k, y_k, theta_k] = pose_t.unpack();

            options = odeset('RelTol',1e-8,'AbsTol',1e-8);
            [t,z] = ode45(@obj.dynamics, [0 dt], [x_k, y_k, theta_k, v, w], options);
            
%             x_k_1 = x_k + dt*(v*cos(theta_k));
%             y_k_1 = y_k + dt*(v*sin(theta_k));
%             theta_k_1 = theta_k + dt*w;
            
%             pose_t_1 = simiam.ui.Pose2D(x_k_1, y_k_1, theta_k_1);
            pose_t_1 = simiam.ui.Pose2D(z(end,1),z(end,2),z(end,3));
        end
        
        function dz = dynamics(obj, t, z)
            dz = zeros(5,1);
            dz(1:2) = z(4)*[cos(z(3));sin(z(3))];
            dz(3) = z(5);
        end
        
        function [vel_r,vel_l] = uni_to_diff(obj,v,w)
            % Make sure to fix this transformation!
            R = obj.wheel_radius;
            L = obj.wheel_base_length;
            
            %% START CODE BLOCK %%
            vel_r = 0;
            vel_l = 0;
            %% END CODE BLOCK %%
        end
        
        function [v,w] = diff_to_uni(obj,r,l)
            R = obj.wheel_radius;
            L = obj.wheel_base_length;
            
            v = R/2*(r+l);
            w = R/L*(r-l);
        end
    end
    
end

