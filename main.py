import math
import matplotlib.pyplot as plt
import numpy as np
import copy


class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

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


class Body:
    def __init__(self, x, y, size, mass, angle=0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.size = size
        self.mass = mass
        self.angle = angle
        self.angular_velocity = 0
        self.angular_acceleration = 0

    def apply_force(self, force):
        self.acceleration += force / self.mass

    def apply_vert_force(self, force):
        force_vec = Vector2(0, force)
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

        self.angular_velocity += self.angular_acceleration * dt
        self.angle += self.angular_velocity * dt
        self.angular_acceleration = 0


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
        plt.show()


b = Body(0, 0, 10, 1)

tcE16 = ThrustCurve(((0,	    0),
                    (0.15,	1.371),
                    (0.186,	1.92),
                    (0.206,	3.387),
                    (0.242,	5.587),
                    (0.252,	7.422),
                    (0.277,	8.705),
                    (0.333,	13.474),
                    (0.359,	15.858),
                    (0.374,	16.592),
                    (0.394,	18.609),
                    (0.435,	21.544),
                    (0.476,	24.661),
                    (0.521,	26.44),
                    (0.643,	21.72),
                    (0.725,	20.432),
                    (0.821,	19.511),
                    (0.898,	18.958),
                    (1.025,	18.219),
                    (1.142,	18.032),
                    (1.259,	17.844),
                    (1.396,	17.472),
                    (1.569,	17.282),
                    (1.757,	17.275),
                    (1.895,	17.086),
                    (2.027,	17.816),
                    (2.042,	12.494),
                    (2.052,	8.457),
                    (2.063,	4.97),
                    (2.09,	0)))

# tcE16.plot()

simStep = 0.1

thrusttime = tcE16.get_thrust_time()

time = 0
running = True

b_log = []

while running:
    b.apply_vert_force(tcE16.get_thrust(time))
    b.apply_gravity()

    # if thrusttime < time:
    #     b.apply_torque(100)

    b.update(simStep)

    b_log.append(copy.deepcopy(b))

    time += simStep

    if b.position.y < 0 and not thrusttime > time:
        running = False
    elif b.position.y < 0 and thrusttime > time:
        b.position.y = 0

positions = []
altitudes = []
rotations = []
for body in b_log:
    positions.append((body.position.x, body.position.y))
    altitudes.append(body.position.y)
    rotations.append(body.angle)

# Convert the position data to a numpy array
positions = np.array(positions)
altitudes = np.array(altitudes)
rotations = np.array(rotations)

plt.plot(np.arange(len(altitudes))*simStep, altitudes)
plt.xlabel('Time')
plt.ylabel('Altitude')
plt.title('Altitude of Body Over Time')
plt.show()

# Plot the position data
plt.plot(positions[:, 0], positions[:, 1])
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Position of Body Over Time')
plt.show()

plt.plot(np.arange(len(rotations))*simStep, rotations)
plt.xlabel('Time')
plt.ylabel('Rotation')
plt.title('Rotation of Body Over Time')
plt.show()
