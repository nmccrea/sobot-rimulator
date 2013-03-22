classdef Physics < handle

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software
    
    properties
        world
    end
    
    methods
        function obj = Physics(world)
            obj.world = world;
        end
        
        function bool = apply_physics(obj)
%             tstart = tic;
            bool = obj.body_collision_detection();
            if (bool)
                return;
            end
%             telapsed = toc(tstart);
%             fprintf('body_collision_detect(): %0.3fs\n', telapsed);
            
%             tstart = tic;
            obj.proximity_sensor_detection();
%             telapsed = toc(tstart);
%             fprintf('proximity_sensor_detect(): %0.3fs\n', telapsed);
        end
        
        function bool = body_collision_detection(obj)
            token_k = obj.world.robots.head_; 
            while (~isempty(token_k))
                robot = token_k.key_.robot;
                body_r_s = robot.surfaces.head_.key_;
                
                % check against obstacles
                token_l = obj.world.obstacles.head_;
                while (~isempty(token_l))
                    obstacle = token_l.key_.obstacle;
                    body_o_s = obstacle.surfaces.head_.key_;
                    
                    if(body_r_s.precheck_surface(body_o_s))
                        pts = body_r_s.intersection_with_surface(body_o_s, true);
%                         bool = (pts.size_ > 0);
                        bool = (size(pts,1) > 0);
                        if (bool)
                            fprintf('COLLISION!\n');
                            return;
                        end
                    end
                    token_l = token_l.next_;
                end
                
                % check against other robots
                token_l = obj.world.robots.head_;
                while (~isempty(token_l))
                    robot_o = token_l.key_.robot;
                    if(robot_o ~= robot)
                        body_o_s = robot_o.surfaces.head_.key_;
                        
                        if(body_r_s.precheck_surface(body_o_s))
                            pts = body_r_s.intersection_with_surface(body_o_s, true);
%                             bool = (pts.size_ > 0);
                            bool = (size(pts,1) > 0);
                            if (bool)
                                fprintf('COLLISION!\n');
                                return;
                            end
                        end
                    end
                    token_l = token_l.next_;
                end
                token_k = token_k.next_;
            end
        end
        
        function proximity_sensor_detection(obj)
            token_k = obj.world.robots.head_();
            while (~isempty(token_k))
                robot = token_k.key_.robot;
                for i = 1:length(robot.ir_array)
                    ir = robot.ir_array(i);
                    body_ir_s = ir.surfaces.head_.key_;
                    d_min = ir.max_range;
                    ir.update_range(d_min);

                    % check against obstacles
                    token_l = obj.world.obstacles.head_;
                    while (~isempty(token_l))
                        obstacle = token_l.key_.obstacle;
                        body_o_s = obstacle.surfaces.head_.key_;
                        
                        if(body_ir_s.precheck_surface(body_o_s))
                            d_min = obj.update_proximity_sensor(ir, body_ir_s, body_o_s, d_min);
                        end
                        token_l = token_l.next_;
                    end

                    % check against other robots
                    token_l = obj.world.robots.head_;
                    while (~isempty(token_l))
                        robot_o = token_l.key_.robot;
                        if(robot_o ~= robot)
                            body_o_s = robot_o.surfaces.head_.key_;
                            
                            if(body_ir_s.precheck_surface(body_o_s))
                                d_min = obj.update_proximity_sensor(ir, body_ir_s, body_o_s, d_min);
                            end
                        end
                        token_l = token_l.next_;
                    end
                    
                    if(d_min < ir.max_range)
                        ir.update_range(d_min);
                    end
                end
                token_k = token_k.next_;
            end
        end
    end
        
    methods (Access = private)

        function d_min = update_proximity_sensor(obj, sensor, sensor_surface, obstacle_surface, d_min)
            pts = sensor_surface.intersection_with_surface(obstacle_surface, false);
            n = size(pts,1);
            for k = 1:n
                pt = pts(k,:);
%                 d = norm(pt-sensor_surface.geometry_(1,1:2));
                d = sqrt((pt(1)-sensor_surface.geometry_(1,1))^2+(pt(2)-sensor_surface.geometry_(1,2))^2);
                d = sensor.limit_to_sensor(d);
                if (d < d_min)
                    d_min = d;
                end
            end
        end
    end
    
end

