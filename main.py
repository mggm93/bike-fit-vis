import matplotlib.pyplot as plt
import numpy as np
import math
import json

from bike import Bike
from rider import Rider

if __name__ == '__main__':
    # Read bike configuration
    with open('bike.json') as f:
        bc = json.load(f)
        print('Read bike configuration file:')
        for key, val in bc.items():
            print(key+":", val)
        print()

    # Read rider configurations
    riderNames = []
    with open('rider.json') as f:
        rcs = json.load(f)
        print('Read rider configuration file:')
        for riderName, rc in rcs.items():
            riderNames.append(riderName)
            print("Rider: %s" % riderName)
            for key, val in rc.items():
                print(key+":", val)
            print()

    # Create figure
    fig = plt.figure(figsize=(13*1.5, 5*1.5))
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(222)
    ax3 = plt.subplot(224, sharex=ax2)
    ax3.set_xlabel('Crank Angle (Deg)')
    ax2.set_ylabel('Knee Angle (Deg)')
    ax3.set_ylabel('Hip Angle (Deg)')
    ax2.grid(axis='y', ls='--')
    ax3.grid(axis='y', ls='--')
    plt.tight_layout()
    ax1.axis('equal')
    ax1.set_xlim([-950, 1200])
    ax1.set_ylim([-400, 1050])
    ax1.axis('off')
    plt.ion()

    # Create bike
    bike = Bike(bc, ax=ax1)
    bike.calcBikePositions()

    # Create riders
    riders = []
    seatColors = ['royalblue', 'lime', 'purple', 'cyan']
    riderColors = ['blueviolet', 'darkgreen', 'red', 'lime']
    for i, riderName in enumerate(riderNames):
      riders.append(Rider(rcs[riderName], bike, seatColor=seatColors[i], riderColor=riderColors[i], riderAlpha=0.5, ax=ax1))

    # Draw bike
    bike.drawBikePositions()

    # Draw Seat
    for rider in riders:
      rider.drawSeat()

    # Draw pedal and feet
    for crankAngleDeg in np.linspace(-2, 360*40, 360*20):
        # Draw cranks
        bike.calcCrankLoc(theta=-crankAngleDeg)
        bike.drawCrank()

        # Draw rider lower body
        for rider in riders:
          rider.calcAndDrawAll(crankAngleDeg)

        # Draw angle lines
        for rider in riders:
          rider.drawAngleLines(ax2, ax3)

        # Update Axes Limits
        ax2.relim()
        ax2.autoscale_view()
        ax3.relim()
        ax3.autoscale_view()

        plt.pause(0.01)

    plt.axis('equal')
    plt.show()
