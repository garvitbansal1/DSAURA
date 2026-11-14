"""
DSAURA Database Seeder

Seeds:
1. DSA Topic taxonomy
2. DSA Pattern library
3. 70+ curated LeetCode problems with classifications

Run with: python -m app.knowledge_base.seed_data
Or call seed_database(db) from application code.
"""

import uuid
from sqlalchemy.orm import Session
from app.models.topic import DSATopic
from app.models.pattern import DSAPattern
from app.models.problem import Problem, problem_topics, problem_patterns
from app.knowledge_base.taxonomy import TOPICS
from app.knowledge_base.patterns_db import PATTERNS


def seed_database(db: Session) -> dict:
    """Idempotent database seeder. Returns counts of seeded items."""
    counts = {"topics": 0, "patterns": 0, "problems": 0}

    # ---- SEED TOPICS ----
    topic_map: dict = {}  # slug -> DSATopic

    # First pass: create all topics (without parent links)
    for slug, name, parent_slug, sort_order, description in TOPICS:
        existing = db.query(DSATopic).filter(DSATopic.slug == slug).first()
        if existing:
            topic_map[slug] = existing
            continue
        topic = DSATopic(
            id=uuid.uuid4(),
            slug=slug,
            name=name,
            sort_order=sort_order,
            description=description,
        )
        db.add(topic)
        topic_map[slug] = topic
        counts["topics"] += 1

    db.flush()

    # Second pass: assign parent_id
    for slug, name, parent_slug, sort_order, description in TOPICS:
        if parent_slug and parent_slug in topic_map:
            topic = topic_map[slug]
            parent = topic_map[parent_slug]
            if topic.parent_id is None:
                topic.parent_id = parent.id

    db.flush()

    # ---- SEED PATTERNS ----
    pattern_map: dict = {}  # slug -> DSAPattern

    for pdata in PATTERNS:
        slug = pdata["slug"]
        existing = db.query(DSAPattern).filter(DSAPattern.slug == slug).first()
        if existing:
            pattern_map[slug] = existing
            continue

        topic_slug = pdata["topic_slug"]
        topic = topic_map.get(topic_slug)
        if not topic:
            continue  # Skip if topic not found

        pattern = DSAPattern(
            id=uuid.uuid4(),
            topic_id=topic.id,
            name=pdata["name"],
            slug=slug,
            explanation=pdata.get("explanation"),
            when_to_use=pdata.get("when_to_use"),
            recognition_clues=pdata.get("recognition_clues"),
            common_keywords=pdata.get("common_keywords", []),
            pseudocode=pdata.get("pseudocode"),
            java_template=pdata.get("java_template"),
            python_template=pdata.get("python_template"),
            time_complexity=pdata.get("time_complexity"),
            space_complexity=pdata.get("space_complexity"),
            common_mistakes=pdata.get("common_mistakes", []),
            difficulty_level=pdata.get("difficulty_level", "medium"),
        )
        db.add(pattern)
        pattern_map[slug] = pattern
        counts["patterns"] += 1

    db.flush()

    # ---- SEED PROBLEMS ----
    # Curated LeetCode problem list with classifications
    CURATED_PROBLEMS = [
        # (lc_id, name, slug, difficulty, [topic_slugs], [pattern_slugs])
        (1, "Two Sum", "two-sum", "easy", ["arrays", "hashing"], ["basic-stack-operations"]),
        (2, "Add Two Numbers", "add-two-numbers", "medium", ["linked-lists"], ["fast-slow-pointer"]),
        (3, "Longest Substring Without Repeating Characters", "longest-substring-without-repeating-characters", "medium", ["strings", "sliding-window"], ["variable-window", "longest-substring"]),
        (15, "3Sum", "3sum", "medium", ["arrays", "two-pointers"], ["two-sum-sorted", "three-sum"]),
        (20, "Valid Parentheses", "valid-parentheses", "easy", ["stacks", "strings"], ["parentheses-matching"]),
        (21, "Merge Two Sorted Lists", "merge-two-sorted-lists", "easy", ["linked-lists"], ["fast-slow-pointer"]),
        (42, "Trapping Rain Water", "trapping-rain-water", "hard", ["arrays", "stacks", "two-pointers"], ["next-smaller-element", "prefix-sum-basic"]),
        (53, "Maximum Subarray", "maximum-subarray", "medium", ["arrays", "dynamic-programming"], ["one-d-dp", "kadanes-algorithm"]),
        (70, "Climbing Stairs", "climbing-stairs", "easy", ["dynamic-programming"], ["memoization-top-down", "tabulation-bottom-up"]),
        (84, "Largest Rectangle in Histogram", "largest-rectangle-in-histogram", "hard", ["stacks", "arrays"], ["largest-rectangle-histogram"]),
        (94, "Binary Tree Inorder Traversal", "binary-tree-inorder-traversal", "easy", ["trees"], ["inorder-traversal"]),
        (100, "Same Tree", "same-tree", "easy", ["trees"], ["tree-dfs-pattern"]),
        (102, "Binary Tree Level Order Traversal", "binary-tree-level-order-traversal", "medium", ["trees", "bfs"], ["level-order-bfs"]),
        (104, "Maximum Depth of Binary Tree", "maximum-depth-of-binary-tree", "easy", ["trees"], ["tree-dfs-pattern"]),
        (121, "Best Time to Buy and Sell Stock", "best-time-to-buy-and-sell-stock", "easy", ["arrays", "dynamic-programming"], ["one-d-dp"]),
        (128, "Longest Consecutive Sequence", "longest-consecutive-sequence", "medium", ["arrays", "hashing"], ["basic-stack-operations"]),
        (141, "Linked List Cycle", "linked-list-cycle", "easy", ["linked-lists"], ["fast-slow-pointer"]),
        (142, "Linked List Cycle II", "linked-list-cycle-ii", "medium", ["linked-lists"], ["fast-slow-pointer"]),
        (152, "Maximum Product Subarray", "maximum-product-subarray", "medium", ["arrays", "dynamic-programming"], ["one-d-dp"]),
        (153, "Find Minimum in Rotated Sorted Array", "find-minimum-in-rotated-sorted-array", "medium", ["binary-search"], ["binary-search-rotated"]),
        (155, "Min Stack", "min-stack", "medium", ["stacks"], ["basic-stack-operations"]),
        (160, "Intersection of Two Linked Lists", "intersection-of-two-linked-lists", "easy", ["linked-lists", "two-pointers"], ["fast-slow-pointer"]),
        (169, "Majority Element", "majority-element", "easy", ["arrays"], ["basic-stack-operations"]),
        (200, "Number of Islands", "number-of-islands", "medium", ["graphs", "bfs", "dfs"], ["graph-bfs", "graph-dfs", "union-find-basic"]),
        (206, "Reverse Linked List", "reverse-linked-list", "easy", ["linked-lists"], ["fast-slow-pointer"]),
        (207, "Course Schedule", "course-schedule", "medium", ["graphs", "topological-sorting"], ["topological-sort-kahn", "cycle-detection-directed"]),
        (208, "Implement Trie (Prefix Tree)", "implement-trie-prefix-tree", "medium", ["tries"], ["trie-insert-search"]),
        (210, "Course Schedule II", "course-schedule-ii", "medium", ["graphs", "topological-sorting"], ["topological-sort-kahn"]),
        (215, "Kth Largest Element in an Array", "kth-largest-element-in-an-array", "medium", ["heaps", "sorting"], ["top-k-elements"]),
        (217, "Contains Duplicate", "contains-duplicate", "easy", ["arrays", "hashing"], ["basic-stack-operations"]),
        (226, "Invert Binary Tree", "invert-binary-tree", "easy", ["trees"], ["tree-dfs-pattern"]),
        (230, "Kth Smallest Element in a BST", "kth-smallest-element-in-a-bst", "medium", ["trees", "binary-search-trees"], ["inorder-traversal", "bst-operations"]),
        (234, "Palindrome Linked List", "palindrome-linked-list", "easy", ["linked-lists", "two-pointers"], ["fast-slow-pointer"]),
        (238, "Product of Array Except Self", "product-of-array-except-self", "medium", ["arrays", "prefix-sum"], ["prefix-sum-basic"]),
        (239, "Sliding Window Maximum", "sliding-window-maximum", "hard", ["stacks", "sliding-window"], ["monotonic-decreasing-stack", "fixed-window"]),
        (242, "Valid Anagram", "valid-anagram", "easy", ["strings", "hashing"], ["basic-stack-operations"]),
        (268, "Missing Number", "missing-number", "easy", ["arrays", "bit-manipulation"], ["prefix-sum-basic"]),
        (300, "Longest Increasing Subsequence", "longest-increasing-subsequence", "medium", ["dynamic-programming"], ["longest-increasing-subsequence", "binary-search-on-answer"]),
        (322, "Coin Change", "coin-change", "medium", ["dynamic-programming"], ["coin-change", "tabulation-bottom-up"]),
        (347, "Top K Frequent Elements", "top-k-frequent-elements", "medium", ["heaps", "hashing"], ["top-k-elements"]),
        (394, "Decode String", "decode-string", "medium", ["stacks", "strings"], ["basic-stack-operations"]),
        (416, "Partition Equal Subset Sum", "partition-equal-subset-sum", "medium", ["dynamic-programming"], ["knapsack-01"]),
        (424, "Longest Repeating Character Replacement", "longest-repeating-character-replacement", "medium", ["strings", "sliding-window"], ["variable-window"]),
        (494, "Target Sum", "target-sum", "medium", ["dynamic-programming"], ["knapsack-01", "memoization-top-down"]),
        (543, "Diameter of Binary Tree", "diameter-of-binary-tree", "easy", ["trees"], ["tree-dfs-pattern", "tree-diameter"]),
        (560, "Subarray Sum Equals K", "subarray-sum-equals-k", "medium", ["arrays", "prefix-sum", "hashing"], ["subarray-sum", "prefix-sum-basic"]),
        (572, "Subtree of Another Tree", "subtree-of-another-tree", "easy", ["trees"], ["tree-dfs-pattern"]),
        (621, "Task Scheduler", "task-scheduler", "medium", ["heaps", "greedy"], ["top-k-elements"]),
        (647, "Palindromic Substrings", "palindromic-substrings", "medium", ["strings", "dynamic-programming"], ["two-d-dp"]),
        (684, "Redundant Connection", "redundant-connection", "medium", ["graphs", "union-find"], ["union-find-basic", "cycle-detection-undirected"]),
        (739, "Daily Temperatures", "daily-temperatures", "medium", ["stacks", "arrays"], ["next-greater-element", "monotonic-decreasing-stack"]),
        (743, "Network Delay Time", "network-delay-time", "medium", ["graphs"], ["dijkstra-shortest-path"]),
        (763, "Partition Labels", "partition-labels", "medium", ["strings", "greedy", "two-pointers"], ["variable-window"]),
        (787, "Cheapest Flights Within K Stops", "cheapest-flights-within-k-stops", "medium", ["graphs", "dynamic-programming"], ["bellman-ford"]),
        (844, "Backspace String Compare", "backspace-string-compare", "easy", ["stacks", "strings", "two-pointers"], ["basic-stack-operations"]),
        (853, "Car Fleet", "car-fleet", "medium", ["stacks", "sorting"], ["monotonic-stack"]),
        (875, "Koko Eating Bananas", "koko-eating-bananas", "medium", ["binary-search"], ["binary-search-on-answer"]),
        (912, "Sort an Array", "sort-an-array", "medium", ["sorting"], ["basic-stack-operations"]),
        (973, "K Closest Points to Origin", "k-closest-points-to-origin", "medium", ["heaps", "sorting"], ["top-k-elements"]),
        (994, "Rotting Oranges", "rotting-oranges", "medium", ["graphs", "bfs"], ["graph-bfs"]),
        (1143, "Longest Common Subsequence", "longest-common-subsequence", "medium", ["dynamic-programming", "strings"], ["longest-common-subsequence"]),
        (1046, "Last Stone Weight", "last-stone-weight", "easy", ["heaps"], ["top-k-elements"]),
        (1143, "Longest Common Subsequence", "longest-common-subsequence", "medium", ["dynamic-programming"], ["longest-common-subsequence"]),
        (11, "Container With Most Water", "container-with-most-water", "medium", ["arrays", "two-pointers"], ["two-sum-sorted"]),
        (33, "Search in Rotated Sorted Array", "search-in-rotated-sorted-array", "medium", ["binary-search"], ["binary-search-rotated"]),
        (74, "Search a 2D Matrix", "search-a-2d-matrix", "medium", ["binary-search", "arrays"], ["basic-binary-search"]),
        (76, "Minimum Window Substring", "minimum-window-substring", "hard", ["strings", "sliding-window"], ["minimum-window"]),
        (110, "Balanced Binary Tree", "balanced-binary-tree", "easy", ["trees"], ["tree-dfs-pattern"]),
        (199, "Binary Tree Right Side View", "binary-tree-right-side-view", "medium", ["trees", "bfs"], ["level-order-bfs"]),
        (417, "Pacific Atlantic Water Flow", "pacific-atlantic-water-flow", "medium", ["graphs", "dfs", "bfs"], ["graph-dfs", "graph-bfs"]),
        (695, "Max Area of Island", "max-area-of-island", "medium", ["graphs", "dfs"], ["graph-dfs"]),
    ]

    seen_lc_ids = set()
    for item in CURATED_PROBLEMS:
        lc_id, name, lc_slug, difficulty, topic_slugs, pattern_slugs = item

        # Skip duplicates
        if lc_id in seen_lc_ids:
            continue
        seen_lc_ids.add(lc_id)

        # Check if problem already exists
        existing = db.query(Problem).filter(
            Problem.platform == "leetcode",
            Problem.platform_id == str(lc_id)
        ).first()
        if existing:
            continue

        problem = Problem(
            id=uuid.uuid4(),
            platform="leetcode",
            platform_id=str(lc_id),
            name=name,
            url=f"https://leetcode.com/problems/{lc_slug}/",
            difficulty=difficulty,
            classification_confidence=0.95,
        )
        db.add(problem)
        db.flush()

        # Associate topics
        for ts in topic_slugs:
            if ts in topic_map:
                db.execute(
                    problem_topics.insert().values(
                        problem_id=problem.id,
                        topic_id=topic_map[ts].id,
                    )
                )

        # Associate patterns
        for ps in pattern_slugs:
            if ps in pattern_map:
                db.execute(
                    problem_patterns.insert().values(
                        problem_id=problem.id,
                        pattern_id=pattern_map[ps].id,
                        confidence=0.95,
                    )
                )

        counts["problems"] += 1

    db.commit()
    return counts


if __name__ == "__main__":
    from app.database import SessionLocal, engine
    from app.models import Base

    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        result = seed_database(db)
        print(f"Seeded: {result}")
    finally:
        db.close()
