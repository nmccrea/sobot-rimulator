classdef Surface2D < handle

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software
    
    properties
        centroid_
        geometry_
        handle_
        geometric_span_
        edge_set_
    end
    
    properties (Access = private)
        vertex_set_
        is_drawable_
    end
    
    methods
        function obj = Surface2D(varargin)
            switch(nargin)
                case 1,
                    obj.geometry_ = varargin{1};
                    obj.is_drawable_ = false;
                case 2,
                    obj.handle_ = varargin{1};
                    obj.geometry_ = varargin{2};
                    obj.is_drawable_ = true;
                otherwise
                    error('expected 1 or 2 arguments');
            end
            obj.vertex_set_ = obj.geometry_;
            
            % compute the surface's centroid
%             obj.centroid_ = mean(obj.geometry_(:,1:2));
            n = size(obj.geometry_,1);
            obj.centroid_ = sum(obj.geometry_(:,1:2),1)/n;
            
            % compute the surface's geometric span
            obj.geometric_span_ = 2*max(sqrt((obj.geometry_(:,1)-obj.centroid_(1)).^2+(obj.geometry_(:,2)-obj.centroid_(2)).^2));
            
            obj.edge_set_ = [obj.geometry_(:,1:2) obj.geometry_([2:n,1],1:2)];
        end
        
        function transform_surface(obj, T)
            obj.geometry_ = obj.vertex_set_*T';
            n = size(obj.geometry_,1);
            obj.edge_set_(:,1:2) = obj.geometry_(:,1:2);
            obj.edge_set_(:,3:4) = obj.geometry_([2:n,1],1:2);
            obj.centroid_ = sum(obj.geometry_(:,1:2),1)/n;
            if(obj.is_drawable_)
                set(obj.handle_, 'Vertices', obj.geometry_);
            end
        end
        
        function update_geometry(obj, geometry)
            obj.vertex_set_ = geometry;
%             obj.centroid_ = sum(obj.geometry_(:,1:2),1)/size(obj.geometry_,1);
%             obj.geometric_span_ = 2*max(sqrt((obj.geometry_(:,1)-obj.centroid_(1)).^2+(obj.geometry_(:,2)-obj.centroid_(2)).^2));
%             obj.geometric_span_ = 2*max(sqrt((obj.vertex_set_(:,1)-obj.centroid_(1)).^2+(obj.vertex_set_(:,2)-obj.centroid_(2)).^2));
        end
        
        function bool = precheck_surface(obj, surface)
%             d = norm(obj.centroid_-surface_b.centroid_);
            d = sqrt((obj.centroid_(1)-surface.centroid_(1))^2+(obj.centroid_(2)-surface.centroid_(2))^2);
            bool = (d < (obj.geometric_span_+surface.geometric_span_)/sqrt(3));
        end
        
        function points = intersection_with_surface(obj, surface, is_cursory)
            edge_set_a = obj.edge_set_;
            edge_set_b = surface.edge_set_';
            
            n_edges_a = size(edge_set_a,1);
            n_edges_b = size(edge_set_b,2);
            
            m_x_1 = edge_set_a(:,1*ones(n_edges_b,1));
            m_x_2 = edge_set_a(:,3*ones(n_edges_b,1));
            m_x_3 = edge_set_b(1*ones(1,n_edges_a),:);
            m_x_4 = edge_set_b(3*ones(1,n_edges_a),:);
            
            m_y_1 = edge_set_a(:,2*ones(n_edges_b,1));
            m_y_2 = edge_set_a(:,4*ones(n_edges_b,1));
            m_y_3 = edge_set_b(2*ones(1,n_edges_a),:);
            m_y_4 = edge_set_b(4*ones(1,n_edges_a),:);
       
            m_y_13 = (m_y_1-m_y_3);
            m_x_13 = (m_x_1-m_x_3);
            m_x_21 = (m_x_2-m_x_1);
            m_y_21 = (m_y_2-m_y_1);    
            m_x_43 = (m_x_4-m_x_3);
            m_y_43 = (m_y_4-m_y_3);
            
            n_edge_a = (m_x_43.*m_y_13)-(m_y_43.*m_x_13);
            n_edge_b = (m_x_21.*m_y_13)-(m_y_21.*m_x_13);
            d_edge_ab = (m_y_43.*m_x_21)-(m_x_43.*m_y_21);
            
            u_a = (n_edge_a./d_edge_ab);
            u_b = (n_edge_b./d_edge_ab);
            
            intersect_set_x = m_x_1+(m_x_21.*u_a);
            intersect_set_y = m_y_1+(m_y_21.*u_a);
            is_in_segment = (u_a >= 0) & (u_a <= 1) & (u_b >= 0) & (u_b <= 1);

            points = [intersect_set_x(is_in_segment) intersect_set_y(is_in_segment)];
        end
    
%         function points = intersection_with_surface(obj, surface, is_cursory)
% %             points = mcodekit.list.dl_list();
%             intersections = 0;
%             
%             % iterate over this surface's edge set
%             n = size(obj.geometry_, 1);
%             m = size(surface.geometry_, 1);
%             
%             points = zeros(n*m,2);
%             
%             for k = 1:n
%                 edge_a = obj.geometry_([k,mod(k,n)+1],1:2);
%                 
%                 % iterate over the other surface's edge set
%                 for l = 1:m
%                     edge_b = surface.geometry_([l,mod(l,m)+1],1:2);
%                     
%                     diff_set = [edge_a(2,:)-edge_a(1,:); edge_b(2,:)-edge_b(1,:)];
%                     diff_set_t = (edge_a-edge_b);
%                     
%                     var_ab_d = diff_set(1,1)*diff_set(2,2)-diff_set(1,2)*diff_set(2,1);
%                     var_a_n = diff_set(2,1)*diff_set_t(1,2)-diff_set(2,2)*diff_set_t(1,1);
%                     var_a = var_a_n/var_ab_d;
%                     var_b_n = diff_set(1,1)*diff_set_t(1,2)-diff_set(1,2)*diff_set_t(1,1);
%                     var_b = var_b_n/var_ab_d;
%                     
%                     point = edge_a(1,:)+var_a*diff_set(1,:);
%                     
% %                     if((var_a_n == 0 && var_b_n == 0) && var_ab_d == 0)
% %                         fprintf('edge are coincident\n');
% %                     elseif (var_ab_d == 0)
% %                         fprintf('edges are parallel\n');
% %                     else
%                         is_point_in_segment = (0 <= var_a && var_a <= 1) && (0 <= var_b && var_b <= 1);
%                         if(is_point_in_segment)
%                             if(is_cursory)
%                                 points = [];
%                                 return;
%                             end
%                             intersections = intersections+1;
%                             points(intersections,:) = point;
% %                         else
% %                             fprintf('intersection point is not in any line segment\n');
%                         end
% %                     end
%                 end
%             end
%             if(intersections > 0)
%                 points = points(1:intersections,:);
%             else
%                 points = [];
%             end
%         end
    end
end

