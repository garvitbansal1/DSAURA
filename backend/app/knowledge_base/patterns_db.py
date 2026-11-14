"""
Complete DSA Pattern Library for DSAURA.
Every pattern has: slug, name, topic_slug, explanation, when_to_use,
recognition_clues, common_keywords, pseudocode, java_template,
python_template, time_complexity, space_complexity, common_mistakes,
difficulty_level.
"""

PATTERNS = [
    # =========================================================
    # STACK PATTERNS
    # =========================================================
    {
        "slug": "basic-stack-operations",
        "name": "Basic Stack Operations",
        "topic_slug": "stacks",
        "difficulty_level": "easy",
        "explanation": (
            "A stack is a Last-In-First-Out (LIFO) data structure. "
            "Elements are pushed onto the top and popped from the top. "
            "It is the foundation for many advanced patterns like monotonic stacks, "
            "expression evaluation, and backtracking."
        ),
        "when_to_use": (
            "Use a stack when you need to process elements in reverse order, "
            "track nested structures, or undo recent operations."
        ),
        "recognition_clues": (
            "Keywords: 'last in first out', 'undo', 'reverse order', 'nested', "
            "'balanced brackets', 'function call'. "
            "Problems that require remembering the most recently seen element."
        ),
        "common_keywords": ["push", "pop", "peek", "top", "LIFO", "last", "recent", "undo"],
        "pseudocode": (
            "stack = []\n"
            "PUSH(x): stack.append(x)\n"
            "POP(): return stack.pop()  # removes and returns top\n"
            "PEEK(): return stack[-1]   # returns top without removing\n"
            "IS_EMPTY(): return len(stack) == 0"
        ),
        "python_template": (
            "stack = []\n\n"
            "# Push\n"
            "stack.append(element)\n\n"
            "# Pop (always check not empty first)\n"
            "if stack:\n"
            "    top = stack.pop()\n\n"
            "# Peek\n"
            "if stack:\n"
            "    top = stack[-1]"
        ),
        "java_template": (
            "Deque<Integer> stack = new ArrayDeque<>();\n\n"
            "// Push\n"
            "stack.push(element);\n\n"
            "// Pop\n"
            "if (!stack.isEmpty()) {\n"
            "    int top = stack.pop();\n"
            "}\n\n"
            "// Peek\n"
            "if (!stack.isEmpty()) {\n"
            "    int top = stack.peek();\n"
            "}"
        ),
        "time_complexity": "O(1) per operation",
        "space_complexity": "O(n) for n elements",
        "common_mistakes": [
            "Popping from an empty stack (causes error/exception)",
            "Using a List as stack (pop from front is O(n))",
            "Forgetting to check isEmpty() before accessing top",
        ],
    },
    {
        "slug": "parentheses-matching",
        "name": "Parentheses Matching",
        "topic_slug": "stacks",
        "difficulty_level": "easy",
        "explanation": (
            "Use a stack to track opening brackets. When a closing bracket is encountered, "
            "check if the top of the stack contains the matching opener. "
            "If yes, pop and continue. If no, the string is invalid."
        ),
        "when_to_use": (
            "Whenever you need to validate or process nested/paired structures: "
            "brackets, parentheses, HTML/XML tags, nested function calls."
        ),
        "recognition_clues": (
            "Problem involves matching pairs: (), [], {}. "
            "Keywords: 'valid', 'balanced', 'matching', 'brackets', 'parentheses'."
        ),
        "common_keywords": ["valid", "balanced", "brackets", "parentheses", "matching", "pairs"],
        "pseudocode": (
            "stack = []\n"
            "matching = {')': '(', ']': '[', '}': '{'}\n"
            "for char in s:\n"
            "    if char in '([{':\n"
            "        stack.push(char)\n"
            "    else:\n"
            "        if stack is empty OR stack.top() != matching[char]:\n"
            "            return False\n"
            "        stack.pop()\n"
            "return stack is empty"
        ),
        "python_template": (
            "def is_valid(s: str) -> bool:\n"
            "    stack = []\n"
            "    matching = {')': '(', ']': '[', '}': '{'}\n"
            "    for char in s:\n"
            "        if char in '([{':\n"
            "            stack.append(char)\n"
            "        else:\n"
            "            if not stack or stack[-1] != matching[char]:\n"
            "                return False\n"
            "            stack.pop()\n"
            "    return len(stack) == 0"
        ),
        "java_template": (
            "public boolean isValid(String s) {\n"
            "    Deque<Character> stack = new ArrayDeque<>();\n"
            "    for (char c : s.toCharArray()) {\n"
            "        if (c == '(' || c == '[' || c == '{') {\n"
            "            stack.push(c);\n"
            "        } else {\n"
            "            if (stack.isEmpty()) return false;\n"
            "            char top = stack.pop();\n"
            "            if ((c == ')' && top != '(') ||\n"
            "                (c == ']' && top != '[') ||\n"
            "                (c == '}' && top != '{')) return false;\n"
            "        }\n"
            "    }\n"
            "    return stack.isEmpty();\n"
            "}"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "common_mistakes": [
            "Not checking if stack is empty before popping",
            "Forgetting to check if stack is empty at the end",
            "Using wrong mapping direction for matching",
        ],
    },
    {
        "slug": "next-greater-element",
        "name": "Next Greater Element",
        "topic_slug": "monotonic-stack",
        "difficulty_level": "medium",
        "explanation": (
            "For each element in an array, find the next element to its right that is strictly greater. "
            "Use a monotonic decreasing stack of indices. When a larger element is found, "
            "it is the NGE for all elements still in the stack that are smaller."
        ),
        "when_to_use": (
            "Problems asking: 'for each element, find the next larger/smaller element'. "
            "Also used as a subroutine in Stock Span, Histogram, and Circular Array problems."
        ),
        "recognition_clues": (
            "Keywords: 'next greater', 'next larger', 'right side'. "
            "Pattern: for each element, look rightward for a condition. "
            "O(n²) brute force suggests a stack optimization."
        ),
        "common_keywords": ["next greater", "next larger", "right", "span", "daily temperatures"],
        "pseudocode": (
            "result = [-1] * n\n"
            "stack = []  # stores indices\n"
            "for i in range(n):\n"
            "    # While current element > top of stack element\n"
            "    while stack and nums[i] > nums[stack[-1]]:\n"
            "        idx = stack.pop()\n"
            "        result[idx] = nums[i]  # nums[i] is NGE for idx\n"
            "    stack.append(i)\n"
            "# Elements remaining in stack have no NGE (result stays -1)"
        ),
        "python_template": (
            "def next_greater_element(nums):\n"
            "    n = len(nums)\n"
            "    result = [-1] * n\n"
            "    stack = []  # stores indices\n"
            "    \n"
            "    for i in range(n):\n"
            "        while stack and nums[i] > nums[stack[-1]]:\n"
            "            idx = stack.pop()\n"
            "            result[idx] = nums[i]\n"
            "        stack.append(i)\n"
            "    \n"
            "    return result"
        ),
        "java_template": (
            "public int[] nextGreaterElement(int[] nums) {\n"
            "    int n = nums.length;\n"
            "    int[] result = new int[n];\n"
            "    Arrays.fill(result, -1);\n"
            "    Deque<Integer> stack = new ArrayDeque<>(); // indices\n"
            "    \n"
            "    for (int i = 0; i < n; i++) {\n"
            "        while (!stack.isEmpty() && nums[i] > nums[stack.peek()]) {\n"
            "            int idx = stack.pop();\n"
            "            result[idx] = nums[i];\n"
            "        }\n"
            "        stack.push(i);\n"
            "    }\n"
            "    return result;\n"
            "}"
        ),
        "time_complexity": "O(n) — each element pushed and popped at most once",
        "space_complexity": "O(n)",
        "common_mistakes": [
            "Storing values instead of indices in the stack (makes it hard to update result)",
            "Forgetting circular array variant requires 2 passes",
            "Confusing 'next greater' (strict) with 'next greater or equal'",
        ],
    },
    {
        "slug": "next-smaller-element",
        "name": "Next Smaller Element",
        "topic_slug": "monotonic-stack",
        "difficulty_level": "medium",
        "explanation": (
            "Same idea as NGE but we look for the next element that is strictly smaller. "
            "Use a monotonic increasing stack. Pop when a smaller element is found."
        ),
        "when_to_use": "Problems asking 'next smaller to the right/left'. Often combined with NGE in histogram problems.",
        "recognition_clues": "Similar to NGE but looking for smaller values. Stack is maintained in increasing order.",
        "common_keywords": ["next smaller", "next minimum", "trap water", "histogram"],
        "pseudocode": (
            "result = [-1] * n\n"
            "stack = []  # indices, increasing order of values\n"
            "for i in range(n):\n"
            "    while stack and nums[i] < nums[stack[-1]]:\n"
            "        idx = stack.pop()\n"
            "        result[idx] = nums[i]\n"
            "    stack.append(i)"
        ),
        "python_template": (
            "def next_smaller_element(nums):\n"
            "    n = len(nums)\n"
            "    result = [-1] * n\n"
            "    stack = []\n"
            "    for i in range(n):\n"
            "        while stack and nums[i] < nums[stack[-1]]:\n"
            "            idx = stack.pop()\n"
            "            result[idx] = nums[i]\n"
            "        stack.append(i)\n"
            "    return result"
        ),
        "java_template": (
            "public int[] nextSmallerElement(int[] nums) {\n"
            "    int n = nums.length;\n"
            "    int[] result = new int[n];\n"
            "    Arrays.fill(result, -1);\n"
            "    Deque<Integer> stack = new ArrayDeque<>();\n"
            "    for (int i = 0; i < n; i++) {\n"
            "        while (!stack.isEmpty() && nums[i] < nums[stack.peek()]) {\n"
            "            result[stack.pop()] = nums[i];\n"
            "        }\n"
            "        stack.push(i);\n"
            "    }\n"
            "    return result;\n"
            "}"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "common_mistakes": [
            "Confusing the direction of comparison (< vs >)",
            "Mixing up Next Smaller vs Previous Smaller",
        ],
    },
    {
        "slug": "largest-rectangle-histogram",
        "name": "Largest Rectangle in Histogram",
        "topic_slug": "monotonic-stack",
        "difficulty_level": "hard",
        "explanation": (
            "For each bar, find the largest rectangle that uses that bar as the shortest bar. "
            "Use a monotonic increasing stack. When a shorter bar is found, "
            "pop and calculate the rectangle area using the popped bar as height."
        ),
        "when_to_use": "Classic hard stack problem. Also appears as a subroutine in 'Maximal Rectangle in Binary Matrix'.",
        "recognition_clues": "Involves finding the largest area under a height array. Bars with heights forming a histogram.",
        "common_keywords": ["histogram", "rectangle", "area", "maximal", "largest"],
        "pseudocode": (
            "stack = []  # indices, increasing heights\n"
            "max_area = 0\n"
            "for i in range(len(heights) + 1):\n"
            "    h = heights[i] if i < len(heights) else 0\n"
            "    while stack and h < heights[stack[-1]]:\n"
            "        height = heights[stack.pop()]\n"
            "        width = i if not stack else i - stack[-1] - 1\n"
            "        max_area = max(max_area, height * width)\n"
            "    stack.append(i)\n"
            "return max_area"
        ),
        "python_template": (
            "def largest_rectangle_area(heights):\n"
            "    stack = []  # monotonic increasing stack of indices\n"
            "    max_area = 0\n"
            "    n = len(heights)\n"
            "    \n"
            "    for i in range(n + 1):\n"
            "        h = heights[i] if i < n else 0\n"
            "        while stack and h < heights[stack[-1]]:\n"
            "            height = heights[stack.pop()]\n"
            "            width = i if not stack else i - stack[-1] - 1\n"
            "            max_area = max(max_area, height * width)\n"
            "        stack.append(i)\n"
            "    \n"
            "    return max_area"
        ),
        "java_template": (
            "public int largestRectangleArea(int[] heights) {\n"
            "    int n = heights.length;\n"
            "    int maxArea = 0;\n"
            "    Deque<Integer> stack = new ArrayDeque<>();\n"
            "    \n"
            "    for (int i = 0; i <= n; i++) {\n"
            "        int h = (i == n) ? 0 : heights[i];\n"
            "        while (!stack.isEmpty() && h < heights[stack.peek()]) {\n"
            "            int height = heights[stack.pop()];\n"
            "            int width = stack.isEmpty() ? i : i - stack.peek() - 1;\n"
            "            maxArea = Math.max(maxArea, height * width);\n"
            "        }\n"
            "        stack.push(i);\n"
            "    }\n"
            "    return maxArea;\n"
            "}"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "common_mistakes": [
            "Incorrect width calculation when stack is empty after pop",
            "Not handling the sentinel (0 at end) to flush remaining stack",
            "Off-by-one in width formula",
        ],
    },
    # =========================================================
    # BINARY SEARCH PATTERNS
    # =========================================================
    {
        "slug": "basic-binary-search",
        "name": "Basic Binary Search",
        "topic_slug": "binary-search",
        "difficulty_level": "easy",
        "explanation": (
            "Eliminate half the search space in each step by comparing the target with the middle element. "
            "Only works on sorted arrays. Achieves O(log n) search time."
        ),
        "when_to_use": "Sorted array + search for a value. Any problem where you can halve the search space.",
        "recognition_clues": "Sorted array, searching for exact value, O(log n) expected.",
        "common_keywords": ["sorted", "search", "find", "target", "binary", "log n"],
        "pseudocode": (
            "lo, hi = 0, len(arr) - 1\n"
            "while lo <= hi:\n"
            "    mid = lo + (hi - lo) // 2\n"
            "    if arr[mid] == target:\n"
            "        return mid\n"
            "    elif arr[mid] < target:\n"
            "        lo = mid + 1\n"
            "    else:\n"
            "        hi = mid - 1\n"
            "return -1"
        ),
        "python_template": (
            "def binary_search(arr, target):\n"
            "    lo, hi = 0, len(arr) - 1\n"
            "    while lo <= hi:\n"
            "        mid = lo + (hi - lo) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return -1"
        ),
        "java_template": (
            "public int binarySearch(int[] arr, int target) {\n"
            "    int lo = 0, hi = arr.length - 1;\n"
            "    while (lo <= hi) {\n"
            "        int mid = lo + (hi - lo) / 2;\n"
            "        if (arr[mid] == target) return mid;\n"
            "        else if (arr[mid] < target) lo = mid + 1;\n"
            "        else hi = mid - 1;\n"
            "    }\n"
            "    return -1;\n"
            "}"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "common_mistakes": [
            "Integer overflow: use mid = lo + (hi - lo) / 2 not (lo + hi) / 2",
            "Using lo < hi instead of lo <= hi (misses single element)",
            "Applying binary search to unsorted data",
        ],
    },
    {
        "slug": "binary-search-on-answer",
        "name": "Binary Search on Answer",
        "topic_slug": "binary-search",
        "difficulty_level": "hard",
        "explanation": (
            "Instead of searching for a value in an array, binary search over the answer space itself. "
            "Define a predicate function f(x) that is monotonic (once false, always false). "
            "Binary search to find the boundary where f transitions from true to false (or vice versa)."
        ),
        "when_to_use": (
            "Problems asking 'find the minimum/maximum value such that some condition holds'. "
            "Classic examples: Koko Eating Bananas, Ship Within D Days, Minimum Days to Make Bouquet."
        ),
        "recognition_clues": (
            "Asks for 'minimum possible maximum' or 'maximum possible minimum'. "
            "Answer can be binary-searched. A feasibility check function exists."
        ),
        "common_keywords": ["minimum", "maximum", "feasible", "can", "at most", "at least", "capacity", "speed"],
        "pseudocode": (
            "def can_achieve(mid):  # check if answer = mid is feasible\n"
            "    ...\n"
            "\n"
            "lo, hi = min_possible_answer, max_possible_answer\n"
            "while lo < hi:\n"
            "    mid = lo + (hi - lo) // 2\n"
            "    if can_achieve(mid):\n"
            "        hi = mid       # mid works, try smaller\n"
            "    else:\n"
            "        lo = mid + 1   # mid doesn't work, need larger\n"
            "return lo"
        ),
        "python_template": (
            "def solve(nums, limit):\n"
            "    def feasible(capacity):\n"
            "        # Check if 'capacity' satisfies the problem constraint\n"
            "        # Return True if achievable, False otherwise\n"
            "        ...\n"
            "    \n"
            "    lo, hi = 1, max(nums)  # define search space\n"
            "    while lo < hi:\n"
            "        mid = lo + (hi - lo) // 2\n"
            "        if feasible(mid):\n"
            "            hi = mid\n"
            "        else:\n"
            "            lo = mid + 1\n"
            "    return lo"
        ),
        "java_template": (
            "private boolean feasible(int[] nums, int capacity) {\n"
            "    // Check if capacity satisfies the constraint\n"
            "    return true; // implement logic\n"
            "}\n\n"
            "public int solve(int[] nums) {\n"
            "    int lo = 1, hi = Arrays.stream(nums).max().getAsInt();\n"
            "    while (lo < hi) {\n"
            "        int mid = lo + (hi - lo) / 2;\n"
            "        if (feasible(nums, mid)) hi = mid;\n"
            "        else lo = mid + 1;\n"
            "    }\n"
            "    return lo;\n"
            "}"
        ),
        "time_complexity": "O(n log(answer_range))",
        "space_complexity": "O(1) or O(n) depending on feasibility check",
        "common_mistakes": [
            "Wrong boundary: lo = 0 when answer must be >= 1",
            "Using lo <= hi instead of lo < hi (leads to infinite loop for minimum-finding)",
            "Incorrect feasibility function direction",
            "Not identifying that the answer space is monotonic",
        ],
    },
    # =========================================================
    # SLIDING WINDOW PATTERNS
    # =========================================================
    {
        "slug": "fixed-window",
        "name": "Fixed Size Sliding Window",
        "topic_slug": "sliding-window",
        "difficulty_level": "easy",
        "explanation": (
            "Maintain a window of exactly k elements. Slide it from left to right, "
            "adding the new element and removing the oldest. Compute the aggregate "
            "(sum, max, etc.) efficiently by updating instead of recomputing."
        ),
        "when_to_use": "When k is given explicitly and the window never changes size.",
        "recognition_clues": "Window size k is fixed. 'Sum/max/min of every k consecutive elements'.",
        "common_keywords": ["window size k", "subarray of length k", "consecutive k elements"],
        "pseudocode": (
            "window_sum = sum(nums[0:k])\n"
            "result = [window_sum]\n"
            "for i in range(k, n):\n"
            "    window_sum += nums[i] - nums[i - k]  # add new, remove old\n"
            "    result.append(window_sum)\n"
            "return result"
        ),
        "python_template": (
            "def max_sum_subarray(nums, k):\n"
            "    n = len(nums)\n"
            "    window_sum = sum(nums[:k])\n"
            "    max_sum = window_sum\n"
            "    \n"
            "    for i in range(k, n):\n"
            "        window_sum += nums[i] - nums[i - k]\n"
            "        max_sum = max(max_sum, window_sum)\n"
            "    \n"
            "    return max_sum"
        ),
        "java_template": (
            "public int maxSumSubarray(int[] nums, int k) {\n"
            "    int windowSum = 0;\n"
            "    for (int i = 0; i < k; i++) windowSum += nums[i];\n"
            "    int maxSum = windowSum;\n"
            "    for (int i = k; i < nums.length; i++) {\n"
            "        windowSum += nums[i] - nums[i - k];\n"
            "        maxSum = Math.max(maxSum, windowSum);\n"
            "    }\n"
            "    return maxSum;\n"
            "}"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "common_mistakes": [
            "Computing sum from scratch for each window (O(nk) instead of O(n))",
            "Off-by-one in window removal index",
        ],
    },
    {
        "slug": "variable-window",
        "name": "Variable Size Sliding Window",
        "topic_slug": "sliding-window",
        "difficulty_level": "medium",
        "explanation": (
            "Expand the window by moving the right pointer. "
            "Shrink from the left when the window violates a constraint. "
            "Track the optimal window seen so far."
        ),
        "when_to_use": "Find the longest/shortest subarray satisfying a condition. Window size is not fixed.",
        "recognition_clues": "Subarray questions with a constraint (at most k distinct, sum equals target). No fixed k.",
        "common_keywords": ["longest", "shortest", "at most", "at least", "subarray", "substring"],
        "pseudocode": (
            "left = 0\n"
            "result = 0\n"
            "window_state = {}  # track window contents\n"
            "\n"
            "for right in range(n):\n"
            "    # Expand window: add nums[right]\n"
            "    update(window_state, nums[right])\n"
            "    \n"
            "    # Shrink window while constraint violated\n"
            "    while constraint_violated(window_state):\n"
            "        remove(window_state, nums[left])\n"
            "        left += 1\n"
            "    \n"
            "    # Update result with current valid window\n"
            "    result = max(result, right - left + 1)"
        ),
        "python_template": (
            "def longest_subarray_with_condition(nums, k):\n"
            "    left = 0\n"
            "    result = 0\n"
            "    freq = {}  # or any window state\n"
            "    \n"
            "    for right in range(len(nums)):\n"
            "        freq[nums[right]] = freq.get(nums[right], 0) + 1\n"
            "        \n"
            "        # Shrink when condition violated\n"
            "        while len(freq) > k:  # example condition\n"
            "            freq[nums[left]] -= 1\n"
            "            if freq[nums[left]] == 0:\n"
            "                del freq[nums[left]]\n"
            "            left += 1\n"
            "        \n"
            "        result = max(result, right - left + 1)\n"
            "    \n"
            "    return result"
        ),
        "java_template": (
            "public int longestSubarray(int[] nums, int k) {\n"
            "    int left = 0, result = 0;\n"
            "    Map<Integer, Integer> freq = new HashMap<>();\n"
            "    \n"
            "    for (int right = 0; right < nums.length; right++) {\n"
            "        freq.merge(nums[right], 1, Integer::sum);\n"
            "        \n"
            "        while (freq.size() > k) {  // example condition\n"
            "            freq.merge(nums[left], -1, Integer::sum);\n"
            "            if (freq.get(nums[left]) == 0)\n"
            "                freq.remove(nums[left]);\n"
            "            left++;\n"
            "        }\n"
            "        result = Math.max(result, right - left + 1);\n"
            "    }\n"
            "    return result;\n"
            "}"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(k) for the frequency map",
        "common_mistakes": [
            "Moving left pointer too aggressively (using if instead of while)",
            "Not updating frequency map when shrinking",
            "Wrong direction of optimization (max vs min window)",
        ],
    },
    # =========================================================
    # TWO POINTERS
    # =========================================================
    {
        "slug": "two-sum-sorted",
        "name": "Two Sum on Sorted Array",
        "topic_slug": "two-pointers",
        "difficulty_level": "easy",
        "explanation": (
            "With a sorted array, place one pointer at the start (lo) and one at the end (hi). "
            "If sum < target, move lo right. If sum > target, move hi left. If equal, found."
        ),
        "when_to_use": "Find pair with given sum in sorted array. Avoids O(n²) brute force.",
        "recognition_clues": "Sorted array, find pair summing to target. 'Two numbers', 'pair'.",
        "common_keywords": ["two sum", "pair", "sorted", "target sum", "complement"],
        "pseudocode": (
            "lo, hi = 0, n - 1\n"
            "while lo < hi:\n"
            "    s = arr[lo] + arr[hi]\n"
            "    if s == target:\n"
            "        return [lo, hi]\n"
            "    elif s < target:\n"
            "        lo += 1\n"
            "    else:\n"
            "        hi -= 1\n"
            "return []"
        ),
        "python_template": (
            "def two_sum_sorted(numbers, target):\n"
            "    lo, hi = 0, len(numbers) - 1\n"
            "    while lo < hi:\n"
            "        s = numbers[lo] + numbers[hi]\n"
            "        if s == target:\n"
            "            return [lo + 1, hi + 1]  # 1-indexed\n"
            "        elif s < target:\n"
            "            lo += 1\n"
            "        else:\n"
            "            hi -= 1\n"
            "    return []"
        ),
        "java_template": (
            "public int[] twoSum(int[] numbers, int target) {\n"
            "    int lo = 0, hi = numbers.length - 1;\n"
            "    while (lo < hi) {\n"
            "        int sum = numbers[lo] + numbers[hi];\n"
            "        if (sum == target) return new int[]{lo + 1, hi + 1};\n"
            "        else if (sum < target) lo++;\n"
            "        else hi--;\n"
            "    }\n"
            "    return new int[]{};\n"
            "}"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "common_mistakes": [
            "Applying to unsorted array (use hash map instead)",
            "Using lo <= hi (misses the case where same index used twice)",
        ],
    },
    {
        "slug": "fast-slow-pointer",
        "name": "Fast and Slow Pointers (Floyd's Algorithm)",
        "topic_slug": "linked-lists",
        "difficulty_level": "medium",
        "explanation": (
            "Use two pointers moving at different speeds (slow moves 1 step, fast moves 2). "
            "If a cycle exists, they will meet inside it. "
            "To find the cycle start: reset one pointer to head after they meet, then advance both by 1 until they meet again."
        ),
        "when_to_use": "Detect cycle in linked list, find middle of linked list, detect cycle start.",
        "recognition_clues": "Linked list + cycle detection. 'Middle of list'. 'Happy number' (implicit cycle).",
        "common_keywords": ["cycle", "loop", "linked list", "middle", "fast", "slow", "Floyd"],
        "pseudocode": (
            "slow = fast = head\n"
            "# Detect cycle\n"
            "while fast and fast.next:\n"
            "    slow = slow.next\n"
            "    fast = fast.next.next\n"
            "    if slow == fast:\n"
            "        return True  # cycle detected\n"
            "return False"
        ),
        "python_template": (
            "def has_cycle(head):\n"
            "    slow = fast = head\n"
            "    while fast and fast.next:\n"
            "        slow = slow.next\n"
            "        fast = fast.next.next\n"
            "        if slow == fast:\n"
            "            return True\n"
            "    return False\n"
            "\n"
            "def find_middle(head):\n"
            "    slow = fast = head\n"
            "    while fast and fast.next:\n"
            "        slow = slow.next\n"
            "        fast = fast.next.next\n"
            "    return slow  # slow is at middle"
        ),
        "java_template": (
            "public boolean hasCycle(ListNode head) {\n"
            "    ListNode slow = head, fast = head;\n"
            "    while (fast != null && fast.next != null) {\n"
            "        slow = slow.next;\n"
            "        fast = fast.next.next;\n"
            "        if (slow == fast) return true;\n"
            "    }\n"
            "    return false;\n"
            "}"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "common_mistakes": [
            "Not checking fast.next before accessing fast.next.next (NullPointerException)",
            "Stopping when slow == fast for cycle start detection (need extra step)",
        ],
    },
    # =========================================================
    # DYNAMIC PROGRAMMING PATTERNS
    # =========================================================
    {
        "slug": "memoization-top-down",
        "name": "Top-Down Memoization",
        "topic_slug": "dynamic-programming",
        "difficulty_level": "medium",
        "explanation": (
            "Start from the original problem and recursively break it into subproblems. "
            "Cache the result of each subproblem in a memo table so each is computed only once. "
            "Natural extension of recursion — add a cache."
        ),
        "when_to_use": "When a recursive solution has overlapping subproblems. Good starting point before converting to tabulation.",
        "recognition_clues": "Recursive structure with repeated subproblems. Try brute force first, then add cache.",
        "common_keywords": ["cache", "memo", "recursive", "overlapping", "subproblem"],
        "pseudocode": (
            "memo = {}\n"
            "def dp(state):\n"
            "    if state in memo:\n"
            "        return memo[state]\n"
            "    if base_case(state):\n"
            "        return base_value\n"
            "    result = combine(dp(sub_state1), dp(sub_state2), ...)\n"
            "    memo[state] = result\n"
            "    return result"
        ),
        "python_template": (
            "from functools import lru_cache\n"
            "\n"
            "def solve(n):\n"
            "    @lru_cache(maxsize=None)\n"
            "    def dp(i):\n"
            "        if i == 0: return base_value\n"
            "        # Combine subproblem results\n"
            "        return dp(i - 1) + dp(i - 2)  # example: fibonacci\n"
            "    \n"
            "    return dp(n)"
        ),
        "java_template": (
            "Map<Integer, Integer> memo = new HashMap<>();\n"
            "\n"
            "public int dp(int i) {\n"
            "    if (i == 0) return 0; // base case\n"
            "    if (memo.containsKey(i)) return memo.get(i);\n"
            "    int result = dp(i - 1) + dp(i - 2); // example\n"
            "    memo.put(i, result);\n"
            "    return result;\n"
            "}"
        ),
        "time_complexity": "O(states * transition cost)",
        "space_complexity": "O(states) for memo + O(depth) for call stack",
        "common_mistakes": [
            "Caching before computing (should cache after)",
            "Using mutable objects as cache keys",
            "Forgetting base cases",
        ],
    },
    {
        "slug": "knapsack-01",
        "name": "0/1 Knapsack",
        "topic_slug": "dynamic-programming",
        "difficulty_level": "medium",
        "explanation": (
            "Classic DP: given items with weights and values, fill a knapsack of capacity W "
            "to maximize value. Each item can be included at most once (0/1). "
            "dp[i][w] = max value using first i items with capacity w."
        ),
        "when_to_use": "Subset selection with capacity constraint. 'Can we achieve exactly X using subset of items?'",
        "recognition_clues": "Items, weights/costs, capacity, include/exclude decision. Subset Sum is a variant.",
        "common_keywords": ["knapsack", "subset", "include", "exclude", "capacity", "weight", "value"],
        "pseudocode": (
            "dp[0..n][0..W] = 0\n"
            "for i in 1..n:\n"
            "    for w in 0..W:\n"
            "        # Exclude item i\n"
            "        dp[i][w] = dp[i-1][w]\n"
            "        # Include item i (if it fits)\n"
            "        if weights[i-1] <= w:\n"
            "            dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1])\n"
            "return dp[n][W]"
        ),
        "python_template": (
            "def knapsack_01(weights, values, W):\n"
            "    n = len(weights)\n"
            "    dp = [[0] * (W + 1) for _ in range(n + 1)]\n"
            "    \n"
            "    for i in range(1, n + 1):\n"
            "        for w in range(W + 1):\n"
            "            dp[i][w] = dp[i-1][w]  # exclude\n"
            "            if weights[i-1] <= w:\n"
            "                dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1])\n"
            "    \n"
            "    return dp[n][W]"
        ),
        "java_template": (
            "public int knapsack(int[] weights, int[] values, int W) {\n"
            "    int n = weights.length;\n"
            "    int[][] dp = new int[n + 1][W + 1];\n"
            "    for (int i = 1; i <= n; i++) {\n"
            "        for (int w = 0; w <= W; w++) {\n"
            "            dp[i][w] = dp[i-1][w];\n"
            "            if (weights[i-1] <= w)\n"
            "                dp[i][w] = Math.max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1]);\n"
            "        }\n"
            "    }\n"
            "    return dp[n][W];\n"
            "}"
        ),
        "time_complexity": "O(n * W)",
        "space_complexity": "O(n * W), reducible to O(W) with 1D DP",
        "common_mistakes": [
            "Using 0D array and iterating w left-to-right (use right-to-left for 1D 0/1 knapsack)",
            "Confusing 0/1 knapsack (each item once) with unbounded knapsack (unlimited)",
        ],
    },
    {
        "slug": "longest-common-subsequence",
        "name": "Longest Common Subsequence (LCS)",
        "topic_slug": "dynamic-programming",
        "difficulty_level": "medium",
        "explanation": (
            "dp[i][j] = length of LCS of text1[0..i-1] and text2[0..j-1]. "
            "If characters match: dp[i][j] = dp[i-1][j-1] + 1. "
            "Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])."
        ),
        "when_to_use": "Find common subsequence between two strings/sequences. Base for Edit Distance, Shortest Common Supersequence.",
        "recognition_clues": "Two strings, 'common subsequence', 'edit distance', 'delete operations'.",
        "common_keywords": ["LCS", "subsequence", "common", "two strings", "edit", "delete"],
        "pseudocode": (
            "dp[0..m][0..n] = 0\n"
            "for i in 1..m:\n"
            "    for j in 1..n:\n"
            "        if text1[i-1] == text2[j-1]:\n"
            "            dp[i][j] = dp[i-1][j-1] + 1\n"
            "        else:\n"
            "            dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n"
            "return dp[m][n]"
        ),
        "python_template": (
            "def lcs(text1, text2):\n"
            "    m, n = len(text1), len(text2)\n"
            "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
            "    for i in range(1, m + 1):\n"
            "        for j in range(1, n + 1):\n"
            "            if text1[i-1] == text2[j-1]:\n"
            "                dp[i][j] = dp[i-1][j-1] + 1\n"
            "            else:\n"
            "                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n"
            "    return dp[m][n]"
        ),
        "java_template": (
            "public int longestCommonSubsequence(String text1, String text2) {\n"
            "    int m = text1.length(), n = text2.length();\n"
            "    int[][] dp = new int[m + 1][n + 1];\n"
            "    for (int i = 1; i <= m; i++) {\n"
            "        for (int j = 1; j <= n; j++) {\n"
            "            if (text1.charAt(i-1) == text2.charAt(j-1))\n"
            "                dp[i][j] = dp[i-1][j-1] + 1;\n"
            "            else\n"
            "                dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);\n"
            "        }\n"
            "    }\n"
            "    return dp[m][n];\n"
            "}"
        ),
        "time_complexity": "O(m * n)",
        "space_complexity": "O(m * n), reducible to O(n)",
        "common_mistakes": [
            "Confusing subsequence (order matters, not contiguous) with substring (contiguous)",
            "Using 0-indexed text with 1-indexed dp (off by one)",
        ],
    },
    # =========================================================
    # TREE PATTERNS
    # =========================================================
    {
        "slug": "level-order-bfs",
        "name": "Level Order BFS (Tree)",
        "topic_slug": "trees",
        "difficulty_level": "easy",
        "explanation": (
            "Process tree nodes level by level using a queue. "
            "Start with root. At each step, dequeue a node, process it, "
            "and enqueue its children. Use a size variable to track levels."
        ),
        "when_to_use": "Find depth, process by level, right/left view, zigzag traversal, minimum depth.",
        "recognition_clues": "Level-by-level, shortest path in tree, 'each level', 'layer'.",
        "common_keywords": ["level", "BFS", "breadth", "layer", "depth", "right view", "left view"],
        "pseudocode": (
            "queue = deque([root])\n"
            "result = []\n"
            "while queue:\n"
            "    level_size = len(queue)\n"
            "    current_level = []\n"
            "    for _ in range(level_size):\n"
            "        node = queue.popleft()\n"
            "        current_level.append(node.val)\n"
            "        if node.left: queue.append(node.left)\n"
            "        if node.right: queue.append(node.right)\n"
            "    result.append(current_level)\n"
            "return result"
        ),
        "python_template": (
            "from collections import deque\n"
            "\n"
            "def level_order(root):\n"
            "    if not root:\n"
            "        return []\n"
            "    result = []\n"
            "    queue = deque([root])\n"
            "    while queue:\n"
            "        level = []\n"
            "        for _ in range(len(queue)):\n"
            "            node = queue.popleft()\n"
            "            level.append(node.val)\n"
            "            if node.left: queue.append(node.left)\n"
            "            if node.right: queue.append(node.right)\n"
            "        result.append(level)\n"
            "    return result"
        ),
        "java_template": (
            "public List<List<Integer>> levelOrder(TreeNode root) {\n"
            "    List<List<Integer>> result = new ArrayList<>();\n"
            "    if (root == null) return result;\n"
            "    Queue<TreeNode> queue = new LinkedList<>();\n"
            "    queue.offer(root);\n"
            "    while (!queue.isEmpty()) {\n"
            "        int size = queue.size();\n"
            "        List<Integer> level = new ArrayList<>();\n"
            "        for (int i = 0; i < size; i++) {\n"
            "            TreeNode node = queue.poll();\n"
            "            level.add(node.val);\n"
            "            if (node.left != null) queue.offer(node.left);\n"
            "            if (node.right != null) queue.offer(node.right);\n"
            "        }\n"
            "        result.add(level);\n"
            "    }\n"
            "    return result;\n"
            "}"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n) for the queue",
        "common_mistakes": [
            "Not capturing level size before the inner loop (queue size changes during loop)",
            "Forgetting null checks for children",
        ],
    },
    # =========================================================
    # GRAPH PATTERNS
    # =========================================================
    {
        "slug": "graph-bfs",
        "name": "Graph BFS",
        "topic_slug": "bfs",
        "difficulty_level": "medium",
        "explanation": (
            "Explore all nodes at distance 1 before distance 2, etc. "
            "Use a queue and a visited set. BFS guarantees shortest path in unweighted graphs."
        ),
        "when_to_use": "Shortest path in unweighted graph, minimum steps, word ladder, rotten oranges.",
        "recognition_clues": "Grid problems, 'minimum steps', 'shortest path', level-based expansion.",
        "common_keywords": ["shortest", "minimum steps", "grid", "BFS", "distance", "level"],
        "pseudocode": (
            "queue = deque([start])\n"
            "visited = {start}\n"
            "distance = 0\n"
            "while queue:\n"
            "    for _ in range(len(queue)):  # process level by level\n"
            "        node = queue.popleft()\n"
            "        if node == target: return distance\n"
            "        for neighbor in graph[node]:\n"
            "            if neighbor not in visited:\n"
            "                visited.add(neighbor)\n"
            "                queue.append(neighbor)\n"
            "    distance += 1\n"
            "return -1"
        ),
        "python_template": (
            "from collections import deque\n"
            "\n"
            "def bfs(graph, start, target):\n"
            "    queue = deque([start])\n"
            "    visited = {start}\n"
            "    distance = 0\n"
            "    \n"
            "    while queue:\n"
            "        for _ in range(len(queue)):\n"
            "            node = queue.popleft()\n"
            "            if node == target:\n"
            "                return distance\n"
            "            for neighbor in graph[node]:\n"
            "                if neighbor not in visited:\n"
            "                    visited.add(neighbor)\n"
            "                    queue.append(neighbor)\n"
            "        distance += 1\n"
            "    \n"
            "    return -1"
        ),
        "java_template": (
            "public int bfs(Map<Integer, List<Integer>> graph, int start, int target) {\n"
            "    Queue<Integer> queue = new LinkedList<>();\n"
            "    Set<Integer> visited = new HashSet<>();\n"
            "    queue.offer(start);\n"
            "    visited.add(start);\n"
            "    int distance = 0;\n"
            "    while (!queue.isEmpty()) {\n"
            "        int size = queue.size();\n"
            "        for (int i = 0; i < size; i++) {\n"
            "            int node = queue.poll();\n"
            "            if (node == target) return distance;\n"
            "            for (int neighbor : graph.getOrDefault(node, Collections.emptyList())) {\n"
            "                if (!visited.contains(neighbor)) {\n"
            "                    visited.add(neighbor);\n"
            "                    queue.offer(neighbor);\n"
            "                }\n"
            "            }\n"
            "        }\n"
            "        distance++;\n"
            "    }\n"
            "    return -1;\n"
            "}"
        ),
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V) for visited and queue",
        "common_mistakes": [
            "Adding to visited when dequeuing (too late — allows duplicate enqueues)",
            "Not tracking visited nodes (infinite loop in cyclic graphs)",
        ],
    },
    {
        "slug": "union-find-basic",
        "name": "Union Find with Path Compression",
        "topic_slug": "union-find",
        "difficulty_level": "medium",
        "explanation": (
            "Disjoint Set Union (DSU) efficiently answers: 'Are these two elements in the same group?' "
            "Path compression flattens trees during find(). "
            "Union by rank keeps trees shallow. Combined: nearly O(1) amortized per operation."
        ),
        "when_to_use": "Connected components, cycle detection in undirected graph, Kruskal's MST, number of provinces.",
        "recognition_clues": "'Connected components', 'are these connected?', 'merge groups', 'number of islands' variants.",
        "common_keywords": ["connected", "component", "union", "find", "group", "cycle", "MST"],
        "pseudocode": (
            "parent = list(range(n))\n"
            "rank = [0] * n\n"
            "\n"
            "def find(x):\n"
            "    if parent[x] != x:\n"
            "        parent[x] = find(parent[x])  # path compression\n"
            "    return parent[x]\n"
            "\n"
            "def union(x, y):\n"
            "    px, py = find(x), find(y)\n"
            "    if px == py: return False  # already same group\n"
            "    if rank[px] < rank[py]: px, py = py, px\n"
            "    parent[py] = px\n"
            "    if rank[px] == rank[py]: rank[px] += 1\n"
            "    return True"
        ),
        "python_template": (
            "class UnionFind:\n"
            "    def __init__(self, n):\n"
            "        self.parent = list(range(n))\n"
            "        self.rank = [0] * n\n"
            "        self.components = n\n"
            "    \n"
            "    def find(self, x):\n"
            "        if self.parent[x] != x:\n"
            "            self.parent[x] = self.find(self.parent[x])\n"
            "        return self.parent[x]\n"
            "    \n"
            "    def union(self, x, y):\n"
            "        px, py = self.find(x), self.find(y)\n"
            "        if px == py:\n"
            "            return False\n"
            "        if self.rank[px] < self.rank[py]:\n"
            "            px, py = py, px\n"
            "        self.parent[py] = px\n"
            "        if self.rank[px] == self.rank[py]:\n"
            "            self.rank[px] += 1\n"
            "        self.components -= 1\n"
            "        return True"
        ),
        "java_template": (
            "class UnionFind {\n"
            "    int[] parent, rank;\n"
            "    int components;\n"
            "    \n"
            "    UnionFind(int n) {\n"
            "        parent = new int[n];\n"
            "        rank = new int[n];\n"
            "        components = n;\n"
            "        for (int i = 0; i < n; i++) parent[i] = i;\n"
            "    }\n"
            "    \n"
            "    int find(int x) {\n"
            "        if (parent[x] != x) parent[x] = find(parent[x]);\n"
            "        return parent[x];\n"
            "    }\n"
            "    \n"
            "    boolean union(int x, int y) {\n"
            "        int px = find(x), py = find(y);\n"
            "        if (px == py) return false;\n"
            "        if (rank[px] < rank[py]) { int t = px; px = py; py = t; }\n"
            "        parent[py] = px;\n"
            "        if (rank[px] == rank[py]) rank[px]++;\n"
            "        components--;\n"
            "        return true;\n"
            "    }\n"
            "}"
        ),
        "time_complexity": "O(α(n)) per operation (inverse Ackermann — nearly O(1))",
        "space_complexity": "O(n)",
        "common_mistakes": [
            "Forgetting path compression (makes find O(n))",
            "Using union without rank (causes linear chains)",
            "Not checking if already in same set before union",
        ],
    },
    # =========================================================
    # PREFIX SUM
    # =========================================================
    {
        "slug": "prefix-sum-basic",
        "name": "Prefix Sum Array",
        "topic_slug": "prefix-sum",
        "difficulty_level": "easy",
        "explanation": (
            "Build a prefix array where prefix[i] = sum of nums[0..i-1]. "
            "Then any range sum [l, r] = prefix[r+1] - prefix[l]. "
            "Transforms range sum queries from O(n) to O(1) after O(n) preprocessing."
        ),
        "when_to_use": "Multiple range sum queries, subarray sum problems, 2D range queries.",
        "recognition_clues": "Sum of subarray, range sum queries, 'sum between indices'.",
        "common_keywords": ["prefix", "range sum", "subarray sum", "cumulative"],
        "pseudocode": (
            "prefix = [0] * (n + 1)\n"
            "for i in range(n):\n"
            "    prefix[i+1] = prefix[i] + nums[i]\n"
            "\n"
            "# Range sum query [l, r]\n"
            "def range_sum(l, r):\n"
            "    return prefix[r+1] - prefix[l]"
        ),
        "python_template": (
            "def build_prefix(nums):\n"
            "    n = len(nums)\n"
            "    prefix = [0] * (n + 1)\n"
            "    for i in range(n):\n"
            "        prefix[i + 1] = prefix[i] + nums[i]\n"
            "    return prefix\n"
            "\n"
            "def range_sum(prefix, l, r):\n"
            "    return prefix[r + 1] - prefix[l]"
        ),
        "java_template": (
            "int[] buildPrefix(int[] nums) {\n"
            "    int[] prefix = new int[nums.length + 1];\n"
            "    for (int i = 0; i < nums.length; i++)\n"
            "        prefix[i + 1] = prefix[i] + nums[i];\n"
            "    return prefix;\n"
            "}\n\n"
            "int rangeSum(int[] prefix, int l, int r) {\n"
            "    return prefix[r + 1] - prefix[l];\n"
            "}"
        ),
        "time_complexity": "O(n) build, O(1) query",
        "space_complexity": "O(n)",
        "common_mistakes": [
            "Off-by-one indexing (prefix has n+1 elements)",
            "Using prefix[r] - prefix[l] instead of prefix[r+1] - prefix[l]",
        ],
    },
    {
        "slug": "top-k-elements",
        "name": "Top K Elements (Heap)",
        "topic_slug": "heaps",
        "difficulty_level": "medium",
        "explanation": (
            "Use a min-heap of size k to track the k largest elements seen so far. "
            "If heap size exceeds k, remove the smallest. "
            "At the end, the heap contains the k largest elements."
        ),
        "when_to_use": "'K largest/smallest/most frequent elements'. Avoid sorting entire array: O(n log k) vs O(n log n).",
        "recognition_clues": "'Top k', 'k largest', 'k most frequent', 'k closest'.",
        "common_keywords": ["top k", "k largest", "k smallest", "frequent", "heap", "priority queue"],
        "pseudocode": (
            "heap = []  # min-heap of size k\n"
            "for num in nums:\n"
            "    heappush(heap, num)\n"
            "    if len(heap) > k:\n"
            "        heappop(heap)  # remove smallest\n"
            "return heap  # contains k largest"
        ),
        "python_template": (
            "import heapq\n"
            "\n"
            "def top_k_largest(nums, k):\n"
            "    heap = []  # min-heap\n"
            "    for num in nums:\n"
            "        heapq.heappush(heap, num)\n"
            "        if len(heap) > k:\n"
            "            heapq.heappop(heap)\n"
            "    return sorted(heap, reverse=True)  # or just return heap"
        ),
        "java_template": (
            "public int[] topKLargest(int[] nums, int k) {\n"
            "    PriorityQueue<Integer> heap = new PriorityQueue<>(); // min-heap\n"
            "    for (int num : nums) {\n"
            "        heap.offer(num);\n"
            "        if (heap.size() > k) heap.poll();\n"
            "    }\n"
            "    int[] result = new int[k];\n"
            "    for (int i = k - 1; i >= 0; i--)\n"
            "        result[i] = heap.poll();\n"
            "    return result;\n"
            "}"
        ),
        "time_complexity": "O(n log k)",
        "space_complexity": "O(k)",
        "common_mistakes": [
            "Using max-heap to find k largest (need min-heap to efficiently remove the non-top-k)",
            "Sorting entire array when O(n log k) is sufficient",
        ],
    },
    {
        "slug": "trie-insert-search",
        "name": "Trie Insert and Search",
        "topic_slug": "tries",
        "difficulty_level": "medium",
        "explanation": (
            "A Trie is a tree where each node represents a character. "
            "Paths from root to nodes represent prefixes. "
            "Insert: traverse characters, creating nodes as needed. "
            "Search: traverse characters, return false if any node missing."
        ),
        "when_to_use": "Prefix-based search, autocomplete, word existence check, longest common prefix.",
        "recognition_clues": "Multiple string operations on a dictionary, prefix queries, autocomplete.",
        "common_keywords": ["prefix", "trie", "insert", "search", "autocomplete", "word", "dictionary"],
        "pseudocode": (
            "class TrieNode:\n"
            "    children = {}\n"
            "    is_end = False\n"
            "\n"
            "INSERT(word):\n"
            "    node = root\n"
            "    for char in word:\n"
            "        if char not in node.children:\n"
            "            node.children[char] = TrieNode()\n"
            "        node = node.children[char]\n"
            "    node.is_end = True\n"
            "\n"
            "SEARCH(word):\n"
            "    node = root\n"
            "    for char in word:\n"
            "        if char not in node.children: return False\n"
            "        node = node.children[char]\n"
            "    return node.is_end"
        ),
        "python_template": (
            "class TrieNode:\n"
            "    def __init__(self):\n"
            "        self.children = {}\n"
            "        self.is_end = False\n"
            "\n"
            "class Trie:\n"
            "    def __init__(self):\n"
            "        self.root = TrieNode()\n"
            "    \n"
            "    def insert(self, word):\n"
            "        node = self.root\n"
            "        for char in word:\n"
            "            if char not in node.children:\n"
            "                node.children[char] = TrieNode()\n"
            "            node = node.children[char]\n"
            "        node.is_end = True\n"
            "    \n"
            "    def search(self, word):\n"
            "        node = self.root\n"
            "        for char in word:\n"
            "            if char not in node.children:\n"
            "                return False\n"
            "            node = node.children[char]\n"
            "        return node.is_end\n"
            "    \n"
            "    def starts_with(self, prefix):\n"
            "        node = self.root\n"
            "        for char in prefix:\n"
            "            if char not in node.children:\n"
            "                return False\n"
            "            node = node.children[char]\n"
            "        return True"
        ),
        "java_template": (
            "class Trie {\n"
            "    private TrieNode root = new TrieNode();\n"
            "    \n"
            "    static class TrieNode {\n"
            "        TrieNode[] children = new TrieNode[26];\n"
            "        boolean isEnd;\n"
            "    }\n"
            "    \n"
            "    public void insert(String word) {\n"
            "        TrieNode node = root;\n"
            "        for (char c : word.toCharArray()) {\n"
            "            int idx = c - 'a';\n"
            "            if (node.children[idx] == null)\n"
            "                node.children[idx] = new TrieNode();\n"
            "            node = node.children[idx];\n"
            "        }\n"
            "        node.isEnd = true;\n"
            "    }\n"
            "    \n"
            "    public boolean search(String word) {\n"
            "        TrieNode node = root;\n"
            "        for (char c : word.toCharArray()) {\n"
            "            int idx = c - 'a';\n"
            "            if (node.children[idx] == null) return false;\n"
            "            node = node.children[idx];\n"
            "        }\n"
            "        return node.isEnd;\n"
            "    }\n"
            "}"
        ),
        "time_complexity": "O(m) per insert/search where m = word length",
        "space_complexity": "O(ALPHABET_SIZE * m * n) for n words",
        "common_mistakes": [
            "Not marking is_end (search returns true for prefixes of inserted words)",
            "Using array of size 26 and forgetting uppercase letters or special chars",
        ],
    },
]
