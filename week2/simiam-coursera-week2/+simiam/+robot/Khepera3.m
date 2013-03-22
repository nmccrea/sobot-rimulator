classdef Khepera3 < simiam.robot.Robot

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software
    
    properties
        wheel_radius
        wheel_base_length
        ticks_per_rev
        speed_factor
        
        encoders = simiam.robot.sensor.WheelEncoder.empty(1,0);
        ir_array = simiam.robot.sensor.ProximitySensor.empty(1,0);
        
        dynamics
    end
    
    properties (SetAccess = private)
        right_wheel_speed
        left_wheel_speed
    end
    
    methods
        function obj = Khepera3(parent, pose)
           obj = obj@simiam.robot.Robot(parent, pose);
           
           % Add surfaces: Khepera3 in top-down 2D view
           k3_top_plate =  [ -0.031   0.043    1;
                             -0.031  -0.043    1;
                              0.033  -0.043    1;
                              0.052  -0.021    1;
                              0.057       0    1;
                              0.052   0.021    1;
                              0.033   0.043    1];
                          
           k3_base =  [ -0.024   0.064    1;
                         0.033   0.064    1;
                         0.057   0.043    1;
                         0.074   0.010    1;
                         0.074  -0.010    1;
                         0.057  -0.043    1;
                         0.033  -0.064    1;
                        -0.025  -0.064    1;
                        -0.042  -0.043    1;
                        -0.048  -0.010    1;
                        -0.048   0.010    1;
                        -0.042   0.043    1];
            
            obj.add_surface(k3_base, [ 0.8 0.8 0.8 ]);
            obj.add_surface(k3_top_plate, [ 0.0 0.0 0.0 ]);
            
            % Add sensors: wheel encoders and IR proximity sensors
            obj.wheel_radius = 0.021;           % 42mm
            obj.wheel_base_length = 0.0885;     % 88.5mm
            obj.ticks_per_rev = 2765;
            obj.speed_factor = 6.2953e-6;
            
            obj.encoders(1) = simiam.robot.sensor.WheelEncoder('right_wheel', obj.wheel_radius, obj.wheel_base_length, obj.ticks_per_rev);
            obj.encoders(2) = simiam.robot.sensor.WheelEncoder('left_wheel', obj.wheel_radius, obj.wheel_base_length, obj.ticks_per_rev);
            
            import simiam.robot.sensor.ProximitySensor;
            import simiam.robot.Khepera3;
            import simiam.ui.Pose2D;
            
            ir_pose = Pose2D(-0.038, 0.048, Pose2D.deg2rad(128));
            obj.ir_array(1) = ProximitySensor(parent, 'IR', pose, ir_pose, 0.02, 0.2, Pose2D.deg2rad(20), 'simiam.robot.Khepera3.ir_distance_to_raw');
            
            ir_pose = Pose2D(0.019, 0.064, Pose2D.deg2rad(75));
            obj.ir_array(2) = ProximitySensor(parent, 'IR', pose, ir_pose, 0.02, 0.2, Pose2D.deg2rad(20), 'simiam.robot.Khepera3.ir_distance_to_raw');
            
            ir_pose = Pose2D(0.050, 0.050, Pose2D.deg2rad(42));
            obj.ir_array(3) = ProximitySensor(parent, 'IR', pose, ir_pose, 0.02, 0.2, Pose2D.deg2rad(20), 'simiam.robot.Khepera3.ir_distance_to_raw');
            
            ir_pose = Pose2D(0.070, 0.017, Pose2D.deg2rad(13));
            obj.ir_array(4) = ProximitySensor(parent, 'IR', pose, ir_pose, 0.02, 0.2, Pose2D.deg2rad(20), 'simiam.robot.Khepera3.ir_distance_to_raw');
            
            ir_pose = Pose2D(0.070, -0.017, Pose2D.deg2rad(-13));
            obj.ir_array(5) = ProximitySensor(parent, 'IR', pose, ir_pose, 0.02, 0.2, Pose2D.deg2rad(20), 'simiam.robot.Khepera3.ir_distance_to_raw');
            
            ir_pose = Pose2D(0.050, -0.050, Pose2D.deg2rad(-42));
            obj.ir_array(6) = ProximitySensor(parent, 'IR', pose, ir_pose, 0.02, 0.2, Pose2D.deg2rad(20), 'simiam.robot.Khepera3.ir_distance_to_raw');
            
            ir_pose = Pose2D(0.019, -0.064, Pose2D.deg2rad(-75));
            obj.ir_array(7) = ProximitySensor(parent, 'IR', pose, ir_pose, 0.02, 0.2, Pose2D.deg2rad(20), 'simiam.robot.Khepera3.ir_distance_to_raw');
            
            ir_pose = Pose2D(-0.038, -0.048, Pose2D.deg2rad(-128));
            obj.ir_array(8) = ProximitySensor(parent, 'IR', pose, ir_pose, 0.02, 0.2, Pose2D.deg2rad(20), 'simiam.robot.Khepera3.ir_distance_to_raw');
            
            ir_pose = Pose2D(-0.048, 0.000, Pose2D.deg2rad(180));
            obj.ir_array(9) = ProximitySensor(parent, 'IR', pose, ir_pose, 0.02, 0.2, Pose2D.deg2rad(20), 'simiam.robot.Khepera3.ir_distance_to_raw');
            
            % Add dynamics: two-wheel differential drive
            obj.dynamics = simiam.robot.dynamics.DifferentialDrive(obj.wheel_radius, obj.wheel_base_length);
            
            obj.right_wheel_speed = 0;
            obj.left_wheel_speed = 0;
        end
        
        function ir_distances = get_ir_distances(obj)
            ir_array_values = [obj.ir_array.get_range()];
            
            %% START EDIT BLOCK
            ir_distances = ir_array_values.*1;
            % OR
