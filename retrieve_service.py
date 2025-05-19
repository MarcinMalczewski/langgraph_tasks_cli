from datetime import datetime

import matplotlib
from langchain_core.tools import tool
from matplotlib import pyplot as plt

from load_data import db

matplotlib.use('Agg')  # Use the non-interactive Agg backend


@tool
def get_tasks():
    """Returns all the tasks"""
    return db["tasks"]


@tool
def get_tasks_for_team(team: str):
    """Returns tasks for a given team"""
    return [task for task in db["tasks"] if task["team"] == team]


@tool
def get_tasks_for_person(person: str):
    """Returns tasks for a given person"""
    return [task for task in db["tasks"] if task["assignee"].lower() == person.lower()]


@tool
def create_graph(labels: list[str], values: list[int], xlabel: str, ylabel: str):
    """Creates a bar chart with labels on the X-axis and values on the Y-axis"""
    # Create the bar chart
    plt.figure(figsize=(8, len(values)))
    plt.bar(labels, values)
    # plt.bar(labels, values, color=['blue', 'green', 'red', 'purple', 'orange'])

    # Labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.title("Tasks Assigned to Team Members")

    # Save without displaying
    filename = f"graph_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png"
    plt.savefig(filename, dpi=300)
    # return f"Graph saved as {file_name}"
    # return "Graph created"
    return {"graph_generated": True, "file": filename}
