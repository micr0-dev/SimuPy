import math
import matplotlib.pyplot as plt
import numpy as np


class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def one():
        return Vector2(1, 1)

    def zero():
        return Vector2()

    def up():
        return Vector2(0, 1)

    def down():
        return Vector2(0, -1)

    def left():
        return Vector2(1, 0)

    def right():
        return Vector2(-1, 0)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, num: int):
        return Vector2(self.x * num, self.y * num)

    def __truediv__(self, num: int):
        return Vector2(self.x / num, self.y / num)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __pow__(self, num: int):
        return Vector2(self.x**num, self.y**num)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def sqrMagnitude(self):
        return self.x**2 + self.y**2

    def dist(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def normalized(self):
        magTemp = self.magnitude()
        return Vector2(self.x / magTemp, self.y / magTemp)

    def angle(self):
        if self.x == 0:
            if self.y > 0:
                return math.pi / 2
            elif self.y < 0:
                return -math.pi / 2
            else:
                return 0
        else:
            return math.atan(self.y / self.x)

    def rotate_ip(self, angle):
        # Rotate this vector by the given angle (in degrees) in place.
        angle_radians = math.radians(angle)
        cos_theta = math.cos(angle_radians)
        sin_theta = math.sin(angle_radians)
        x = self.x * cos_theta - self.y * sin_theta
        y = self.x * sin_theta + self.y * cos_theta
        self.x = x
        self.y = y

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def tuple(self):
        return (self.x, self.y)


class Body:
    def __init__(self, x, y, sizex, sizey, mass, angle=0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.thrust = Vector2(0, 0)
        self.size = Vector2(sizex, sizey)
        self.mass = mass
        self.angle = angle
        self.angular_velocity = 0
        self.angular_acceleration = 0

    def apply_force(self, force):
        self.acceleration += force / self.mass

    def apply_vert_force(self, force):
        force_vec = Vector2(0, force)
        self.thrust = Vector2(0, force)
        # Rotate the force vector by the body's current angle
        force_vec.rotate_ip(self.angle)
        # Add the rotated force to the body's acceleration
        self.acceleration += force_vec / self.mass

    def apply_gravity(self):
        self.acceleration += Vector2(0, -9.81)

    def apply_torque(self, torque):
        self.angular_acceleration += torque / self.mass

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.acceleration = Vector2(0, 0)
        self.thrust = Vector2(0, 0)

        self.angular_velocity += self.angular_acceleration * dt
        self.angle += self.angular_velocity * dt
        self.angular_acceleration = 0


class Rocket(Body):
    def __init__(self, height, diameter, mass):
        super(Rocket, self).__init__(0, height/2, diameter, height, mass)


class ThrustCurve:
    def __init__(self, data):
        self.times = []
        self.forces = []
        for t, f in data:
            self.times.append(t)
            self.forces.append(f)
        self.length = len(self.times)

    def get_thrust(self, t):
        if t < 0 or self.length == 0:
            return 0

        if t <= self.times[0]:
            return self.forces[0]

        if t >= self.times[-1]:
            return self.forces[-1]

        for i in range(self.length - 1):
            if self.times[i] <= t < self.times[i+1]:
                frac = (t - self.times[i]) / (self.times[i+1] - self.times[i])
                return self.forces[i] + frac * (self.forces[i+1] - self.forces[i])

        return 0

    def get_thrust_time(self):
        return self.times[-1]

    def plot(self, step=0.01):
        t_end = self.get_thrust_time()+1
        t = 0
        thrusts = []
        while t <= t_end:
            thrusts.append(self.get_thrust(t))
            t += step
        plt.plot(np.arange(0, t_end+step, step), thrusts)
        plt.xlabel('Time (s)')
        plt.ylabel('Thrust (N)')
        plt.title('Thrust Curve')
        plt.show()
