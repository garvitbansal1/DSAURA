from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
from datetime import datetime

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

# Comprehensive DSA Pattern Recognition Question Bank
ASSESSMENT_QUESTIONS = [
    {
        "id": "q1",
        "topic": "Stacks",
        "difficulty": "medium",
        "title": "Stock Span & Temperatures",
        "scenario": (
            "Given an array of integers representing daily temperatures, you need to return an array "
            "such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. "
            "If there is no future day for which this is possible, keep answer[i] == 0."
        ),
        "question": "Which algorithmic pattern provides the optimal O(n) time solution?",
        "options": [
            {"id": "a", "text": "Two Pointers starting at both ends"},
            {"id": "b", "text": "Monotonic Decreasing Stack (Next Greater Element)", "is_correct": True},
            {"id": "c", "text": "Sliding Window with dynamic sizing"},
            {"id": "d", "text": "Breadth-First Search (BFS)"}
        ],
        "explanation": (
            "Because we are looking for the next greater element in an array, a Monotonic Decreasing Stack "
            "stores indices whose temperatures haven't found a warmer day yet. It resolves each element in O(1) amortized time."
        ),
        "target_pattern": "next-greater-element",
        "target_topic": "monotonic-stack"
    },
    {
        "id": "q2",
        "topic": "Two Pointers & Sliding Window",
        "difficulty": "medium",
        "title": "Subarray Sum Equals K vs Longest Subarray",
        "scenario": (
            "Given an array containing both positive and negative integers, you need to find the length of the "
            "longest subarray that sums to exactly K."
        ),
        "question": "Why does a standard dynamic Sliding Window fail here, and what pattern should be used instead?",
        "options": [
            {"id": "a", "text": "Sliding window works fine; just shrink when sum exceeds K."},
            {"id": "b", "text": "Prefix Sum combined with a Hash Map storing earliest indices.", "is_correct": True},
            {"id": "c", "text": "Binary Search on Answer."},
            {"id": "d", "text": "Fast & Slow Pointers (Floyd's Cycle Detection)."}
        ],
        "explanation": (
            "Standard two-pointer sliding window relies on monotonicity (expanding increases sum, shrinking decreases sum). "
            "Negative numbers break this monotonic property! Hence, Prefix Sum with a Hash Map is required to find subarray sum in O(n)."
        ),
        "target_pattern": "prefix-sum-basic",
        "target_topic": "prefix-sum"
    },
    {
        "id": "q3",
        "topic": "Binary Search",
        "difficulty": "hard",
        "title": "Capacity Allocation & Splitting",
        "scenario": (
            "You have weights of packages on a conveyor belt and D days to ship them all. "
            "Packages must be shipped in order without reordering. You must find the least weight capacity of the ship."
        ),
        "question": "What key pattern should be recognized to solve this problem?",
        "options": [
            {"id": "a", "text": "0/1 Knapsack Dynamic Programming"},
            {"id": "b", "text": "Greedy Interval Scheduling"},
            {"id": "c", "text": "Binary Search on Answer (Feasibility Condition)", "is_correct": True},
            {"id": "d", "text": "Minimum Spanning Tree (Kruskal's)"}
        ],
        "explanation": (
            "The answer (capacity) lies within a bounded search space: min is max(weights), max is sum(weights). "
            "If capacity C is sufficient to ship within D days, any capacity > C is also sufficient (monotonic feasibility). "
            "This is the hallmark of 'Binary Search on Answer'."
        ),
        "target_pattern": "binary-search-on-answer",
        "target_topic": "binary-search"
    },
    {
        "id": "q4",
        "topic": "Graphs",
        "difficulty": "medium",
        "title": "Course Prerequisites",
        "scenario": (
            "There are total numCourses you have to take, labeled from 0 to numCourses - 1. "
            "You are given prerequisites pairs [a, b] indicating you must take course b before course a."
        ),
        "question": "Which algorithm determines whether it is possible to finish all courses without a deadlock?",
        "options": [
            {"id": "a", "text": "Dijkstra's Algorithm"},
            {"id": "b", "text": "Topological Sort / Cycle Detection in Directed Graph (Kahn's or DFS)", "is_correct": True},
            {"id": "c", "text": "Union-Find with Path Compression only"},
            {"id": "d", "text": "Bellman-Ford Algorithm"}
        ],
        "explanation": (
            "Course prerequisites form a directed graph. Finishing all courses is possible if and only if the directed "
            "graph has no cycles (is a Directed Acyclic Graph - DAG). Kahn's BFS with indegrees or 3-color DFS detects cycles and gives topological order."
        ),
        "target_pattern": "topological-sort-kahns",
        "target_topic": "topological-sorting"
    },
    {
        "id": "q5",
        "topic": "Dynamic Programming",
        "difficulty": "medium",
        "title": "Partition Equal Subset Sum",
        "scenario": (
            "Given an integer array nums, return true if you can partition the array into two subsets such that "
            "the sum of the elements in both subsets is equal."
        ),
        "question": "This problem is a direct variation of which classic pattern?",
        "options": [
            {"id": "a", "text": "0/1 Knapsack where target weight is sum(nums) / 2", "is_correct": True},
            {"id": "b", "text": "Longest Increasing Subsequence (LIS)"},
            {"id": "c", "text": "Two Pointers Meet-in-the-Middle"},
            {"id": "d", "text": "Interval Overlap Detection"}
        ],
        "explanation": (
            "Two equal subsets means each subset must sum to total_sum / 2. If total_sum is odd, it's impossible. "
            "Otherwise, it reduces to whether a subset with sum equal to target exists, which is exactly the 0/1 Knapsack problem."
        ),
        "target_pattern": "knapsack-01",
        "target_topic": "dynamic-programming"
    },
    {
        "id": "q6",
        "topic": "Sliding Window",
        "difficulty": "medium",
        "title": "Longest Substring with At Most K Distinct Characters",
        "scenario": (
            "Given a string s and an integer k, find the length of the longest substring that contains at most k distinct characters."
        ),
        "question": "Which window contraction strategy correctly maintains the optimal window?",
        "options": [
            {"id": "a", "text": "Reset left pointer to right pointer whenever unique characters exceed k."},
            {"id": "b", "text": "Expand right pointer, update frequency map; while map size > k, decrement frequency of left char and increment left pointer.", "is_correct": True},
            {"id": "c", "text": "Sort the string first and apply Two Pointers."},
            {"id": "d", "text": "Store all substrings in a Trie."}
        ],
        "explanation": (
            "Variable-size sliding window with frequency map: Expand right by 1, if unique chars exceed k, shrink left "
            "until unique chars <= k. Each element is added and removed at most once: O(n) time."
        ),
        "target_pattern": "variable-sliding-window",
        "target_topic": "sliding-window"
    }
]


