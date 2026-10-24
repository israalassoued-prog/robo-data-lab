import pandas as pd
import joblib
import os

import matplotlib.pyplot as plt

from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay
)


# LOAD DATA

df = pd.read_csv(
    "data/raw/robot_data.csv"
)



# TEST EPISODES

test_episodes = [17, 18, 19]

test_df = df[
    df["episode"].isin(test_episodes)
].copy()


features = [
    "front_distance",
    "left_distance",
    "right_distance"
]


X_test = test_df[features]

y_test = test_df["action"]


# LOAD MODEL

model = joblib.load(
    "models/random_forest_robot_controller.pkl"
)


# PREDICTIONS

predictions = model.predict(
    X_test
)


# CONFUSION MATRIX

labels = [
    "FORWARD",
    "LEFT",
    "RIGHT"
]

cm = confusion_matrix(
    y_test,
    predictions,
    labels=labels
)


print("\nCONFUSION MATRIX")
print("----------------")

print(cm)


# VISUALIZATION

os.makedirs(
    "results",
    exist_ok=True
)


display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)


display.plot()

plt.title(
    "Random Forest Action Prediction"
)

plt.tight_layout()

plt.savefig(
    "results/confusion_matrix.png",
    dpi=200
)

plt.show()


print(
    "\nSaved:"
)

print(
    "results/confusion_matrix.png"
)