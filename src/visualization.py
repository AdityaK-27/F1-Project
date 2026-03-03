import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def animate_race(session, drivers=None):
    """
    Animate selected drivers on track using telemetry X/Y coordinates.
    """

    if drivers is None:
        drivers = session.drivers[:5]  # default first 5 drivers

    telemetry_data = {}

    for drv in drivers:
        laps = session.laps.pick_driver(drv)
        fastest = laps.pick_fastest()
        tel = fastest.get_telemetry()

        # Downsample for performance
        tel = tel.iloc[::10]

        telemetry_data[drv] = tel

    fig, ax = plt.subplots()
    ax.set_title("F1 Track Replay (Fastest Lap)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    lines = {}
    points = {}

    for drv in drivers:
        tel = telemetry_data[drv]
        lines[drv], = ax.plot(tel["X"], tel["Y"], alpha=0.3)
        points[drv], = ax.plot([], [], "o")

    max_frames = min(len(tel) for tel in telemetry_data.values())

    def update(frame):
        for drv in drivers:
            tel = telemetry_data[drv]
            x = tel["X"].iloc[frame]
            y = tel["Y"].iloc[frame]
            points[drv].set_data(x, y)
        return list(points.values())

    anim = FuncAnimation(fig, update, frames=max_frames, interval=30)
    plt.show()