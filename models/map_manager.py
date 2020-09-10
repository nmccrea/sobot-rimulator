from math import pi, sin, cos
from random import random, randrange
import pickle
from models.pose import Pose
from models.polygon import Polygon
from models.rectangle_obstacle import RectangleObstacle
import utils.geometrics_util as geometrics

# random environment parameters
OBS_MIN_DIM = 0.1  # meters
OBS_MAX_DIM = 2.5  # meters
OBS_MAX_COMBINED_DIM = 2.6  # meters
OBS_MIN_COUNT = 10
OBS_MAX_COUNT = 50
OBS_MIN_DIST = 0.4  # meters
OBS_MAX_DIST = 6.0  # meters
GOAL_MIN_DIST = 2.0  # meters
GOAL_MAX_DIST = 4.0  # meters
MIN_GOAL_CLEARANCE = 0.2  # meters


class MapManager:
    def __init__(self):
        self.current_obstacles = []
        self.current_goal = None

    def random_map(self, world):
        # OBSTACLE PARAMS
        obs_min_dim = OBS_MIN_DIM
        obs_max_dim = OBS_MAX_DIM
        obs_max_combined_dim = OBS_MAX_COMBINED_DIM
        obs_min_count = OBS_MIN_COUNT
        obs_max_count = OBS_MAX_COUNT
        obs_min_dist = OBS_MIN_DIST
        obs_max_dist = OBS_MAX_DIST

        # GOAL PARAMS
        goal_min_dist = GOAL_MIN_DIST
        goal_max_dist = GOAL_MAX_DIST

        # BUILD RANDOM ELEMENTS
        # generate the goal
        goal_dist_range = goal_max_dist - goal_min_dist
        dist = goal_min_dist + (random() * goal_dist_range)
        phi = -pi + (random() * 2 * pi)
        x = dist * sin(phi)
        y = dist * cos(phi)
        goal = [x, y]

        # generate a proximity test geometry for the goal
        r = MIN_GOAL_CLEARANCE
        n = 6
        goal_test_geometry = []
        for i in range(n):
            goal_test_geometry.append(
                [x + r * cos(i * 2 * pi / n), y + r * sin(i * 2 * pi / n)]
            )
        goal_test_geometry = Polygon(goal_test_geometry)

        # generate the obstacles
        obstacles = []
        obs_dim_range = obs_max_dim - obs_min_dim
        obs_dist_range = obs_max_dist - obs_min_dist
        num_obstacles = randrange(obs_min_count, obs_max_count + 1)

        test_geometries = [r.global_geometry for r in world.robots] + [
            goal_test_geometry
        ]
        while len(obstacles) < num_obstacles:

            # generate dimensions
            width = obs_min_dim + (random() * obs_dim_range)
            height = obs_min_dim + (random() * obs_dim_range)
            while width + height > obs_max_combined_dim:
                height = obs_min_dim + (random() * obs_dim_range)

            # generate position
            dist = obs_min_dist + (random() * obs_dist_range)
            phi = -pi + (random() * 2 * pi)
            x = dist * sin(phi)
            y = dist * cos(phi)

            # generate orientation
            theta = -pi + (random() * 2 * pi)

            # test if the obstacle overlaps the robots or the goal
            obstacle = RectangleObstacle(width, height, Pose(x, y, theta))
            intersects = False
            for test_geometry in test_geometries:
                intersects |= geometrics.convex_polygon_intersect_test(
                    test_geometry, obstacle.global_geometry
                )
            if not intersects:
                obstacles.append(obstacle)

        # update the current obstacles and goal
        self.current_obstacles = obstacles
        self.current_goal = goal

        # apply the new obstacles and goal to the world
        self.apply_to_world(world)

    def save_map(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.current_obstacles, file)
            pickle.dump(self.current_goal, file)

    def load_map(self, filename):
        with open(filename, "rb") as file:
            self.current_obstacles = pickle.load(file)
            self.current_goal = pickle.load(file)

    def apply_to_world(self, world):
        # add the current obstacles
        for obstacle in self.current_obstacles:
            world.add_obstacle(obstacle)

        # program the robot supervisors
        for robot in world.robots:
            robot.supervisor.goal = self.current_goal[:]