%             ir_distances = zeros(1,9);
%             for i = 1:9
%                 ir_distances(i) = ir_array_values(i)*1;
%             end
            %% END EDIT BLOCK
        end
        
        function pose = update_state(obj, pose, dt)
            sf = obj.speed_factor;
            R = obj.wheel_radius;
            
            vel_r = obj.right_wheel_speed*(sf/R);     % mm/s
            vel_l = obj.left_wheel_speed*(sf/R);      % mm/s
            
            pose = obj.dynamics.apply_dynamics(pose, dt, vel_r, vel_l);
            obj.update_pose(pose);
            
            for k=1:length(obj.ir_array)
                obj.ir_array(k).update_pose(pose);
            end
            
            % update wheel encoders
            sf = obj.speed_factor;
            R = obj.wheel_radius;
            
            vel_r = obj.right_wheel_speed*(sf/R); %% mm/s
            vel_l = obj.left_wheel_speed*(sf/R); %% mm/s
            
            obj.encoders(1).update_ticks(vel_r, dt);
            obj.encoders(2).update_ticks(vel_l, dt);
        end
        
        function set_wheel_speeds(obj, vel_r, vel_l)
            [vel_r, vel_l] = obj.limit_speeds(vel_r, vel_l);
            
            sf = obj.speed_factor;
            R = obj.wheel_radius;
            
            obj.right_wheel_speed = floor(vel_r*(R/sf));
            obj.left_wheel_speed = floor(vel_l*(R/sf));
        end
        
        function [vel_r, vel_l] = limit_speeds(obj, vel_r, vel_l)
            % actuator hardware limits
            [v,w] = obj.dynamics.diff_to_uni(vel_r, vel_l);
            v = max(min(v,0.314),-0.3148);
            w = max(min(w,2.276),-2.2763);
            [vel_r, vel_l] = obj.dynamics.uni_to_diff(v,w);
        end
    end
    
    methods (Static)
        function raw = ir_distance_to_raw(varargin)
            distance = cell2mat(varargin);
            if(distance < 0.02)
                raw = 3960;
            else
                raw = ceil(3960*exp(-30*(distance-0.02)));
            end
        end
    end
    
end

