---
name: Greedy Algorithms
description: Problem-solving strategy that makes the locally optimal choice at each step with the hope of finding a global optimum
---

# Greedy Algorithms Paradigm

## What It Is
A problem-solving strategy that makes the locally optimal choice at each step with the hope of finding a global optimum. Unlike dynamic programming which considers all possible decisions, greedy algorithms commit to the best immediate option without reconsidering past choices. The key insight: for certain problems, always choosing what looks best right now leads to the overall best solution.

## When to Use It
- Problem has **greedy choice property** (local optimal choices lead to global optimum)
- Problem has **optimal substructure** (optimal solution contains optimal subsolutions)
- Need fast, simple solution (greedy is usually O(n log n) or better)
- Can prove that greedy choice never needs to be undone
- Making irreversible decisions is acceptable (no backtracking needed)
- Problem involves optimization with ordering/scheduling/selection

**Key Test**: Can you prove that choosing the best option now won't block a better overall solution later?

## Execution Steps

### 1. Evaluate Available Options
At each decision point, identify all valid choices. Define what "best" means for your problem (largest, smallest, earliest deadline, highest ratio). Sort or prioritize options if needed.

**Action**: List all candidates. Define the selection criterion clearly (e.g., "choose activity with earliest finish time" or "select item with highest value/weight ratio").

### 2. Make the Greedy Choice
Select the option that appears optimal according to your criterion. Commit to this choice immediately without considering future consequences. This is the core greedy step.

**Action**: Pick the best option from available candidates. Add it to your solution. This choice is final and irreversible.

### 3. Update State
Remove the chosen option from consideration. Update the problem state based on your choice. Define the new subproblem that remains.

**Action**: Mark chosen item as used. Update constraints (remaining capacity, time, etc.). Recompute what's now available for next iteration.

### 4. Iterate
Repeat steps 1-3 until reaching a solution or no further progress is possible. Each iteration solves a smaller subproblem.

**Action**: Loop until goal achieved, resources exhausted, or no valid choices remain. Return accumulated solution.

### 5. Verify Optimality
Prove (or test) that your greedy strategy produces optimal results. Common proof techniques: exchange argument, greedy stays ahead, structural induction.

**Action**: For known problems (MST, shortest path), use established proofs. For new problems, construct counterexamples to test, or prove correctness formally.

## Real-World Applications

**Scheduling & Resource Allocation**
- Activity selection: conference room booking, CPU task scheduling
- Job sequencing: minimize weighted completion time, maximize throughput
- Huffman coding: optimal prefix-free codes for data compression
- Interval scheduling: maximize non-overlapping meetings

**Graph Algorithms**
- Dijkstra's shortest path: GPS navigation, network routing (OSPF protocol)
- Prim's/Kruskal's MST: network design, circuit layout, cluster analysis
- Fractional knapsack: portfolio optimization with divisible assets

**Network & Routing**
- Load balancing: distribute requests to servers (least loaded server)
- Bandwidth allocation: maximize network utilization
- Packet routing: next-hop forwarding (shortest path to destination)

**Financial & Trading**
- Coin change with specific denominations: make change with fewest coins
- Stock trading: maximize profit with one buy-sell (best time to buy/sell)
- Fractional resource allocation: allocate budget to projects by ROI

**Data Compression**
- Huffman trees: ZIP, JPEG, MP3 compression
- Run-length encoding: simple compression for repeated data
- Optimal merge patterns: external sorting of sorted runs

**Machine Learning**
- Feature selection: forward/backward selection by information gain
- K-means clustering: assign points to nearest centroid
- Decision tree splitting: choose best split by Gini/entropy

## Anti-Patterns

**Using greedy when it doesn't guarantee optimality** → Produces suboptimal results; verify greedy choice property first or use DP.

**Not sorting when needed** → Greedy algorithms often require sorted input; missing this step breaks the strategy.

**Confusing greedy with dynamic programming** → If choices overlap or need reconsideration, use DP; greedy is for irreversible local decisions.

**Applying to 0/1 knapsack** → Greedy fails here (DP required); only works for fractional knapsack.

**Ignoring problem constraints** → Greedy choice must respect all constraints; check feasibility before committing.

**No proof of correctness** → Just because greedy seems to work doesn't mean it's optimal; always verify with proof or exhaustive testing.

## Success Metrics
- Solution matches known optimal value (for problems with established answers)
- Algorithm runs in expected time (typically O(n log n) for sorting-based greedy)
- Proof of correctness established (exchange argument, greedy stays ahead)
- Empirical testing on edge cases confirms optimality
- Simplicity: code is straightforward, easy to understand and maintain

## Related Frameworks
- **Dynamic Programming**: When greedy fails, DP often succeeds (but slower)
- **Divide and Conquer**: Both make decisions and recurse, but D&C doesn't commit locally
- **Backtracking**: For constraint satisfaction when greedy is insufficient
- **Primal-Dual Algorithms**: Greedy with duality theory for approximation algorithms
- **Matroid Theory**: Mathematical framework proving when greedy works

## Common Pitfalls
- Assuming greedy always works (it doesn't - most optimization problems need DP or search)
- Not proving correctness (greedy algorithms are easy to get wrong)
- Choosing wrong greedy criterion (e.g., sorting by value instead of value/weight ratio)
- Forgetting to sort input when order matters
- Applying greedy to problems requiring backtracking (e.g., N-Queens, Sudoku)
- Not handling ties in selection criterion (can lead to non-deterministic results)

## Tools & Resources
- **Visualization**: VisuAlgo (visualgo.net) for greedy algorithm animations
- **Practice**: LeetCode greedy tag (~150 problems), Codeforces greedy category
- **Books**: "Algorithm Design" (Kleinberg & Tardos), "Introduction to Algorithms" (CLRS)
- **Proof Techniques**: "Exchange argument" tutorial, "Greedy stays ahead" proof pattern
- **Counterexample Testing**: Generate random inputs, compare greedy vs. brute force on small instances

## Classic Greedy Algorithms

**Activity Selection**: Choose activities with earliest finish time → maximizes number of non-overlapping activities

**Fractional Knapsack**: Sort items by value/weight ratio, take highest ratios first → optimal value

**Huffman Coding**: Build tree by repeatedly merging two lowest-frequency nodes → optimal prefix-free code

**Dijkstra's Algorithm**: Always expand nearest unvisited node → shortest paths from source

**Kruskal's MST**: Add cheapest edge that doesn't create cycle → minimum spanning tree

**Prim's MST**: Grow tree by adding cheapest edge to current tree → minimum spanning tree

**Coin Change (specific denominations)**: Always take largest coin ≤ remaining amount → fewest coins (works for standard denominations like US coins)

## When Greedy Fails

**0/1 Knapsack**: Can't split items, so greedy by value/weight fails. Need DP.

**Longest Path**: Greedy (always choose longest available edge) fails. NP-hard, need exponential search.

**Traveling Salesman**: Greedy (nearest neighbor) gives 2-approximation but not optimal. Need sophisticated approaches.

**Job Scheduling with Dependencies**: Greedy ignores dependencies. Need topological sort + DP.

**Fair Division**: Greedy may give one party too much. Need game-theoretic approaches.

---
*Framework Type*: Algorithm Design Paradigm
*Domain*: Computer Science, Optimization
*Practitioner Score*: 9/10 - Powers many production algorithms (Dijkstra, MST, Huffman)
*Complexity*: Medium - Conceptually simple, but proving correctness is non-trivial
*Prerequisites*: Sorting algorithms, basic graph theory, proof techniques (induction, contradiction)
