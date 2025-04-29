import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fetch the data from the API
url = "https://perspective-task-backend.onrender.com/get-results"
response = requests.get(url)
data = response.json()

# Process the data into a DataFrame
records = []
for entry in data:
    name = entry["name"]
    for task in entry["tasks"]:
        task["name"] = name
        records.append(task)

df = pd.DataFrame(records)

# Calculate the average error for each task
avg_errors = df.groupby("task_id")["error"].mean().reset_index()

# Plot the average errors for each task with a gradient color palette
plt.figure(figsize=(10, 6))
sns.barplot(x="task_id", y="error", hue="task_id", data=avg_errors, dodge=False,
            palette=sns.color_palette("crest", as_cmap=True), legend=False)
plt.title("Average Error for Each Task", fontsize=16, fontweight="bold")
plt.xlabel("Task ID", fontsize=14)
plt.ylabel("Average Error", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Second Plot: Individual points and error bars for each task
plt.figure(figsize=(10, 6))

# Individual points
for task_id in df["task_id"].unique():
    task_data = df[df["task_id"] == task_id]
    x_values = [task_id] * len(task_data)
    plt.scatter(
        x=x_values,
        y=task_data["logged_angle"],
        color="black",
        alpha=0.7,
        label=None if task_id != df["task_id"].unique()[0] else "Individual Points"
    )

# Error bars for mean and std dev
task_stats = df.groupby("task_id").agg(
    mean_logged_angle=("logged_angle", "mean"),
    std_logged_angle=("logged_angle", "std")
).reset_index()

plt.errorbar(
    x=task_stats["task_id"],
    y=task_stats["mean_logged_angle"],
    yerr=task_stats["std_logged_angle"],
    fmt='o',
    color='red',
    capsize=5,
    label="Mean ± Std. Dev"
)

plt.title("Logged Angle with Individual Points and Error Bars (per Task)", fontsize=16, fontweight="bold")
plt.xlabel("Task ID", fontsize=14)
plt.ylabel("Logged Angle", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(loc="upper right", fontsize=12)
plt.show()

# Calculate overall mean and standard deviation for error deviation angles
overall_mean_error = df["error"].mean()
overall_std_error = df["error"].std()

# Print overall statistics
print(f"Overall Mean Error Deviation Angle: {overall_mean_error:.2f}")
print(f"Overall Standard Deviation of Error Deviation Angle: {overall_std_error:.2f}")