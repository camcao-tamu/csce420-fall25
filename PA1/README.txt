### How to run the program
### Using 'python' or 'python3'

# Default set to advanced heuristic (H2) with iteration limit of 1000000
python blocksworld.py probA03.bwp

# Use BFS (no heuristic)
python blocksworld.py probA03.bwp -H H0

# Use simple heuristic (H1)
python blocksworld.py probB05.bwp -H H1

# Use advanced heruistic (H2)
python blocksworld.py probB05.bwp -H H2

# Use custom iteration limit
python blocksworld.py probB05.bwp -H H1 --MAX_ITERS 500000



### Known Limitations

# Longer/Harder problems may exceed the iteration limit depending on the heuristic used
# Could not solve probB19.bwp, I believe this is because this type of problem (putting most of the blocks onto one stack)
causes my advanced heuristic to overestimate the cost causing my penalty system to be faulty surpassing the length of the solution.