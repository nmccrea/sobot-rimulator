from models.physics import Physics


class World:
    def __init__(self, dt=0.05):
        # initialize physics engine
        self.physics = Physics(self)

        # initialize world time
        self.world_time = 0.0  # seconds
        self.dt = dt  # seconds

        # initialize lists of world objects
        self.supervisors = []
        self.robots = []
        self.obstacles = []

    # step the simulation through one time interval
    def step(self):
        dt = self.dt

        # step all the robots
        for robot in self.robots:
            # step robot motion
            robot.step_motion(dt)

        # apply physics interactions
        self.physics.apply_physics()

        # NOTE: the supervisors must run last to ensure they are observing the "current"
        # world step all of the supervisors
        for supervisor in self.supervisors:
            supervisor.step(dt)

        # increment world time
        self.world_time += dt

    def add_robot(self, robot):
        self.robots.append(robot)
        self.supervisors.append(robot.supervisor)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    # return all objects in the world that might collide with other objects in the
    # world during simulation
    def colliders(self):
        # moving objects only
        return (
            self.robots
        )  # as obstacles are static we should not test them against each other

    # return all solids in the world
    def solids(self):
        return self.robots + self.obstacles
