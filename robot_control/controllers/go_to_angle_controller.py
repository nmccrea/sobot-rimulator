from utils import math_util


class GoToAngleController:
    def __init__(self, supervisor):
        # bind the supervisor
        self.supervisor = supervisor

        # gains
        self.k_p = 5.0

    def execute(self, theta_d):
        theta = self.supervisor.estimated_pose().theta
        e = math_util.normalize_angle(theta_d - theta)
        omega = self.k_p * e

        self.supervisor.set_outputs(1.0, omega)
