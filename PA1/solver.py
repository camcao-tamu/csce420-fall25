import heapq
from typing import Optional
from state import State
from node import Node


class BlocksworldSolver:
    def __init__(self, initial: State, goal: State, heuristic_type: str = "H2", max_iterations: int = 1000000):
        self.initial = initial
        self.goal = goal
        self.heuristic_type = heuristic_type
        self.max_iterations = max_iterations
        self.iterations = 0
        self.max_queue_size = 0
    
    def calculate_heuristic(self, state: State) -> float:
        if self.heuristic_type == "H0":
            return 0
        elif self.heuristic_type == "H1":
            return self.h1_blocks_out_of_place(state)
        elif self.heuristic_type == "H2":
            return self.h2_advanced_heuristic(state)
        else:
            return 0
    
    def h1_blocks_out_of_place(self, state: State) -> int:
        out_of_place = 0
        
        for i in range(state.num_stacks):
            current_stack = state.stacks[i]
            goal_stack = self.goal.stacks[i]
            
            max_len = max(len(current_stack), len(goal_stack))
            for j in range(max_len):
                current_block = current_stack[j] if j < len(current_stack) else None
                goal_block = goal_stack[j] if j < len(goal_stack) else None
                
                if current_block != goal_block:
                    if current_block:
                        out_of_place += 1
        
        return out_of_place
    
    def h2_advanced_heuristic(self, state: State) -> int:
        penalty = 0
        
        current_positions = {}
        goal_positions = {}
        
        for stack_idx, stack in enumerate(state.stacks):
            for pos, block in enumerate(stack):
                current_positions[block] = (stack_idx, pos)
        
        for stack_idx, stack in enumerate(self.goal.stacks):
            for pos, block in enumerate(stack):
                goal_positions[block] = (stack_idx, pos)
        
        for block in current_positions:
            current_stack, current_pos = current_positions[block]
            goal_stack, goal_pos = goal_positions[block]
            
            if current_stack != goal_stack:
                penalty += 2
            elif current_pos != goal_pos:
                penalty += 1
            elif current_pos == goal_pos and current_stack == goal_stack:
                current_stack_blocks = state.stacks[current_stack]
                goal_stack_blocks = self.goal.stacks[goal_stack]
                
                for above_pos in range(current_pos + 1, len(current_stack_blocks)):
                    if (above_pos >= len(goal_stack_blocks) or 
                        current_stack_blocks[above_pos] != goal_stack_blocks[above_pos]):
                        penalty += 1
        
        return penalty
    
    def solve(self) -> Optional[Node]:
        frontier = []
        visited = set()
        
        initial_node = Node(self.initial)
        initial_node.heuristic = self.calculate_heuristic(self.initial)
        initial_node.calculate_f_score()
        
        heapq.heappush(frontier, initial_node)
        
        self.iterations = 0
        self.max_queue_size = 0
        
        while frontier and self.iterations < self.max_iterations:
            self.iterations += 1
            
            if len(frontier) > self.max_queue_size:
                self.max_queue_size = len(frontier)
            
            current_node = heapq.heappop(frontier)
            
            if str(current_node.state) in visited:
                continue
            
            visited.add(str(current_node.state))
            
            if self.iterations % 1000 == 0 or self.iterations <= 20:
                print(f"iter={self.iterations}, depth={current_node.depth}, pathcost={current_node.path_cost}, "
                      f"heuristic={int(current_node.heuristic)}, score={int(current_node.f_score)}, "
                      f"Qsize={len(frontier)}")
            
            if current_node.state == self.goal:
                print(f"success! iter={self.iterations}, cost={current_node.path_cost}, "
                      f"depth={current_node.depth}, max queue size={self.max_queue_size}")
                return current_node
            
            successors = current_node.state.get_successors()
            
            for successor_state in successors:
                if str(successor_state) in visited:
                    continue
                
                successor_node = Node(successor_state, current_node, current_node.depth + 1)
                successor_node.heuristic = self.calculate_heuristic(successor_state)
                successor_node.calculate_f_score()
                
                heapq.heappush(frontier, successor_node)
        
        print(f"Failed to find solution within {self.max_iterations} iterations")
        return None
