import random

import matplotlib.pyplot as plt

Kp, Ki, Kd = 3,0,2
dt = 0.01
I = 0.0
theta_target = 0.0
simulation_time = 10

theta, omega = 10.0, 0.0  # initial state, based in reality, not influenced by any noise
theta_read = theta + random.uniform(-0.5, 0.5) # theta, taking into account the imperfection of the reading device
prev_error = theta_target - theta_read

theta_results = []
signal_results = []
ang_vel_results = []

for i in range(int(simulation_time / dt)):
    error = theta_target - theta_read

    I += error * dt
    D = (error - prev_error) / dt
    u = Kp*error + Ki*I + Kd*D

    u = max(-20, min(20, u))

    # activating the actuators, changing the physically real rocket position
    omega += u * dt
    theta += omega * dt

    # save and edit the values for the next iteration
    signal_results.append(u)
    theta_results.append(theta)
    ang_vel_results.append(omega)

    theta_read = theta + random.uniform(-0.1,0.1)
    prev_error = error


time_list = [dt * (i+1) for i in range(int(simulation_time / dt))]

fig, axes = plt.subplots(3,1)

axes[0].plot(time_list, theta_results)
axes[1].plot(time_list, signal_results, linewidth = .2)
axes[2].plot(time_list, ang_vel_results, linewidth = .5)

plt.show()
