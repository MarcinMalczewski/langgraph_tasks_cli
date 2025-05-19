import random

print("preparing data...")

team_A_members = ["John", "Mark", "Lucy"]
team_B_members = ["George", "Sandy", "Jimmy", "Will"]

team_A_tasks = ["Implement a Recurring Event Feature for a Calendar App",
                "Create a Reminder Notification System Using Java and JavaFX",
                "Develop a Drag-and-Drop Interface for Rescheduling Events",
                "Build a Calendar App with Multi-Timezone Support",
                "Integrate Calendar Synchronization with Google Calendar API",
                "Implement Two-Factor Authentication (2FA)",
                "Integrate OAuth2 for Third-Party Login"]
team_B_tasks = ["Develop a Text Editor with Syntax Highlighting for Developers",
                "Implement an Auto-Save Functionality for Documents in Java",
                "Create a Collaborative Document Editor Using WebSockets",
                "Build a Version Control System for Document Changes in Java",
                "Develop a Word Count and Analytics Tool for Text Documents",
                "Set Up Session Management",
                "Implement Role-Based Access Control (RBAC)",
                "Secure Password Storage"]

due_dates = ["2025-03-15", "2025-03-31", "2025-04-15", "2025-05-10", None]

statuses = ["to do", "in progress", "done", "canceled"]

db = {"tasks": []}


def generate_tasks_for_team(team, team_tasks, team_members, statuses):
    for i, task in enumerate(team_tasks):
        db["tasks"].append({
            "id": len(db["tasks"]) + 1,
            "title": task,
            "assignee": random.choice(team_members),
            "team": team,
            "status": random.choice(statuses),
            "dueDate": random.choice(due_dates)
        })


generate_tasks_for_team("team_A", team_A_tasks, team_A_members, statuses)
generate_tasks_for_team("team_B", team_B_tasks, team_B_members, statuses)

print("data prepared")
