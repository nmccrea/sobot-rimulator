from views.obstacle_view import ObstacleView
from views.robot_view import RobotView

MAJOR_GRIDLINE_INTERVAL = 1.0  # meters
MAJOR_GRIDLINE_SUBDIVISIONS = 5  # minor gridlines for every major gridline


class WorldView:
    def __init__(self, world, viewer):
        # bind the viewer
        self.viewer = viewer

        # initialize views for world objects
        self.robot_views = []
        for robot in world.robots:
            self.add_robot(robot)

        self.obstacle_views = []
        for obstacle in world.obstacles:
            self.add_obstacle(obstacle)

    def add_robot(self, robot):
        robot_view = RobotView(self.viewer, robot)
        self.robot_views.append(robot_view)

    def add_obstacle(self, obstacle):
        obstacle_view = ObstacleView(self.viewer, obstacle)
        self.obstacle_views.append(obstacle_view)

    def draw_world_to_frame(self):
        # draw the grid
        self._draw_grid_to_frame()

        # draw all the robots
        for robot_view in self.robot_views:
            robot_view.draw_robot_to_frame()
        # draw all the obstacles
        for obstacle_view in self.obstacle_views:
            obstacle_view.draw_obstacle_to_frame()

    def _draw_grid_to_frame(self):
        # NOTE: THIS FORMULA ASSUMES THE FOLLOWING:
        # - Window size never changes
        # - Window is always centered at (0, 0)

        # calculate minor gridline interval
        minor_gridline_interval = MAJOR_GRIDLINE_INTERVAL / MAJOR_GRIDLINE_SUBDIVISIONS

        # determine world space to draw grid upon
        meters_per_pixel = 1.0 / self.viewer.pixels_per_meter
        width = meters_per_pixel * self.viewer.view_width_pixels
        height = meters_per_pixel * self.viewer.view_height_pixels
        x_halfwidth = width * 0.5
        y_halfwidth = height * 0.5

        x_max = int(x_halfwidth / minor_gridline_interval)
        y_max = int(y_halfwidth / minor_gridline_interval)

        # build the gridlines
        major_lines_accum = []  # accumulator for major gridlines
        minor_lines_accum = []  # accumulator for minor gridlines

        for i in range(x_max + 1):  # build the vertical gridlines
            x = i * minor_gridline_interval

            if x % MAJOR_GRIDLINE_INTERVAL == 0:  # sort major from minor
                accum = major_lines_accum
            else:
                accum = minor_lines_accum

            accum.append(
                [[x, -y_halfwidth], [x, y_halfwidth]]
            )  # positive-side gridline
            accum.append(
                [[-x, -y_halfwidth], [-x, y_halfwidth]]
            )  # negative-side gridline

        for j in range(y_max + 1):  # build the horizontal gridlines
            y = j * minor_gridline_interval

            if y % MAJOR_GRIDLINE_INTERVAL == 0:  # sort major from minor
                accum = major_lines_accum
            else:
                accum = minor_lines_accum

            accum.append(
                [[-x_halfwidth, y], [x_halfwidth, y]]
            )  # positive-side gridline
            accum.append(
                [[-x_halfwidth, -y], [x_halfwidth, -y]]
            )  # negative-side gridline

        # draw the gridlines
        self.viewer.current_frame.add_lines(
            major_lines_accum,  # draw major gridlines
            linewidth=meters_per_pixel,  # roughly 1 pixel
            color="black",
            alpha=0.2,
        )
        self.viewer.current_frame.add_lines(
            minor_lines_accum,  # draw minor gridlines
            linewidth=meters_per_pixel,  # roughly 1 pixel
            color="black",
            alpha=0.1,
        )
