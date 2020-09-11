#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
import gui.frame
import gui.viewer
from models.map_manager import MapManager
from models.robot import Robot
from models.world import World
from views.world_view import WorldView
from sim_exceptions.collision_exception import CollisionException
from sim_exceptions.goal_reached_exception import GoalReachedException

REFRESH_RATE = 20.0  # hertz


class Simulator:
    def __init__(self):
        # create the GUI
        self.viewer = gui.viewer.Viewer(self)

        # create the map manager
        self.map_manager = MapManager()

        # timing control
        self.period = 1.0 / REFRESH_RATE  # seconds

        # Gtk simulation event source - for simulation control
        self.sim_event_source = GLib.idle_add(
            self.initialize_sim, True
        )  # we use this opportunity to initialize the sim

        # start Gtk
        Gtk.main()

    def initialize_sim(self, random=False):
        # reset the viewer
        self.viewer.control_panel_state_init()

        # create the simulation world
        self.world = World(self.period)

        # create the robot
        robot = Robot()
        self.world.add_robot(robot)

        # generate a random environment
        if random:
            self.map_manager.random_map(self.world)
        else:
            self.map_manager.apply_to_world(self.world)

        # create the world view
        self.world_view = WorldView(self.world, self.viewer)

        # render the initial world
        self.draw_world()

    def play_sim(self):
        GLib.source_remove(
            self.sim_event_source
        )  # this ensures multiple calls to play_sim do not speed up the simulator
        self._run_sim()
        self.viewer.control_panel_state_playing()

    def pause_sim(self):
        GLib.source_remove(self.sim_event_source)
        self.viewer.control_panel_state_paused()

    def step_sim_once(self):
        self.pause_sim()
        self._step_sim()

    def end_sim(self, alert_text=""):
        GLib.source_remove(self.sim_event_source)
        self.viewer.control_panel_state_finished(alert_text)

    def reset_sim(self):
        self.pause_sim()
        self.initialize_sim()

    def save_map(self, filename):
        self.map_manager.save_map(filename)

    def load_map(self, filename):
        self.map_manager.load_map(filename)
        self.reset_sim()

    def random_map(self):
        self.pause_sim()
        self.initialize_sim(random=True)

    def draw_world(self):
        self.viewer.new_frame()  # start a fresh frame
        self.world_view.draw_world_to_frame()  # draw the world onto the frame
        self.viewer.draw_frame()  # render the frame

    def _run_sim(self):
        self.sim_event_source = GLib.timeout_add(int(self.period * 1000), self._run_sim)
        self._step_sim()

    def _step_sim(self):
        # increment the simulation
        try:
            self.world.step()
        except CollisionException:
            self.end_sim("Collision!")
        except GoalReachedException:
            self.end_sim("Goal Reached!")

        # draw the resulting world
        self.draw_world()


# RUN THE SIM:
Simulator()
