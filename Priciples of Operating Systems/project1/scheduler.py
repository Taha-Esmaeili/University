'''
Mohammad Taha Karbalaee Esmaeili - 40121803
'''



class Scheduler:
    def __init__(self, tasks, quantum=10):
        """
        Initialize the scheduler with tasks and quantum for Round Robin.
        :param tasks: List of tasks where each task is a dictionary with 'name', 'priority', 'burst'.
        :param quantum: Time quantum for Round Robin scheduling.
        """
        self.tasks = tasks
        self.quantum = quantum

    def fcfs(self):
        """First Come First Serve Scheduling."""
        gantt = []
        time = 0
        tasks = self.tasks[:]
        for task in tasks:
            time += task['burst']
            gantt.append((time, task['name']))
        gantt.append((time, None))
        return gantt

    def sjf(self):
        """Shortest Job First Scheduling."""
        gantt = []
        tasks = self.tasks[:]
        time = 0
        while tasks:
            # Find task with minimum burst time (manual sorting)
            shortest = tasks[0]
            for task in tasks:
                if task['burst'] < shortest['burst']:
                    shortest = task
            time += shortest['burst']
            gantt.append((time, shortest['name']))
            tasks.remove(shortest)
        gantt.append((time, None))
        return gantt

    def priority_scheduling(self):
        """Non-preemptive Priority Scheduling."""
        gantt = []
        tasks = self.tasks[:]
        time = 0
        while tasks:
            # Find task with highest priority (manual sorting)
            highest = tasks[0]
            for task in tasks:
                if task['priority'] > highest['priority']:
                    highest = task
            time += highest['burst']
            gantt.append((time, highest['name']))
            tasks.remove(highest)
        gantt.append((time, None))
        return gantt

    def round_robin(self):
        """Round Robin Scheduling."""
        gantt = []
        tasks = self.tasks[:]
        for task in tasks:
            task['remaining'] = task['burst']  # Remaining time for Round Robin
        time = 0
        while any(task['remaining'] > 0 for task in tasks):
            for task in tasks:
                if task['remaining'] > 0:
                    execute = min(self.quantum, task['remaining'])
                    time += execute
                    task['remaining'] -= execute
                    gantt.append((time, task['name']))
        gantt.append((time, None))
        return gantt

    def priority_with_rr(self):
        """Priority Scheduling with Round Robin."""
        gantt = []
        tasks = self.tasks[:]
        for task in tasks:
            task['remaining'] = task['burst']  # Remaining time for Round Robin
        # Manual priority ordering
        priorities = {task['priority'] for task in tasks}
        priorities = list(priorities)
        for i in range(len(priorities)):
            for j in range(i + 1, len(priorities)):
                if priorities[i] < priorities[j]:
                    priorities[i], priorities[j] = priorities[j], priorities[i]

        tasks = self.tasks[:].copy()
        time = 0
        for priority in priorities:
            queue = [task for task in tasks if task['priority'] == priority]
            while any(task['remaining'] > 0 for task in queue):
                for task in queue:
                    if task['remaining'] > 0:
                        execute = min(self.quantum, task['remaining'])
                        time += execute
                        task['remaining'] -= execute
                        gantt.append((time, task['name']))
        gantt.append((time, None))
        return gantt

    def schedule(self):
        """
        Runs all scheduling algorithms and returns their Gantt charts.
        :return: A dictionary with algorithm names as keys and their Gantt charts as values.
        """
        return {
            'FCFS': self.fcfs(),
            'SJF': self.sjf(),
            'Priority': self.priority_scheduling(),
            'Round Robin': self.round_robin(),
            'Priority with Round Robin': self.priority_with_rr(),
        }
