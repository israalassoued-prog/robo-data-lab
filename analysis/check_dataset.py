import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/robot_data.csv")

print("\nDATASET OVERVIEW")
print("----------------")
print(f"Number of samples: {len(df)}")
print(f"Number of columns: {len(df.columns)}")

print("\nCOLUMNS")
print("-------")
print(df.columns.tolist())

print("\nACTION DISTRIBUTION")
print("-------------------")
print(df["action"].value_counts())

print("\nMISSING VALUES")
print("--------------")
print(df.isnull().sum())

print("\nSENSOR STATISTICS")
print("-----------------")
print(df[
    [
        "front_distance",
        "left_distance",
        "right_distance"
    ]
].describe())