import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches
import math
import os

TASK_TEXT_1 = "Imagine you are standing at the"
TASK_TEXT_2 = "and facing the"
TASK_TEXT_3 = "Point to the"

TASK_ITEMS = [
    ("flower", "tree", "cat", 301),  # example
    ("car", "traffic light", "stop sign", 123),
    ("cat", "tree", "car", 237),
    ("stop sign", "cat", "house", 83),
    ("cat", "flower", "car", 156),
    ("stop sign", "tree", "traffic light", 319),
    ("stop sign", "flower", "car", 235),
    ("traffic light", "house", "flower", 333),
    ("house", "flower", "stop sign", 260),
    ("car", "stop sign", "tree", 280),
    ("traffic light", "cat", "car", 48),
    ("tree", "flower", "house", 26),
    ("cat", "house", "traffic light", 150),
]


# Function to generate plots and save them as images
def generate_plots():
    if not os.path.exists("plots"):
        os.makedirs("plots")

    for i, (located_at, facing_to, pointing_to, correct_angle) in enumerate(TASK_ITEMS):
        fig, ax = plt.subplots(figsize=(7.5, 7.5))
        ax.axis('equal')
        circle = patches.Circle((0, 0), 1.015, facecolor='none', edgecolor='black', linewidth=3)
        ax.add_patch(circle)

        # Add upright reference line
        ax.add_line(lines.Line2D((0, 0), (0, 1), linewidth=3, color='black'))
        ax.add_line(lines.Line2D((0, -0.03), (1, 0.95), linewidth=3, color='black'))  # left arrow wedge
        ax.add_line(lines.Line2D((0, 0.03), (1, 0.95), linewidth=3, color='black'))  # right arrow wedge

        # Calculate correct line position
        angle_rad = math.radians(correct_angle)
        x_end = math.sin(angle_rad)
        y_end = math.cos(angle_rad)

        # Add answer line
        ax.add_line(lines.Line2D((0, x_end), (0, y_end), linewidth=3, color='orange'))

        # Add task labels
        ax.text(0, -0.1, located_at, fontsize=10, ha='center')  # Center label
        ax.text(0, 1.1, facing_to, fontsize=10, ha='center')  # Top label
        ax.text(x_end * 1.15, y_end * 1.15, pointing_to, fontsize=10, ha='center')  # Pointing-to label

        # Add task instructions
        task_number = f"Task {i}" if i == 0 else f"Task {i}"
        instruction_text = f"{task_number}. {TASK_TEXT_1} {located_at}, {TASK_TEXT_2} {facing_to}. {TASK_TEXT_3} {pointing_to}."
        ax.text(0.0, -1.5, instruction_text, fontsize=9, ha='center')

        plt.xlim(-1.5, 1.5)
        plt.ylim(-1.5, 1.5)
        plt.xticks([])
        plt.yticks([])

        # Save plot as an image
        plot_filename = f"plots/plot_{i}.png" if i == 0 else f"plots/plot_{i}.png"
        plt.savefig(plot_filename)
        plt.close(fig)

    print("Plots have been generated and saved in the 'plots' directory.")


# Run the function
generate_plots()