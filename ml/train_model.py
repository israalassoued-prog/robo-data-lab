import pandas as pd
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# 1. LOAD DATASET

DATASET_PATH = "data/raw/robot_data.csv"

df = pd.read_csv(DATASET_PATH)

print("=" * 50)
print("ROBOT ACTION CLASSIFICATION")
print("=" * 50)

print(f"\nTotal samples: {len(df)}")


# 2. SELECT INPUT FEATURES

features = [
    "front_distance",
    "left_distance",
    "right_distance"
]

X = df[features]

y = df["action"]


print("\nInput features:")
print(features)

print("\nTarget:")
print("action")


# 3. SPLIT BY EPISODE

train_episodes = list(range(14))
validation_episodes = [14, 15, 16]
test_episodes = [17, 18, 19]


train_df = df[
    df["episode"].isin(train_episodes)
]

validation_df = df[
    df["episode"].isin(validation_episodes)
]

test_df = df[
    df["episode"].isin(test_episodes)
]


X_train = train_df[features]
y_train = train_df["action"]

X_validation = validation_df[features]
y_validation = validation_df["action"]

X_test = test_df[features]
y_test = test_df["action"]


print("\nDATA SPLIT")
print("-" * 30)

print(
    f"Training samples   : {len(X_train)}"
)

print(
    f"Validation samples : {len(X_validation)}"
)

print(
    f"Test samples       : {len(X_test)}"
)


# 4. TRAIN RANDOM FOREST

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)

model.fit(
    X_train,
    y_train
)

print("Training complete!")


# 5. VALIDATION

validation_predictions = model.predict(
    X_validation
)

validation_accuracy = accuracy_score(
    y_validation,
    validation_predictions
)

print("\nVALIDATION RESULTS")
print("-" * 30)

print(
    f"Accuracy: {validation_accuracy:.4f}"
)


# 6. TEST

test_predictions = model.predict(
    X_test
)

test_accuracy = accuracy_score(
    y_test,
    test_predictions
)

print("\nTEST RESULTS")
print("-" * 30)

print(
    f"Accuracy: {test_accuracy:.4f}"
)


# 7. DETAILED REPORT

print("\nCLASSIFICATION REPORT")
print("-" * 30)

print(
    classification_report(
        y_test,
        test_predictions
    )
)


# 8. CONFUSION MATRIX

print("\nCONFUSION MATRIX")
print("-" * 30)

labels = [
    "FORWARD",
    "LEFT",
    "RIGHT"
]

cm = confusion_matrix(
    y_test,
    test_predictions,
    labels=labels
)

print(
    pd.DataFrame(
        cm,
        index=labels,
        columns=labels
    )
)


# 9. FEATURE IMPORTANCE

print("\nFEATURE IMPORTANCE")
print("-" * 30)

for feature, importance in zip(
    features,
    model.feature_importances_
):

    print(
        f"{feature:18}: "
        f"{importance:.4f}"
    )


# 10. SAVE MODEL

import joblib

os.makedirs(
    "models",
    exist_ok=True
)

model_path = (
    "models/"
    "random_forest_robot_controller.pkl"
)

joblib.dump(
    model,
    model_path
)

print("\nMODEL SAVED")
print("-" * 30)

print(model_path)

print("\nDone!")