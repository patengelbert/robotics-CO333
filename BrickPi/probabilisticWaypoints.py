from navigateToWaypoint import Navigate
from probabilisticMotion import ProbabilisticMotion
import math
from robot import Robot

class ProbabilisticWaypoints:
    
    def __init__(self, robot):
        self.navigate = Navigate(robot)
        self.motion = ProbabilisticMotion(robot)
    
    waypoints = [(0, 0.2), (0.2, 0), (0.2, 0.2), (0, 0)]
    
    def run(self):
        for wp in self.waypoints:
            self.motion.printParticles()
            oldAngle = self.navigate.theta
            self.navigate.waypoint(wp)
            self.motion.updateAngle(math.radians(self.navigate.theta - oldAngle))
            self.motion.updateParticles(self.navigate.distance)
            self.motion.updatePosition(self.navigate)

            
if __name__ == '__main__':
    robot = Robot()
    behaviour = ProbabilisticWaypoints(robot)
    behaviour.run()
