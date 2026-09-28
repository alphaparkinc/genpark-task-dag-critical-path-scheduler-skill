from client import TaskDAGCriticalPathScheduler

def main():
    cpm = TaskDAGCriticalPathScheduler()
    cpm.add_task("TaskA", 3)
    cpm.add_task("TaskB", 4, ["TaskA"])
    cpm.add_task("TaskC", 2, ["TaskA"])
    cpm.add_task("TaskD", 5, ["TaskB", "TaskC"])
    res = cpm.compute_critical_path()
    print("Task DAG Critical Path Verification:")
    print(f"Total Duration: {res['project_duration']}")
    print(f"Critical Path: {res['critical_path']}")

if __name__ == "__main__":
    main()
