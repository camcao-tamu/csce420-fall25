from typing import List, Optional
from state import State


class Node:
    def __init__(self, state: State, parent: Optional['Node'] = None, depth: int = 0):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.path_cost = depth
        self.heuristic = 0
        self.f_score = 0
    
    def calculate_f_score(self):
        self.f_score = self.path_cost + self.heuristic
    
    def __lt__(self, other):
        if self.f_score == other.f_score:
            return self.heuristic < other.heuristic
        return self.f_score < other.f_score
    
    def get_solution_path(self) -> List['Node']:
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]
    
    def print_solution_path(self):
        path = self.get_solution_path()
        for i, node in enumerate(path):
            print(f"move {i}, pathcost={node.path_cost}, heuristic={int(node.heuristic)}, f(n)=g(n)+h(n)={int(node.f_score)}")
            node.state.print_state()
