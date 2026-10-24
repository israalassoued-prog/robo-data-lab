# RoboDataLab 

A simulation-based robotics data collection and AI control project built with Python, PyBullet, and Scikit-learn.

The project explores how robot sensor data can be collected, analyzed, and used to train a machine learning model for reactive navigation.

---

## Overview

RoboDataLab simulates a mobile robot equipped with distance sensors operating in an obstacle-filled environment.

The robot continuously collects:

- Front distance
- Left distance
- Right distance
- Position
- Velocity
- Selected navigation action

The collected data is then validated, visualized, and used to train a Random Forest classifier that predicts the robot's next action.

The trained model is finally deployed in a real-time simulation loop.

```text
Robot Simulation
       ↓
Sensor Data Collection
       ↓
Data Validation & Visualization
       ↓
Machine Learning
       ↓
Model Evaluation
       ↓
Real-Time AI Controller
       ↓
Controller Benchmark


Objectives

The main objectives of RoboDataLab are:

Simulate a mobile robot without physical hardware
Implement simulated distance sensors
Collect structured robotics data
Create a dataset containing sensor observations and robot actions
Analyze and validate the collected data
Train a machine learning model for reactive navigation
Evaluate the model on unseen test data
Deploy the trained model in a real-time simulation
Compare machine learning and rule-based control strategies
Investigate the limitations of learned robotic behaviors
Technologies
Python
PyBullet
NumPy
Pandas
Scikit-learn
Matplotlib
Joblib
Project Structure
RoboDataLab/
|
├── simulation/
│   ├── robot.py
│   ├── controller.py
│   ├── data_collector.py
│   ├── environment.py
│   ├── main.py
│   └── ai_controller.py
|
├── analysis/
│   ├── check_dataset.py
│   ├── visualize_data.py
│   ├── evaluate_model.py
│   └── benchmark.py
|
├── ml/
│   └── train_model.py
|
├── data/
│   └── raw/
│       └── robot_data.csv
|
├── models/
│   └── random_forest_robot_controller.pkl
|
├── results/
│   ├── confusion_matrix.png
│   └── controller_benchmark.csv
|
├── requirements.txt
├── .gitignore
└── README.md
1. Simulation

The robot is simulated using PyBullet.

The simulated mobile robot is represented as a box-shaped rigid body with configurable dimensions and movement capabilities.

It can:

Move forward
Turn left
Turn right
Stop
Measure distances to nearby obstacles
Retrieve its position
Retrieve its velocity

The simulation includes an environment containing randomly positioned obstacles.

This allows different obstacle configurations to be tested without requiring physical robotics hardware.

2. Simulated Sensors

The robot uses three ray-based distance sensors.

                 Front
                   |
                   |
            Left   |   Right
                  Robot

Each sensor uses a PyBullet ray test to measure the distance between the robot and an obstacle.

The maximum sensing distance is:

5 meters

The sensors produce the following measurements:

front_distance
left_distance
right_distance

These measurements are used both for data collection and machine learning inference.

3. Data Collection

A dedicated data collection system records the robot's observations and actions during simulation.

The robot operates over multiple episodes while interacting with randomly generated obstacle configurations.

Each recorded sample contains information about:

Simulation episode
Simulation step
Robot position
Sensor measurements
Robot velocity
Selected action

The final dataset contains:

10,000 samples
12 columns
20 episodes

The dataset columns are:

episode
step
x
y
z
front_distance
left_distance
right_distance
velocity_x
velocity_y
velocity_z
action
4. Dataset Analysis

Before training the machine learning model, the dataset is analyzed to verify its quality.

The analysis includes:

Dataset size
Column structure
Missing-value detection
Action distribution
Sensor statistics
Minimum and maximum sensor values
Mean and standard deviation of sensor measurements

The dataset contains no missing values.

Action Distribution

The collected dataset contains:

FORWARD    8622
LEFT        739
RIGHT       639

This shows that the dataset is imbalanced toward the FORWARD action.

This imbalance is an important consideration when evaluating the machine learning model because classification accuracy alone may not fully represent navigation performance.

5. Data Visualization

The collected data is visualized to better understand the relationship between sensor observations and robot behavior.

The visualization stage is used to inspect:

Sensor distributions
Robot movement
Sensor measurements
Action distribution
Relationships between obstacle proximity and navigation decisions

The visualizations provide a way to identify patterns and potential issues in the collected dataset before model training.

6. Machine Learning

A Random Forest classifier is used to learn the relationship between distance sensor measurements and navigation actions.

The model receives three input features:

front_distance
left_distance
right_distance

The target variable is:

action

The model therefore learns the following mapping:

Front Distance
Left Distance
Right Distance
        |
        v
Random Forest Classifier
        |
        v
FORWARD / LEFT / RIGHT
7. Dataset Split

The dataset is divided into training, validation, and test sets.

Training samples   : 7,000
Validation samples : 1,500
Test samples       : 1,500

The test set is kept separate from training so that the final model evaluation measures its performance on previously unseen samples.

8. Model Performance

The Random Forest classifier achieved:

Validation Accuracy: 100.0%

Test Accuracy: 85.47%

The difference between validation and test performance indicates that the model does not generalize perfectly to unseen samples.

The test classification results were:

              precision    recall    f1-score

FORWARD          1.00       1.00       1.00
LEFT             1.00       0.56       0.72
RIGHT            0.55       1.00       0.71

Overall test accuracy:

85.47%

The confusion matrix is saved in:

results/confusion_matrix.png
9. Feature Importance

The Random Forest model provides feature importance values showing how strongly each sensor contributed to its predictions.

The measured importance values were approximately:

front_distance    0.5765
right_distance    0.3844
left_distance     0.0391

The front distance sensor had the highest importance.

This is consistent with the navigation problem because detecting an obstacle directly ahead is particularly important when deciding whether the robot should continue forward or change direction.

10. Real-Time AI Controller

After training, the Random Forest model is loaded into a real-time PyBullet simulation.

At every simulation step, the system:

1. Reads the robot's sensors
2. Extracts the three distance measurements
3. Sends them to the Random Forest model
4. Receives an action prediction
5. Executes the predicted action
6. Advances the simulation
7. Repeats

The trained model is stored at:

models/random_forest_robot_controller.pkl

The AI controller therefore performs inference directly from simulated sensor data rather than using pre-recorded actions.

11. Rule-Based Controller

For comparison, the project also implements a traditional rule-based controller.

The rule-based controller follows a simple decision strategy:

If front distance < threshold:

    If left distance > right distance:
        Turn LEFT

    Otherwise:
        Turn RIGHT

Otherwise:
    Move FORWARD

This provides a baseline against which the machine learning controller can be evaluated.

12. Controller Benchmark

A benchmark was implemented to compare the rule-based controller and the Random Forest controller.

Each controller is evaluated over:

20 episodes

The benchmark records:

Success rate
Collision rate
Number of simulation steps
Number of turns
Minimum distance from obstacles

The benchmark allows the controllers to be evaluated at the navigation level rather than only at the individual classification level.

13. Benchmark Results

The current benchmark produced the following results:

Controller	Success Rate	Collision Rate	Average Turns	Average Minimum Distance
Rule-Based	0%	0%	143.0	0.60 m
Random Forest AI	0%	100%	84.0	0.36 m

The results demonstrate an important distinction between machine learning classification performance and autonomous navigation performance.

Although the Random Forest achieved 85.47% test accuracy, this did not directly translate into successful navigation in the benchmark environment.

The rule-based controller avoided collisions but failed to reach the goal within the maximum number of simulation steps.

The Random Forest controller made fewer turns but eventually collided with an obstacle.

14. Generalization

One of the main observations from the project is that good classification performance does not necessarily guarantee good robotic behavior.

The model was trained to predict actions from sensor measurements collected during simulation.

However, autonomous navigation involves sequential decisions.

A small prediction error can change the robot's trajectory, which changes its future sensor measurements, which can lead to additional errors.

This creates a difference between:

Sensor-to-action classification

and:

Long-term autonomous navigation

The benchmark therefore provides a useful demonstration of a common challenge in robotics machine learning:

Training performance
        !=
Real-world or environment-level performance
15. Limitations

The current project is a proof-of-concept and has several limitations.

Dataset imbalance

Most collected actions are FORWARD, while LEFT and RIGHT occur less frequently.

Limited sensor configuration

The robot currently uses only three distance measurements.

Simple action space

The robot has only three possible actions:

FORWARD
LEFT
RIGHT
Limited environment diversity

The model is trained using simulated environments and may not generalize well to significantly different obstacle configurations.

Classification versus navigation

The machine learning model predicts individual actions but does not explicitly optimize long-term navigation success.

Simplified robot dynamics

The simulated robot is considerably simpler than a real mobile robot and does not model all physical effects encountered in real-world robotics.

16. Future Improvements

Several improvements could make the system more robust.

Dataset Improvements
Collect more episodes
Generate more diverse environments
Balance navigation actions
Introduce more obstacle configurations
Include more challenging navigation scenarios
Sensor Improvements
Add additional ray sensors
Increase sensor coverage
Add rear sensors
Include sensor history
Add simulated camera data
Add IMU measurements
Machine Learning Improvements
Compare Random Forest with other classifiers
Test Gradient Boosting
Test neural networks
Use temporal sensor sequences
Investigate imitation learning
Investigate reinforcement learning
Navigation Improvements
Use trajectory-level evaluation
Introduce explicit goal navigation
Add collision avoidance logic
Combine learned policies with safety constraints
Evaluate performance across unseen environments
17. Installation

Clone the repository:

git clone <repository-url>

Enter the project directory:

cd RoboDataLab

Create a virtual environment:

python -m venv .venv

Activate the virtual environment on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install the required dependencies:

pip install -r requirements.txt
18. Running the Project
Collect Data

Run:

python simulation/data_collector.py

The collected dataset will be saved in:

data/raw/
Check the Dataset

Run:

python analysis/check_dataset.py

This displays:

Dataset size
Columns
Action distribution
Missing values
Sensor statistics
Visualize the Dataset

Run:

python analysis/visualize_data.py

This generates visualizations for exploring the collected robotics data.

Train the Model

Run:

python ml/train_model.py

The trained Random Forest model is saved to:

models/random_forest_robot_controller.pkl
Evaluate the Model

Run:

python analysis/evaluate_model.py

The confusion matrix is saved to:

results/confusion_matrix.png
Run the AI Controller

Run:

python simulation/ai_controller.py

This launches the PyBullet simulation and uses the trained Random Forest model to control the robot in real time.

Run the Benchmark

Run:

python analysis/benchmark.py

The benchmark compares the rule-based and AI controllers.

The final comparison is saved to:

results/controller_benchmark.csv
19. Reproducibility

Random seeds are used in the benchmark to make the obstacle generation reproducible between controller evaluations.

The benchmark uses the same random seed for the rule-based and AI controllers so that both controllers are evaluated under equivalent environment generation conditions.

20. Key Takeaways

RoboDataLab demonstrates a complete robotics data pipeline:

Simulation
    |
    v
Sensor Data Collection
    |
    v
Dataset Validation
    |
    v
Data Visualization
    |
    v
Machine Learning
    |
    v
Model Evaluation
    |
    v
Real-Time Inference
    |
    v
Robot Control
    |
    v
Controller Benchmarking

The project demonstrates how simulated robotics data can be transformed into a machine learning model and deployed in a closed-loop robotic simulation.

It also demonstrates an important practical lesson: strong machine learning classification metrics do not automatically translate into robust autonomous behavior.

Future work will focus on improving dataset diversity, temporal modeling, navigation robustness, and generalization to unseen environments.

Author
Issra Lassoued

Engineering student in Industrial Computing and Automation.