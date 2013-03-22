classdef Simulator < handle
%% SIMULATOR is responsible for stepping the program through the simulation.
%
% Simulator Properties:
%   parent          - AppWindow graphics handle
%   clock           - Global timer for the simulation
%   time_step       - Time step for the simulation
%   split           - Split between calls to step()
%
% Simulator Methods:
%   step            - Executes one time step of the simulation.
%   start           - Starts the simulation.
%   stop            - Stops the simulation.

% Copyright (C) 2012 Jean-Pierre de la Croix
% see the LICENSE file included with this software

    properties
        %% PROPERTIES
        
        parent          % AppWindow graphics handle
        clock           % Global timer for the simulation
        time_step       % Time step for the simulation
        
        world           % A virtual world for the simulator
        physics
    end
    
    methods
        %% METHODS
        
        function obj = Simulator(parent, world, time_step)
        %% SIMULATOR Constructor
        %   obj = Simulator(parent, time_step) is the default constructor
        %   that sets the graphics handle and the time step for the
        %   simulation.
        
            obj.parent = parent;
            obj.time_step = time_step;
            obj.clock = timer('Period', obj.time_step, ...
                              'TimerFcn', @obj.step, ...
                              'ExecutionMode', 'fixedRate');
            obj.world = world;
            obj.physics = simiam.simulator.Physics(world);
        end
        
        function step(obj, src, event)
        %% STEP Executes one time step of the simulation.
        %   step(obj, src, event) is the timer callback which is executed
        %   once every time_step seconds.
            
            split = max(obj.time_step,get(obj.clock, 'InstantPeriod'));
%             fprintf('***TIMING***\nsimulator split: %0.3fs, %0.3fHz\n', split, 1/split);
            
%             tstart = tic;
            token_k = obj.world.robots.head_;
            while (~isempty(token_k))
                robot_s = token_k.key_;
                robot_s.supervisor.execute(split);
                [x, y, theta] = robot_s.robot.update_state(robot_s.pose, split).unpack();
                robot_s.pose.set_pose([x, y, theta]);
                token_k = token_k.next_;
            end
%             fprintf('controls: %0.3fs\n', toc(tstart));
            
%             tstart = tic;
            obj.world.apps.head_.key_.run(split);
%             fprintf('app: %0.3fs\n', toc(tstart));
            
            bool = obj.physics.apply_physics();
            
%             tstart = tic;
            obj.parent.ui_update(split, bool);
            drawnow;
%             fprintf('ui: %0.3fs\n', toc(tstart));
        end
        
        function start(obj)
        %% START Starts the simulation.
        
            start(obj.clock);
        end
        
        function stop(obj)
        %% STOP Stops the simulation.
        
            stop(obj.clock);
        end
        
        function shutdown(obj)
            obj.stop();
            delete(obj.clock);
        end
    end
    
end