import random

import matplotlib.pyplot as plt

dt = 0.01 # one leap, remains constant throughout simulations
random.seed(0)

def PID_loop(error, prev_error, I, kp, ki, kd):

    I += error * dt
    D = (error - prev_error) / dt
    u = kp*error + ki*I + kd*D

    u = max(-20, min(20, u)) # limiting the signal strength

    return u, I

def simulate(noise, kp, ki, kd, comment):
    I = 0.0
    #simulation default settings, could be changed using function parameters if the task required me to do so
    theta_target = 0.0
    simulation_time = 10

    theta, omega = 10.0, 0.0  # initial state, based in reality, not influenced by any noise
    prev_error = - theta # I assume that immediately before the simulation error was equal to the negative base theta (in this case without any noise)

    theta_results = []
    signal_results = []
    ang_vel_results = []

    # the simulation itself
    for i in range(int(simulation_time / dt)):
        theta_read = theta + random.uniform(-noise, noise) # theta, taking into account the imperfection of the reading device

        error = theta_target - theta_read

        signal, I = PID_loop(error, prev_error, I, kp, ki, kd)

        prev_error = error

        # activating the actuators, changing the physically real rocket position
        omega += signal * dt
        theta += omega * dt

        signal_results.append(signal)
        theta_results.append(theta)
        ang_vel_results.append(omega)

    # Plotting

    time_list = [dt * (i+1) for i in range(int(simulation_time / dt))]

    figure, axes = plt.subplots(3,1, figsize=(16, 14), dpi = 60)
    figure.suptitle(f"kp={kp}, ki={ki}, kd={kd}, noise={noise} | {comment}")

    axes[0].plot(time_list, theta_results)
    axes[0].set_title('Angle (theta) results', fontsize = 12)
    axes[0].set_ylabel("Theta [°]")

    axes[1].plot(time_list, signal_results, linewidth = .2)
    axes[1].set_title('Signal strength results', fontsize = 12)
    axes[1].set_ylabel("U")

    axes[2].plot(time_list, ang_vel_results, linewidth = .5)
    axes[2].set_title('Angular velocity results', fontsize = 12)
    axes[2].set_ylabel("Angular velocity [°/second]")

    for i in range(3):
        axes[i].set_xlabel("Time[seconds]", fontsize = 8)

    plt.show()

simulate(0, 3, 0, 2, "01 baseline: tuned values, no noise")

simulate(0, 1, 0, 2, "02 Kp comparison: low Kp")
simulate(0, 3, 0, 2, "02 Kp comparison: medium Kp")
simulate(0.1, 3, 0, 2, "02 Kp comparison: medium Kp, low noise")
simulate(0, 8, 0, 2, "02 Kp comparison: high Kp")

simulate(0, 3, 0,   2, "03 Ki comparison: no integral")
simulate(0, 3, 0.5, 2, "03 Ki comparison: low Ki")
simulate(0.1, 3, 0.5, 2, "03 Ki comparison: low Ki, low noise")
simulate(0, 3, 2,   2, "03 Ki comparison: high Ki")

simulate(0, 3, 0, 0, "04 Kd comparison: no derivative")
simulate(0, 3, 0, 1, "04 Kd comparison: low Kd")
simulate(0, 3, 0, 2, "04 Kd comparison: medium Kd")
simulate(0.1, 3, 0, 2, "04 Kd comparison: medium Kd, low noise")
simulate(0, 3, 0, 4, "04 Kd comparison: high Kd")

simulate(0,   3, 0, 2, "05 noise: none")
simulate(0.1, 3, 0, 2, "05 noise: low")
simulate(0.4, 3, 0, 2, "05 noise: high")
