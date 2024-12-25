'''
Mohammad Taha Karbalaee Esmaeili - 40121803
'''


from scheduler import Scheduler

def read_tasks(input_file):
    """Reads tasks from a .txt file and returns a list of dictionaries."""
    tasks = []
    with open(input_file, 'r') as file:
        for line in file:
            task_name, priority, burst_time = line.strip().split(',')
            tasks.append({
                'name': task_name.strip(),
                'priority': int(priority.strip()),
                'burst': int(burst_time.strip())
            })
    return tasks

def make_output(scheduled_list, output_file):
    """Writes Gantt charts to a .txt file."""
    with open(output_file, 'w') as file:
        for algo, gantt in scheduled_list.items():
            file.write(f"--- {algo} ---\n")
            for start, task in gantt:
                if task is not None:
                    file.write(f"| {task} ({start}) ")
            file.write("|\n\n")


if __name__ == '__main__':

    # Provide I/O files names
    input_file = "input.txt"
    output_file = "output.txt"

    # Read tasks from file
    tasks = read_tasks(input_file)

    # Initialize Scheduler and Run
    scheduler = Scheduler(tasks, quantum=10)
    scheduled_list = scheduler.schedule()

    # Write Gantt Charts to file
    make_output(scheduled_list, output_file)