class SubmitAnswerRequest(BaseModel):
    question_id: str
    selected_option_id: str


class AssessmentResult(BaseModel):
    score: int
    total_questions: int
    percentage: float
    feedback: str
    breakdown: List[Dict[str, Any]]


@router.get("/questions")
def get_assessment_questions(current_user: User = Depends(get_current_user)):
    """Return assessment questions without exposing is_correct answer upfront."""
    sanitized = []
    for q in ASSESSMENT_QUESTIONS:
        sanitized.append({
            "id": q["id"],
            "topic": q["topic"],
            "difficulty": q["difficulty"],
            "title": q["title"],
            "scenario": q["scenario"],
            "question": q["question"],
            "options": [{"id": opt["id"], "text": opt["text"]} for opt in q["options"]]
        })
    return {
        "title": "DSA Pattern Recognition & Architectural Assessment",
        "total_questions": len(sanitized),
        "questions": sanitized
    }


class SubmissionPayload(BaseModel):
    answers: Dict[str, str]  # question_id -> selected_option_id


@router.post("/evaluate", response_model=AssessmentResult)
def evaluate_assessment(
    payload: SubmissionPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Evaluates pattern recognition quiz answers.
    Generates explainable feedback on pattern diagnostics.
    """
    answers = payload.answers
    correct_count = 0
    breakdown = []

    for q in ASSESSMENT_QUESTIONS:
        selected_id = answers.get(q["id"])
        correct_opt = next((opt for opt in q["options"] if opt.get("is_correct")), None)
        selected_opt = next((opt for opt in q["options"] if opt["id"] == selected_id), None)

        is_correct = bool(correct_opt and selected_id == correct_opt["id"])
        if is_correct:
            correct_count += 1

        breakdown.append({
            "question_id": q["id"],
            "title": q["title"],
            "topic": q["topic"],
            "is_correct": is_correct,
            "selected_option": selected_opt["text"] if selected_opt else "Unanswered",
            "correct_option": correct_opt["text"] if correct_opt else "",
            "explanation": q["explanation"],
            "target_pattern": q["target_pattern"]
        })

    pct = round((correct_count / len(ASSESSMENT_QUESTIONS)) * 100, 1)

    if pct >= 80:
        feedback = "Outstanding pattern recognition! You demonstrate strong algorithmic architectural intuition."
    elif pct >= 50:
        feedback = "Good foundation. You correctly identified standard patterns, but tricky edge cases (like negatives in sliding window) need practice."
    else:
        feedback = "Pattern recognition needs strengthening. Focus on the 'When to Use' and 'Recognition Clues' in the Pattern Library."

    return AssessmentResult(
        score=correct_count,
        total_questions=len(ASSESSMENT_QUESTIONS),
        percentage=pct,
        feedback=feedback,
        breakdown=breakdown
    )
