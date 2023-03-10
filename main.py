from physics import *
import matplotlib.pyplot as plt
import numpy as np
import copy
import visulizer

b = Body(0, 0, 2, 10, 0.5)

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

simStep = 0.01

thrusttime = tcE16.get_thrust_time()

time = 0
running = True

b_log = []

loadnum = 0

print("Running Simulation.", end="")

while running:
    b.apply_vert_force(tcE16.get_thrust(time))
    b.apply_gravity()

    if thrusttime > time:
        b.apply_torque(-1)

    b_log.append(copy.deepcopy(b))

    b.update(simStep)

    time += simStep

    if b.position.y < 0 and not thrusttime > time:
        running = False
    elif b.position.y < 0 and thrusttime > time:
        b.position.y = 0

    if time >= loadnum:
        print(".", end="")
        loadnum += 1

print(" Done!")

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

# plt.plot(np.arange(len(altitudes))*simStep, altitudes)
# plt.xlabel('Time')
# plt.ylabel('Altitude')
# plt.title('Altitude of Body Over Time')
# plt.show()

# # Plot the position data
# plt.plot(positions[:, 0], positions[:, 1])
# plt.xlabel('X Position')
# plt.ylabel('Y Position')
# plt.title('Position of Body Over Time')
# plt.show()

# plt.plot(np.arange(len(rotations))*simStep, rotations)
# plt.xlabel('Time')
# plt.ylabel('Rotation')
# plt.title('Rotation of Body Over Time')
# plt.show()

csv = ["Time,X_pos,Y_pos,X_vel,Y_vel,X_acl,Y_acl,Angle,Ang_vel,Ang_acl"]

i = 0
for body in b_log:
    line = ""

    line += str(i*simStep) + ","

    line += str(body.position.x) + ","
    line += str(body.position.y) + ","

    line += str(body.velocity.x) + ","
    line += str(body.velocity.y) + ","

    line += str(body.acceleration.x) + ","
    line += str(body.acceleration.y) + ","

    line += str(body.angle) + ","

    line += str(body.angular_velocity) + ","

    line += str(body.angular_acceleration)

    csv.append(line)
    i += 1

with open("sim.csv", "w") as file1:
    file1.write("\n".join(csv))

visulizer.run(b_log, simStep)
