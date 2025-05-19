# langgraph_tasks_cli

## Description

`langgraph_tasks_cli` is a Command Line Interface (CLI) application demonstrating how LLMs can be used to manage and analyze tasks within a team. The application allows users to ask questions about tasks and receive natural language responses.

The key element is the LangChain library, which provides a framework (LangGraph) for building applications that utilize language models.

Since it's just an example, it uses a simple in-memory data structure to represent tasks and teams. The application can be extended to connect to a real database or API for task management.

## Features

- **Task Management**:
  - Retrieve all tasks.
  - Filter tasks by team or individual.
  - Analyze task statuses and deadlines.

- **Language Model Integration**:
  - Generate responses to user queries about tasks.
  - Handle natural language queries.

- **Graph Generation**:
  - Create bar charts to visualize data, such as the number of tasks assigned to team members.

## Project Structure

- **`llm.py`**: Handles the logic for the language model and builds the state graph for processing queries.
- **`load_data.py`**: Generates sample data for team tasks.
- **`main.py`**: The main CLI application that allows user interaction with the system.
- **`retrieve_service.py`**: Provides tools for retrieving task data and generating graphs.

## Requirements

- Python 3.8+
- Libraries:
  - `langchain_core`
  - `matplotlib`
  - `langgraph`

## How to Run

1. Set up the environment:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the root directory with the following content:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```
   Replace `your_openai_api_key` with your actual OpenAI API key.
3. Start the application:
   ```bash
   python main.py
   ```
4. Enter queries in the terminal, such as:
   - "What is team_B working on?"
   - "Are there any overdue tasks?"
   - "Draw a chart showing the number of tasks for each person."

## Example Queries

- "What tasks is team_A working on? Specify which person is responsible for each task"
- "Who has the most tasks?"
- "Which team is working on the calendar?"
- "Generate a chart showing task distribution among team members."
- "Today is March 17th. Are there any tasks that are overdue? Take task statuses into account. Tasks in status 'done' shouldn't be considered as overdue"


