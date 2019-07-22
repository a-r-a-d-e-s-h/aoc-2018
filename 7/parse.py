import argparse
import re

class Graph:
    def __init__(self):
        self.steps = {}

    def add(self, pre, goal):
        pre_step = self.get_step(pre)
        goal_step = self.get_step(goal)
        goal_step.add_req(pre_step)

    def get_step(self, name):
        if name not in self.steps:
            new_step = Step(name)
            self.steps[name] = new_step

        return self.steps[name]

    def can_do(self):
        steps = self.steps.values()
        return [step for step in steps if not step.completed and step.can_do]

    def do(self, step):
        step.completed = True


class Step:
    extra_time = 60
    def __init__(self, name):
        self.name = name
        self.time_required = ord(name) - ord('A') + 1 + self.extra_time
        self.time_spent = 0
        self.requires = []
        self.completed = False

    def add_req(self, req):
        if req not in self.requires:
            self.requires.append(req)

    @property
    def can_do(self):
        return all(step.completed for step in self.requires)


def do_puzzle(text, do_sanity):
    if do_sanity:
        sanity_check(text)
    graph = build_graph(text)
    return follow_instructions(graph)

def build_graph(text):
    lines = text.split('\n')
    regex = re.compile("Step ([A-Z]) must be finished before step ([A-Z]) can begin\.")
    graph = Graph()
    for line in lines:
        res = regex.match(line)
        if res:
            graph.add(*res.groups())
    return graph


def sanity_check(text):
    lines = text.split('\n')
    regex = re.compile("Step ([A-Z]) must be finished before step ([A-Z]) can begin\.")
    chars = set()
    for line in lines:
        res = regex.match(line)
        if res:
            chars = chars.union(res.groups())
    print("All chars:", ''.join(sorted(chars)))
    print("Total:", len(chars))

def do_puzzle2(text, do_sanity):
    graph = build_graph(text)
    return follow_instructions_with_workers(graph, 5)

def follow_instructions(graph):
    step_order = []
    while 1:
        can_do = graph.can_do()
        if not can_do:
            break
        next_step = sorted(can_do, key=lambda x: x.name)[0]
        step_order.append(next_step.name)
        graph.do(next_step)
    return step_order

def follow_instructions_with_workers(graph, num_workers):
    time = 0
    workers = [None]*num_workers
    steps_completed = []
    while 1:
        can_do = graph.can_do()
        if not can_do:
            break
        time += 1
        for step in sorted(can_do, key=lambda x: x.name):
            if step in workers:
                continue
            for i in range(num_workers):
                if workers[i] is None:
                    break
            else:
                i = None
            if i is None:
                break
            workers[i] = step
        for i in range(num_workers):
            step = workers[i]
            if step is None:
                continue
            step.time_spent += 1
            if step.time_spent == step.time_required:
                graph.do(step)
                workers[i] = None
                steps_completed.append(step.name)
        in_process = []
        for item in workers:
            if item is None:
                in_process.append('-')
            else:
                in_process.append(item.name)
        print("{:3d}:".format(time), ' '.join(in_process), ''.join(steps_completed))
    return time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs='?', default='input.txt')
    parser.add_argument("-s", action='store_true')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        answer = do_puzzle2(f.read(), args.s)
        print(answer)
if __name__ == "__main__":
    main()

