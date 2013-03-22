classdef Drawable < handle

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software
    
    properties
        surfaces
        parent
    end
    
    properties (Access = protected)
        pose
    end
    
    methods
        function obj = Drawable(parent, pose)
           obj.pose = pose;
           obj.parent = parent;
           obj.surfaces = mcodekit.list.dl_list();
        end
    end
    
    methods (Access = protected)
        
        function surface = add_surface(obj, geometry, color)
            surface_g = geometry;
            T = obj.pose.get_transformation_matrix();
            surface_h = patch('Parent', obj.parent, ...
                              'Vertices', geometry*T', ...
                              'Faces', 1:size(geometry,1), ...
                              'FaceColor', 'flat', ...
                              'FaceVertexCData', color);
%             surface = struct('geometry', mcodekit.geometry.Surface2D(surface_g), 'handle', surface_h);
            surface = simiam.ui.Surface2D(surface_h, surface_g);
            surface.transform_surface(T);
            obj.surfaces.append_key(surface);
        end
        
        function draw_surfaces(obj)
            T = obj.pose.get_transformation_matrix();
            
            token_k = obj.surfaces.head_;
            while(~isempty(token_k))
                token_k.key_.transform_surface(T);
                token_k = token_k.next_;
            end
        end
        
%         function transform_surfaces(obj, T)
%             i = obj.surfaces.get_iterator();
%             while(i.has_next())
%                 surface = i.next();
%                 surface.transform(T);
%             end
%         end
        
        function update_pose(obj, pose)
            [x, y, theta] = pose.unpack();
            obj.pose.set_pose([x, y, theta]);
%             obj.transform_surfaces(pose.get_transformation_matrix());
            obj.draw_surfaces();
        end
        
        
    end
end