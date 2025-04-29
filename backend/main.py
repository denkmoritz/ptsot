from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database setup
db_file = "results.db"  # Use the correct database file

def init_db():
    """Initialize the database, dropping and recreating the 'results' table."""
    conn = sqlite3.connect(db_file)  # Use the correct database file here
    cursor = conn.cursor()

    # Drop the table if it exists
    cursor.execute("DROP TABLE IF EXISTS results;")

    # Recreate the table with the correct schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            correct_angle REAL,
            logged_angle REAL,
            error REAL,
            name TEXT  -- Ensure the 'name' column exists
        );
    """)

    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Task specifications
TASK_ITEMS = [
    ("flower", "tree", "cat", 301),
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

# Endpoint to get task data
@app.route("/get-task", methods=["GET"])
def get_task():
    task_id = int(request.args.get("task_id", 0))
    if task_id < len(TASK_ITEMS):
        task = TASK_ITEMS[task_id]
        return jsonify(
            {
                "task_id": task_id,
                "standing_at": task[0],
                "facing_to": task[1],
                "pointing_to": task[2],
            }
        )
    else:
        return jsonify({"error": "No more tasks"}), 404


# Endpoint to save task results
@app.route("/submit-task", methods=["POST"])
def submit_task():
    data = request.json
    task_id = data["task_id"]
    logged_angle = data["logged_angle"]
    name = data["name"]  # Get the user's name
    correct_angle = TASK_ITEMS[task_id][3]
    error = abs(correct_angle - logged_angle)
    error = min(error, 360 - error)  # Normalize error to <= 180

    # Save to SQLite database
    conn = sqlite3.connect("results.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO results (task_id, correct_angle, logged_angle, error, name)
        VALUES (?, ?, ?, ?, ?)
        """,
        (task_id, correct_angle, logged_angle, error, name),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task submitted"})


# Endpoint to get all results
@app.route("/get-results", methods=["GET"])
def get_results():
    conn = sqlite3.connect("results.db")
    cursor = conn.cursor()

    # Fetch all results
    cursor.execute(
        """
        SELECT name, task_id, correct_angle, logged_angle, error
        FROM results
        ORDER BY name, task_id
        """
    )
    rows = cursor.fetchall()
    conn.close()

    # Group results by name
    results_by_name = {}
    for row in rows:
        name = row[0]
        task_result = {
            "task_id": row[1],
            "correct_angle": row[2],
            "logged_angle": row[3],
            "error": row[4],
        }

        if name not in results_by_name:
            results_by_name[name] = []

        results_by_name[name].append(task_result)

    # Convert the grouped results to the desired format
    formatted_results = []
    for name, tasks in results_by_name.items():
        formatted_results.append({"name": name, "tasks": tasks})

    return jsonify(formatted_results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)