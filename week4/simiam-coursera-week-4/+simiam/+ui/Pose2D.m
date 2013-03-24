classdef Pose2D < handle
    
% Copyright (C) 2013, Georgia Tech Research Corporation
% see the LICENSE file included with this software
    
    properties
        x
        y
        theta
    end
    
    methods
        function obj = Pose2D(x, y, theta)
           obj.x = x;
           obj.y = y;
           obj.theta = theta;
        end
        
        function set_pose(obj, pose)
%             if isa(pose, 'simiam.ui.Pose2D')
%                 obj.set_pose(pose.unpack());
%             else
                obj.x = pose(1);
                obj.y = pose(2);
                obj.theta = pose(3);
%             end
        end
        
        function [x, y, theta] = unpack(obj)
            x = obj.x;
            y = obj.y;
            theta = obj.theta;
        end
        
        function T = get_transformation_matrix(obj)
            T = [ cos(obj.theta) -sin(obj.theta) obj.x;
                  sin(obj.theta)  cos(obj.theta) obj.y;
                               0               0     1];
        end
    end
    
    methods (Static)
        function rad = deg2rad(deg)
            rad = deg*pi/180;
        end
        
        function deg = rad2deg(rad)
            deg = rad*180/pi;
        end
    end
end