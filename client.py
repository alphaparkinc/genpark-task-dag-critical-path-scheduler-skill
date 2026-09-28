"""Task DAG Critical Path Method (CPM) Scheduling Engine
100% Python Standard Library (collections).
"""

import collections

class TaskDAGCriticalPathScheduler:
    """DAG scheduler computing Early/Late schedules, total slack, and critical paths."""
    def __init__(self):
        self.tasks = {}

    def add_task(self, task_id, duration, predecessors=None):
        preds = predecessors or []
        self.tasks[task_id] = {
            "duration": duration,
            "predecessors": preds,
            "successors": []
        }
        for p in preds:
            if p in self.tasks:
                self.tasks[p]["successors"].append(task_id)

    def compute_critical_path(self):
        in_degree = {t: len(data["predecessors"]) for t, data in self.tasks.items()}
        queue = collections.deque([t for t, deg in in_degree.items() if deg == 0])
        topo_order = []

        while queue:
            curr = queue.popleft()
            topo_order.append(curr)
            for succ in self.tasks[curr]["successors"]:
                in_degree[succ] -= 1
                if in_degree[succ] == 0:
                    queue.append(succ)

        es = {t: 0 for t in self.tasks}
        ef = {}
        for t in topo_order:
            ef[t] = es[t] + self.tasks[t]["duration"]
            for succ in self.tasks[t]["successors"]:
                es[succ] = max(es[succ], ef[t])

        project_duration = max(ef.values()) if ef else 0

        lf = {t: project_duration for t in self.tasks}
        ls = {}
        for t in reversed(topo_order):
            for succ in self.tasks[t]["successors"]:
                lf[t] = min(lf[t], ls[succ])
            ls[t] = lf[t] - self.tasks[t]["duration"]

        slack = {t: ls[t] - es[t] for t in self.tasks}
        critical_path = [t for t in topo_order if slack[t] == 0]

        return {
            "project_duration": project_duration,
            "critical_path": critical_path,
            "schedule": {t: {"ES": es[t], "EF": ef[t], "LS": ls[t], "LF": lf[t], "slack": slack[t]} for t in self.tasks}
        }
