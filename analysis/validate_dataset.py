import pandas as pd


DATASET_PATH = "data/raw/robot_data.csv"


# Load dataset

df = pd.read_csv(DATASET_PATH)

print("=" * 50)
print("ROBOTICS DATA QUALITY REPORT")
print("=" * 50)


# 1. Dataset size

print("\n[1] DATASET SIZE")

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")


# 2. Missing values

print("\n[2] MISSING VALUES")

missing = df.isnull().sum()

if missing.sum() == 0:

    print("PASS - No missing values")

else:

    print("WARNING - Missing values detected")

    print(
        missing[missing > 0]
    )


# 3. Duplicate rows

print("\n[3] DUPLICATE ROWS")

duplicates = df.duplicated().sum()

print(f"Duplicates: {duplicates}")

if duplicates == 0:

    print("PASS - No duplicate rows")

else:

    print("WARNING - Duplicate rows detected")


# 4. Sensor range validation

print("\n[4] SENSOR RANGE CHECK")

sensor_columns = [
    "front_distance",
    "left_distance",
    "right_distance"
]

invalid_sensor_rows = 0

for column in sensor_columns:

    invalid = (
        (df[column] < 0)
        |
        (df[column] > 5)
    )

    count = invalid.sum()

    print(
        f"{column}: {count} invalid values"
    )

    invalid_sensor_rows += count


if invalid_sensor_rows == 0:

    print("PASS - Sensor values are within range")

else:

    print("WARNING - Invalid sensor values found")


# 5. Action validation

print("\n[5] ACTION VALIDATION")

valid_actions = {
    "FORWARD",
    "LEFT",
    "RIGHT",
    "STOP"
}

invalid_actions = ~df["action"].isin(
    valid_actions
)

print(
    f"Invalid actions: {invalid_actions.sum()}"
)

if invalid_actions.sum() == 0:

    print("PASS - All actions are valid")

else:

    print("WARNING - Invalid actions detected")


# 6. Action distribution

print("\n[6] ACTION DISTRIBUTION")

action_counts = df["action"].value_counts()

for action, count in action_counts.items():

    percentage = (
        count / len(df)
    ) * 100

    print(
        f"{action:8} : "
        f"{count:5} "
        f"({percentage:.2f}%)"
    )


# 7. Sensor variability

print("\n[7] SENSOR VARIABILITY")

for column in sensor_columns:

    std = df[column].std()

    print(
        f"{column:18} "
        f"std = {std:.3f}"
    )

    if std == 0:

        print(
            "WARNING - Sensor has no variation"
        )

    else:

        print(
            "PASS - Sensor contains variation"
        )


# 8. Final result

print("\n" + "=" * 50)

if (
    missing.sum() == 0
    and duplicates == 0
    and invalid_sensor_rows == 0
    and invalid_actions.sum() == 0
):

    print("FINAL RESULT: DATASET PASSED")

else:

    print("FINAL RESULT: DATASET NEEDS REVIEW")

print("=" * 50)