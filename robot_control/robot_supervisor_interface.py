# a class representing the available interactions a supervisor may have with a robot
class RobotSupervisorInterface:
    def __init__(self, robot):
        self.robot = robot

    # read the proximity sensors
    def read_proximity_sensors(self):
        return [s.read() for s in self.robot.ir_sensors]

    # read the wheel encoders
    def read_wheel_encoders(self):
        return [e.read() for e in self.robot.wheel_encoders]

    # apply wheel drive command
    def set_wheel_drive_rates(self, v_l, v_r):
        self.robot.set_wheel_drive_rates(v_l, v_r)
