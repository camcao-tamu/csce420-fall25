from typing import List


class State:
    def __init__(self, stacks: List[str]):
        self.stacks = stacks[:]
        self.num_stacks = len(stacks)
    
    def __str__(self) -> str:
        return "|".join(self.stacks)
    
    def __eq__(self, other) -> bool:
        return str(self) == str(other)
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def copy(self) -> 'State':
        return State(self.stacks[:])
    
    def print_state(self):
        for stack in self.stacks:
            print(stack if stack else "")
        print(">" * 10)
    
    def get_successors(self) -> List['State']:
        successors = []
        
        for from_stack in range(self.num_stacks):
            if not self.stacks[from_stack]:
                continue
                
            for to_stack in range(self.num_stacks):
                if from_stack == to_stack:
                    continue
                
                new_state = self.copy()
                block = new_state.stacks[from_stack][-1]
                new_state.stacks[from_stack] = new_state.stacks[from_stack][:-1]
                new_state.stacks[to_stack] = new_state.stacks[to_stack] + block
                
                successors.append(new_state)
        
        return successors
