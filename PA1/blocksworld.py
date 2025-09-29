import sys
import argparse
from typing import Tuple
from solver import BlocksworldSolver
from state import State


def parse_problem_file(filename: str) -> Tuple[State, State]:
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    header = lines[0].split()
    num_stacks = int(header[0])
    num_blocks = int(header[1])
    
    separator_indices = []
    for i, line in enumerate(lines):
        if line.startswith('>'):
            separator_indices.append(i)
    
    initial_stacks = []
    for i in range(separator_indices[0] + 1, separator_indices[1]):
        initial_stacks.append(lines[i])
    
    goal_stacks = []
    for i in range(separator_indices[1] + 1, separator_indices[2]):
        goal_stacks.append(lines[i])
    
    return State(initial_stacks), State(goal_stacks)


def main():
    parser = argparse.ArgumentParser(description='Blocksworld A* Solver')
    parser.add_argument('filename', help='Problem file (.bwp)')
    parser.add_argument('-H', '--heuristic', default='H2', 
                       choices=['H0', 'H1', 'H2'], 
                       help='Heuristic function to use')
    parser.add_argument('--MAX_ITERS', type=int, default=1000000,
                       help='Maximum number of iterations')
    
    args = parser.parse_args()
    
    try:
        initial_state, goal_state = parse_problem_file(args.filename)
        solver = BlocksworldSolver(initial_state, goal_state, args.heuristic, args.MAX_ITERS)
        solution_node = solver.solve()
        
        if solution_node:
            solution_node.print_solution_path()
            
            method = "BFS" if args.heuristic == "H0" else "Astar"
            print(f"statistics: {args.filename} method {method} planlen {solution_node.path_cost} "
                  f"iters {solver.iterations} maxq {solver.max_queue_size}")
        else:
            method = "BFS" if args.heuristic == "H0" else "Astar"
            print(f"statistics: {args.filename} method {method} planlen FAILED "
                  f"iters {solver.iterations} maxq {solver.max_queue_size}")
    
    except FileNotFoundError:
        print(f"Error: Could not find file {args.filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()