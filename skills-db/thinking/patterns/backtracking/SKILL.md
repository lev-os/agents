---
name: Backtracking
description: Systematic trial-and-error search technique that builds solutions incrementally, abandoning candidates as soon as they cannot lead to a valid solution
---

# Backtracking Algorithm Paradigm

## What It Is
A systematic trial-and-error search technique that builds solutions incrementally, abandoning (backtracking from) candidates as soon as it determines they cannot lead to a valid solution. Think of it as exploring a decision tree depth-first, pruning branches that violate constraints. The key insight: undo bad choices and try alternatives rather than exploring every possibility blindly.

## When to Use It
- Need to find **all valid solutions** (not just one optimal solution)
- Problem involves **constraint satisfaction** (e.g., placing queens, solving Sudoku)
- Solution is a **sequence of choices** with validity constraints
- Choices have dependencies (can't be made independently like greedy)
- Exhaustive search is required but can be pruned intelligently
- Problem space is tree-like (make choice, recurse, undo choice)

**Key Signal**: If you're thinking "try this, if it doesn't work, undo it and try that" → backtracking.

## Execution Steps

### 1. Choose (Make a Decision)
Select one option from available choices at current decision point. This extends the partial solution by one step. Start with first option if exploring all solutions.

**Action**: Pick a candidate (e.g., place queen in column i, assign digit d to cell, include element in subset). Add this choice to current partial solution.

### 2. Check Validity
Verify if the current partial solution satisfies all constraints. This is the pruning step - reject invalid paths early before exploring deeper.

**Action**: Run constraint checks (e.g., no two queens attack each other, Sudoku row/column/box rules, subset sum not exceeded). If invalid, skip to step 4 (backtrack).

### 3. Explore (Recurse)
If valid, move forward with this choice and recursively solve the remaining subproblem. If this is a complete solution, record it and potentially return (depending on whether you need one or all solutions).

**Action**: Recursively call backtracking function with updated state. If complete solution found and only need one, return success. If need all solutions, store it and continue.

### 4. Backtrack (Undo)
Remove the last choice from the partial solution (undo the decision). Try the next alternative at this decision level.

**Action**: Restore state to before step 1 (e.g., remove queen, clear cell, exclude element). Move to next candidate. If no more candidates, return to previous decision level.

### 5. Repeat
Continue until all possibilities at current level are exhausted, then backtrack to previous level. Process completes when all branches explored or solution found (if only need one).

**Action**: Loop through all candidates at each decision point. Recursion handles moving between levels. Base case: solution complete (return it) or no valid choices (return failure).

## Real-World Applications

**Constraint Satisfaction Problems**
- Sudoku solver: fill grid satisfying row/column/box constraints
- N-Queens: place N queens on N×N board with no attacks
- Graph coloring: assign colors to nodes so no adjacent nodes share color
- Crossword puzzle generation: place words satisfying constraints

**Combinatorial Search**
- Permutation generation: find all orderings of elements
- Subset sum: find all subsets summing to target
- Combination generation: select k items from n (C(n,k))
- Partition problem: split set into two equal-sum subsets

**Game Solving**
- Maze solving: find path from start to goal
- Tic-tac-toe/chess move generation: explore game tree
- Puzzle solving (8-puzzle, Rubik's cube): search state space

**Path Finding**
- Hamiltonian path: visit each vertex exactly once
- Traveling salesman (small instances): find optimal tour
- Knight's tour: chess knight visits each square once

**Resource Allocation**
- Job assignment: assign workers to tasks with constraints
- Exam scheduling: schedule exams avoiding conflicts
- Timetable generation: assign classes to rooms/times

**Natural Language Processing**
- Syntax tree parsing: find valid parse trees for sentences
- Word break problem: segment sentence into valid words
- Regular expression matching (with backtracking)

## Anti-Patterns

**Not pruning invalid paths early** → Explores exponentially many invalid branches; check constraints ASAP after each choice.

**Using backtracking for optimization without pruning** → Extremely slow; add bounds/heuristics or use branch-and-bound instead.

**Forgetting to restore state** → Leads to incorrect solutions; always undo changes when backtracking.

**Exploring same state multiple times** → Wastes time; consider memoization or marking visited states.

**Using when greedy/DP suffices** → Backtracking is exponential; if problem has greedy property or overlapping subproblems, use faster methods.

**Poor choice ordering** → Exploring likely-to-fail branches first; use heuristics (e.g., most constrained variable first).

## Success Metrics
- Correctness: finds all valid solutions (for enumeration) or any valid solution (for search)
- Pruning effectiveness: ratio of explored nodes to total nodes (lower is better)
- Time performance: acceptable runtime on target problem sizes
- Space efficiency: recursion depth manageable (< 1000 levels typically)
- Code clarity: recursive structure clearly matches problem structure

## Related Frameworks
- **Depth-First Search (DFS)**: Backtracking is DFS with constraint checking and pruning
- **Branch and Bound**: Backtracking + bounding functions for optimization
- **Dynamic Programming**: When subproblems overlap, replace backtracking with DP
- **Constraint Programming**: Declarative approach with propagation and backtracking
- **A* Search**: Informed search with heuristics for optimal paths

## Common Pitfalls
- Not implementing proper base case (infinite recursion)
- Modifying global state without restoration (bugs in multi-branch exploration)
- Confusing "find one solution" vs. "find all solutions" (early return logic)
- Deep recursion causing stack overflow (convert to iterative with explicit stack)
- Not handling empty input or boundary cases (0 elements, 1 element)
- Inefficient constraint checking (recompute entire state instead of incremental)

## Tools & Resources
- **Visualization**: Algorithm Visualizer (algorithm-visualizer.org), Recursion Tree Visualizer
- **Practice Platforms**: LeetCode backtracking tag (~100 problems), HackerRank recursion section
- **Books**: "Algorithms" (Sedgewick & Wayne), "Programming Pearls" (Bentley)
- **Debugging**: Add trace prints showing decision depth and choices, visualize recursion tree
- **Profiling**: Count number of recursive calls, measure pruning effectiveness

## Classic Backtracking Problems

**N-Queens**: Place N queens on N×N board, no two queens attack each other.
- State: queen positions by row
- Constraint: no two queens share row/column/diagonal
- Time: O(N!) without pruning, much better with constraint checking

**Sudoku**: Fill 9×9 grid with digits 1-9 satisfying row/column/box constraints.
- State: partially filled grid
- Constraint: each digit appears once per row/column/3×3 box
- Time: Exponential in unfilled cells, but heavy pruning makes it practical

**Subset Sum**: Find all subsets of array summing to target T.
- State: current subset and remaining elements
- Constraint: current sum ≤ target
- Time: O(2^n) worst case, pruning helps significantly

**Permutations**: Generate all orderings of n elements.
- State: current permutation prefix
- Constraint: each element used once
- Time: O(n!) - must explore all leaves

**Graph Coloring**: Assign colors to vertices so no adjacent vertices share color.
- State: color assignments for vertices
- Constraint: adjacent vertices have different colors
- Time: O(m^n) where m = colors, n = vertices

## Optimization Techniques

**Choice Ordering (Heuristics)**: Try most promising branches first (fail-fast or succeed-fast).

**Constraint Propagation**: When making a choice, deduce implications and prune early.

**Memoization**: Cache results for states that recur (hybrid backtracking-DP).

**Iterative Deepening**: Limit recursion depth, gradually increase (avoid stack overflow).

**Symmetry Breaking**: Avoid exploring equivalent states (e.g., in N-Queens, only check half of first row).

**Forward Checking**: Before making choice, verify remaining choices still have valid options.

---
*Framework Type*: Algorithm Design Paradigm
*Domain*: Computer Science, Constraint Satisfaction
*Practitioner Score*: 8/10 - Essential for constraint problems, widely used in game AI, solvers
*Complexity*: Medium - Recursive thinking required, state management can be tricky
*Prerequisites*: Recursion, depth-first search, constraint satisfaction concepts
