import pandas as pd
import matplotlib.pyplot as plt
import os


# Load dataset

DATASET_PATH = "data/raw/robot_data.csv"

df = pd.read_csv(DATASET_PATH)

print(f"Loaded {len(df)} samples")


# Create results folder

os.makedirs("results", exist_ok=True)


# 1. ACTION DISTRIBUTION

action_counts = df["action"].value_counts()

plt.figure(figsize=(7, 5))

action_counts.plot(kind="bar")

plt.title("Robot Action Distribution")
plt.xlabel("Action")
plt.ylabel("Number of Samples")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "results/action_distribution.png",
    dpi=200
)

plt.show()


# 2. SENSOR DISTRIBUTIONS

plt.figure(figsize=(8, 5))

plt.hist(
    df["front_distance"],
    bins=30,
    alpha=0.6,
    label="Front"
)

plt.hist(
    df["left_distance"],
    bins=30,
    alpha=0.6,
    label="Left"
)

plt.hist(
    df["right_distance"],
    bins=30,
    alpha=0.6,
    label="Right"
)

plt.title("Distance Sensor Distributions")

plt.xlabel("Distance (m)")
plt.ylabel("Number of Samples")

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/sensor_distributions.png",
    dpi=200
)

plt.show()


# 3. ROBOT TRAJECTORIES

plt.figure(figsize=(8, 7))

for episode_id, episode in df.groupby("episode"):

    plt.plot(
        episode["x"],
        episode["y"],
        linewidth=1,
        alpha=0.7
    )

plt.title("Robot Trajectories Across Episodes")

plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")

plt.axis("equal")

plt.tight_layout()

plt.savefig(
    "results/robot_trajectories.png",
    dpi=200
)

plt.show()


# 4. FRONT SENSOR OVER TIME

episode_0 = df[
    df["episode"] == 0
]

plt.figure(figsize=(9, 5))

plt.plot(
    episode_0["step"],
    episode_0["front_distance"]
)

plt.title(
    "Front Sensor Distance — Episode 0"
)

plt.xlabel("Simulation Step")

plt.ylabel(
    "Front Distance (m)"
)

plt.tight_layout()

plt.savefig(
    "results/front_sensor_episode_0.png",
    dpi=200
)

plt.show()


# Finished

print("\nVisualization complete!")

print("\nGenerated files:")

print(
    "results/action_distribution.png"
)

print(
    "results/sensor_distributions.png"
)

print(
    "results/robot_trajectories.png"
)

print(
    "results/front_sensor_episode_0.png"
)