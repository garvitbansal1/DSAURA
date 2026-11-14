"""
Complete DSA Topic Taxonomy for DSAURA.
This is the authoritative source for all topics and subtopics.
"""

TOPICS = [
    # format: (slug, name, parent_slug_or_None, sort_order, description)
    ("arrays", "Arrays", None, 1, "Foundation of DSA — contiguous memory elements"),
    ("strings", "Strings", None, 2, "Character sequences and string manipulation"),
    ("hashing", "Hashing", None, 3, "Hash maps, hash sets, and collision handling"),
    ("two-pointers", "Two Pointers", None, 4, "Dual-pointer technique for linear structures"),
    ("sliding-window", "Sliding Window", None, 5, "Dynamic window over sequences"),
    ("binary-search", "Binary Search", None, 6, "Logarithmic search on sorted/monotonic spaces"),
    ("sorting", "Sorting", None, 7, "Ordering algorithms and their applications"),
    ("recursion", "Recursion", None, 8, "Self-referential problem decomposition"),
    ("backtracking", "Backtracking", None, 9, "Exhaustive search with pruning"),
    ("linked-lists", "Linked Lists", None, 10, "Node-based linear data structures"),
    ("stacks", "Stacks", None, 11, "LIFO data structure and applications"),
    ("queues", "Queues", None, 12, "FIFO data structure and variants"),
    ("monotonic-stack", "Monotonic Stack", "stacks", 1, "Stack maintaining monotonic order property"),
    ("trees", "Trees", None, 13, "Hierarchical non-linear data structures"),
    ("binary-search-trees", "Binary Search Trees", "trees", 1, "Ordered binary trees for fast lookup"),
    ("heaps", "Heaps", None, 14, "Priority queue implementations"),
    ("tries", "Tries", None, 15, "Prefix tree for string operations"),
    ("graphs", "Graphs", None, 16, "Network of nodes and edges"),
    ("bfs", "BFS", "graphs", 1, "Breadth-First Search traversal"),
    ("dfs", "DFS", "graphs", 2, "Depth-First Search traversal"),
    ("greedy", "Greedy", None, 17, "Locally optimal choice strategy"),
    ("dynamic-programming", "Dynamic Programming", None, 18, "Optimal substructure and memoization"),
    ("bit-manipulation", "Bit Manipulation", None, 19, "Bitwise operations and tricks"),
    ("prefix-sum", "Prefix Sum", None, 20, "Cumulative sum preprocessing"),
    ("union-find", "Union Find", None, 21, "Disjoint set union data structure"),
    ("topological-sorting", "Topological Sorting", "graphs", 3, "Linear ordering of DAG vertices"),
    ("segment-trees", "Segment Trees", None, 22, "Range query data structure"),
    ("math", "Math", None, 23, "Number theory and mathematical patterns"),
]
