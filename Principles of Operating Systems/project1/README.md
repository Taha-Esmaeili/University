# Scheduling Algorithms Project

This project demonstrates the implementation of various CPU scheduling algorithms as part of the **Principles of Operating Systems** course, conducted at **K. N. Toosi University of Technology** by **Professor Mohammad Hossein Hamian**.

## Student Details

- **Name**: Mohammad Taha
- **Surname**: Karbalaee Esmaeili
- **Student ID**: 40121803

---

## Project Overview

The project involves implementing and simulating the following scheduling algorithms:

1. **First-Come-First-Serve (FCFS)**: Executes tasks in the order they arrive.
2. **Shortest Job First (SJF)**: Executes tasks in the order of their burst times.
3. **Priority Scheduling**: Executes tasks based on their priority values.
4. **Round-Robin (RR)**: Executes tasks in a time-sliced manner using a quantum value.
5. **Priority Scheduling with Round-Robin**: Combines priority scheduling and round-robin for tasks with equal priority.

For each scheduling algorithm, the program generates a Gantt chart as output.

---

## Files in the Project

### 1. **`scheduler.py`**

Contains the `Scheduler` class, which implements the scheduling algorithms:

- FCFS
- SJF
- Priority Scheduling
- Round-Robin
- Priority Scheduling with Round-Robin

The `Scheduler` class:

- Takes the task list and quantum value as input.
- Provides methods to execute all algorithms.
- Returns Gantt chart data for each algorithm.

### 2. **`main.py`**

Handles input/output:

- Reads the task list from a `input.txt` file.
- Calls the `Scheduler` class to perform scheduling.
- Writes Gantt charts to an `output.txt` file.

### 3. **`input.txt`**

Contains the task list, formatted as:

``` txt
TaskName, Priority, BurstTime
T1, 4, 20
T2, 2, 25
T3, 3, 25
T4, 3, 15
T5, 10, 10
```

### 4. **`output.txt`**

Generated output file containing Gantt charts for all scheduling algorithms.

---

## Usage Instructions

### Prerequisites

Ensure you have Python 3 installed on your system.

### Steps to Run

1. Place `scheduler.py`, `main.py`, and `input.txt` in the same directory.
2. Modify `input.txt` to include your desired task list.
3. Run the program:

   ```bash
   python3 main.py
   ```

4. The Gantt chart for each algorithm will be saved in `output.txt`.

---

## Example Output

For the following `input.txt`:

``` txt
T1, 4, 20
T2, 2, 25
T3, 3, 25
T4, 3, 15
T5, 10, 10
```

The `output.txt` might look like:

``` txt
--- FCFS ---
| T1 (20) | T2 (45) | T3 (70) | T4 (85) | T5 (95) |

--- SJF ---
| T5 (10) | T4 (25) | T1 (45) | T2 (70) | T3 (95) |

--- Priority ---
| T5 (10) | T1 (30) | T3 (55) | T4 (70) | T2 (95) |

--- Round Robin ---
| T1 (10) | T2 (20) | T3 (30) | T4 (40) | T5 (50) ...

--- Priority with Round Robin ---
| T5 (10) | T1 (20) | T3 (30) | T4 (40) | T2 (50) ...
```

---

## Notes

1. The implementation avoids using Python's built-in sorting functions (e.g., `sort`, `sorted`).
2. Tasks are manually sorted within algorithms to adhere to the project's constraints.
3. This project was part of the course requirements for **Principles of Operating Systems**.

---
