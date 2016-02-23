from robot import Robot
from math import cos, sin, pi
import random

class Particle:
    def __init__(self, x, y, a, p=1):
        self.x = x
        self.y = y
        self.a = a
	self.p = p;

class ProbabilisticMotion:

    mean = 0
    sd = 0.1
    step = 0.1
    size = 0.4
    numParticles = 100

    scale = 400
    offset = 100
    
    def __init__(self, robot):
        self.robot = robot
        self.particles = [Particle(0, 0, 0)]*self.numParticles

    def noise(self):
        return random.gauss(0.0, 0.5)*0.01

    def printParticles(self):
        scale = self.scale
        offset = self.offset
        print("drawParticles:" + str([(p.x*scale + offset, p.y*scale + offset, p.a) for p in self.particles]))

    def printLine(self, x1, y1, x2, y2):
        scale = self.scale
        offset = self.offset
        print("drawLine:" + str((int(x1*scale) + offset, int(y1*scale) + offset, int(x2*scale) + offset, int(y2*scale) + offset)))

    def updateParticles(self, d):
        self.particles = [Particle(\
            p.x + (d + self.noise())*cos(p.a), \
            p.y + (d + self.noise())*sin(p.a), \
            p.a + self.noise()) for p in self.particles]

    def updateAngle(self, a):
        self.particles = [Particle(p.x, p.y, p.a + a + self.noise()) \
            for p in self.particles]

    def run(self):
        posX = 0
        posY = 0
        angle = 0
        for i in range(0, 4):
            total = 0.0
            while total < self.size:
                self.robot.move(self.step)
                self.robot.wait()
                self.updateParticles(self.step)
                self.printParticles()
                newX = posX + self.step*cos(angle)
                newY = posY + self.step*sin(angle)
                self.printLine(posX, posY, newX, newY)
                posX = newX
                posY = newY
                total += self.step
            self.robot.rotate(90)
            self.robot.wait()
            self.updateAngle(pi/2)
            self.printParticles()
            angle += pi/2

if __name__ == '__main__':
    robot = Robot()
    motion = ProbabilisticMotion(robot)
    motion.run()

