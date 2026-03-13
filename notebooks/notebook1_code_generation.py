"""
================================================================================
ESWA 실험: n=5 코드 생성 파이프라인 (Notebook 1/3)
================================================================================
Anthropic API를 사용하여 47개 LeetCode 문제 × 2 페르소나 × 5 runs 생성

사용법 (Google Colab):
  1. 이 파일의 내용을 코랩 셀에 복사
  2. API 키 설정: ANTHROPIC_API_KEY
  3. 순서대로 실행

산출물:
  code_samples_n5/
    problem_001_lru_cache/
      vibecoder_run1.py ~ vibecoder_run5.py
      senior_run1.py ~ senior_run5.py
    problem_002_min_stack/
      ...
    problem_metadata.csv
================================================================================
"""

# ============================================================
# Cell 1: 환경 설정
# ============================================================
# !pip install anthropic

import os
import re
import csv
import json
import time
import logging
from pathlib import Path
from datetime import datetime

# API 키 설정 (코랩에서는 Secrets 또는 직접 입력)
# from google.colab import userdata
# ANTHROPIC_API_KEY = userdata.get('ANTHROPIC_API_KEY')
ANTHROPIC_API_KEY = "YOUR_API_KEY_HERE"  # ← 여기에 API 키 입력

# ============================================================
# Cell 2: 실험 설정
# ============================================================

# 모델 설정
MODEL = "claude-sonnet-4-20250514"  # Claude Sonnet 4
TEMPERATURE = 0.8  # 논문에 명시할 값 (다양성 확보 + 재현성)
MAX_TOKENS = 4096

# 반복 횟수
N_RUNS = 5

# 출력 디렉토리
OUTPUT_DIR = "code_samples_n5"

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"generation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# Cell 3: 47개 문제 메타데이터 (적대적 검증 후 확정)
# ============================================================

PROBLEMS = [
    # System Design (8문제: #5, #10 제외)
    {"num": 1, "leetcode_id": 146, "title": "LRU Cache", "difficulty": "Medium", "category": "System Design",
     "description": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. LRUCache(int capacity), int get(int key), void put(int key, int value)"},
    {"num": 2, "leetcode_id": 155, "title": "Min Stack", "difficulty": "Medium", "category": "System Design",
     "description": "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time."},
    {"num": 3, "leetcode_id": 208, "title": "Implement Trie", "difficulty": "Medium", "category": "System Design",
     "description": "Implement a trie with insert, search, and startsWith methods."},
    {"num": 4, "leetcode_id": 355, "title": "Design Twitter", "difficulty": "Medium", "category": "System Design",
     "description": "Design a simplified version of Twitter with postTweet, getNewsFeed, follow, unfollow."},
    {"num": 6, "leetcode_id": 981, "title": "Time Based Key-Value Store", "difficulty": "Medium", "category": "System Design",
     "description": "Design a time-based key-value data structure that can store/retrieve values at different timestamps."},
    {"num": 7, "leetcode_id": 295, "title": "Find Median from Data Stream", "difficulty": "Hard", "category": "System Design",
     "description": "Design a data structure that supports addNum and findMedian operations."},
    {"num": 8, "leetcode_id": 460, "title": "LFU Cache", "difficulty": "Hard", "category": "System Design",
     "description": "Design and implement a data structure for a Least Frequently Used (LFU) cache."},
    {"num": 9, "leetcode_id": 432, "title": "All O'one Data Structure", "difficulty": "Hard", "category": "System Design",
     "description": "Design a data structure with Inc(key), Dec(key), GetMaxKey(), GetMinKey() all in O(1)."},

    # Dynamic Programming (10문제)
    {"num": 11, "leetcode_id": 5, "title": "Longest Palindromic Substring", "difficulty": "Medium", "category": "Dynamic Programming",
     "description": "Given a string s, return the longest palindromic substring in s."},
    {"num": 12, "leetcode_id": 62, "title": "Unique Paths", "difficulty": "Medium", "category": "Dynamic Programming",
     "description": "A robot on an m x n grid can only move right or down. How many unique paths from top-left to bottom-right?"},
    {"num": 13, "leetcode_id": 91, "title": "Decode Ways", "difficulty": "Medium", "category": "Dynamic Programming",
     "description": "Given a string of digits, return the number of ways to decode it (A=1, B=2, ..., Z=26)."},
    {"num": 14, "leetcode_id": 139, "title": "Word Break", "difficulty": "Medium", "category": "Dynamic Programming",
     "description": "Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words."},
    {"num": 15, "leetcode_id": 198, "title": "House Robber", "difficulty": "Medium", "category": "Dynamic Programming",
     "description": "Given an integer array nums representing the amount of money of each house, return the maximum amount you can rob without robbing two adjacent houses."},
    {"num": 16, "leetcode_id": 300, "title": "Longest Increasing Subsequence", "difficulty": "Medium", "category": "Dynamic Programming",
     "description": "Given an integer array nums, return the length of the longest strictly increasing subsequence."},
    {"num": 17, "leetcode_id": 10, "title": "Regular Expression Matching", "difficulty": "Hard", "category": "Dynamic Programming",
     "description": "Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*'."},
    {"num": 18, "leetcode_id": 72, "title": "Edit Distance", "difficulty": "Hard", "category": "Dynamic Programming",
     "description": "Given two strings word1 and word2, return the minimum number of operations (insert, delete, replace) to convert word1 to word2."},
    {"num": 19, "leetcode_id": 312, "title": "Burst Balloons", "difficulty": "Hard", "category": "Dynamic Programming",
     "description": "Given n balloons with nums, burst them to collect maximum coins. nums[-1] = nums[n] = 1."},
    {"num": 20, "leetcode_id": 1235, "title": "Maximum Profit in Job Scheduling", "difficulty": "Hard", "category": "Dynamic Programming",
     "description": "Given n jobs with startTime, endTime, profit, find the maximum profit such that no two jobs overlap."},

    # Graph/Tree (9문제: #30 제외)
    {"num": 21, "leetcode_id": 102, "title": "Binary Tree Level Order Traversal", "difficulty": "Medium", "category": "Graph/Tree",
     "description": "Given the root of a binary tree, return the level order traversal of its nodes' values."},
    {"num": 22, "leetcode_id": 200, "title": "Number of Islands", "difficulty": "Medium", "category": "Graph/Tree",
     "description": "Given an m x n 2D binary grid, return the number of islands (connected '1's surrounded by '0's)."},
    {"num": 23, "leetcode_id": 207, "title": "Course Schedule", "difficulty": "Medium", "category": "Graph/Tree",
     "description": "There are numCourses courses with prerequisites. Determine if you can finish all courses."},
    {"num": 24, "leetcode_id": 236, "title": "Lowest Common Ancestor of a Binary Tree", "difficulty": "Medium", "category": "Graph/Tree",
     "description": "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes."},
    {"num": 25, "leetcode_id": 310, "title": "Minimum Height Trees", "difficulty": "Medium", "category": "Graph/Tree",
     "description": "Given a tree of n nodes, find all roots that minimize tree height (return a list of labels)."},
    {"num": 26, "leetcode_id": 994, "title": "Rotting Oranges", "difficulty": "Medium", "category": "Graph/Tree",
     "description": "Given a grid with fresh(1) and rotten(2) oranges, return minutes until no fresh orange remains, or -1."},
    {"num": 27, "leetcode_id": 124, "title": "Binary Tree Maximum Path Sum", "difficulty": "Hard", "category": "Graph/Tree",
     "description": "Given the root of a binary tree, return the maximum path sum. A path can start and end at any node."},
    {"num": 28, "leetcode_id": 297, "title": "Serialize and Deserialize Binary Tree", "difficulty": "Hard", "category": "Graph/Tree",
     "description": "Design an algorithm to serialize and deserialize a binary tree."},
    {"num": 29, "leetcode_id": 329, "title": "Longest Increasing Path in a Matrix", "difficulty": "Hard", "category": "Graph/Tree",
     "description": "Given an m x n integers matrix, return the length of the longest increasing path."},

    # String/Array (10문제)
    {"num": 31, "leetcode_id": 3, "title": "Longest Substring Without Repeating Characters", "difficulty": "Medium", "category": "String/Array",
     "description": "Given a string s, find the length of the longest substring without repeating characters."},
    {"num": 32, "leetcode_id": 15, "title": "3Sum", "difficulty": "Medium", "category": "String/Array",
     "description": "Given an integer array nums, return all triplets [nums[i], nums[j], nums[k]] such that i != j != k and nums[i] + nums[j] + nums[k] == 0."},
    {"num": 33, "leetcode_id": 49, "title": "Group Anagrams", "difficulty": "Medium", "category": "String/Array",
     "description": "Given an array of strings strs, group the anagrams together."},
    {"num": 34, "leetcode_id": 56, "title": "Merge Intervals", "difficulty": "Medium", "category": "String/Array",
     "description": "Given an array of intervals, merge all overlapping intervals."},
    {"num": 35, "leetcode_id": 238, "title": "Product of Array Except Self", "difficulty": "Medium", "category": "String/Array",
     "description": "Given an integer array nums, return an array answer such that answer[i] equals the product of all elements except nums[i]. No division allowed."},
    {"num": 36, "leetcode_id": 560, "title": "Subarray Sum Equals K", "difficulty": "Medium", "category": "String/Array",
     "description": "Given an integer array nums and an integer k, return the total number of subarrays whose sum equals k."},
    {"num": 37, "leetcode_id": 4, "title": "Median of Two Sorted Arrays", "difficulty": "Hard", "category": "String/Array",
     "description": "Given two sorted arrays nums1 and nums2, return the median of the two sorted arrays. O(log(m+n)) required."},
    {"num": 38, "leetcode_id": 41, "title": "First Missing Positive", "difficulty": "Hard", "category": "String/Array",
     "description": "Given an unsorted integer array nums, return the smallest missing positive integer. O(n) time and O(1) auxiliary space."},
    {"num": 39, "leetcode_id": 76, "title": "Minimum Window Substring", "difficulty": "Hard", "category": "String/Array",
     "description": "Given strings s and t, return the minimum window substring of s such that every character in t is included. O(m+n) required."},
    {"num": 40, "leetcode_id": 239, "title": "Sliding Window Maximum", "difficulty": "Hard", "category": "String/Array",
     "description": "Given an array nums and sliding window size k, return the max value in each window position."},

    # Backtracking (10문제)
    {"num": 41, "leetcode_id": 17, "title": "Letter Combinations of a Phone Number", "difficulty": "Medium", "category": "Backtracking",
     "description": "Given a string containing digits from 2-9, return all possible letter combinations."},
    {"num": 42, "leetcode_id": 22, "title": "Generate Parentheses", "difficulty": "Medium", "category": "Backtracking",
     "description": "Given n pairs of parentheses, generate all combinations of well-formed parentheses."},
    {"num": 43, "leetcode_id": 39, "title": "Combination Sum", "difficulty": "Medium", "category": "Backtracking",
     "description": "Given an array of distinct integers candidates and a target, return all unique combinations that sum to target. Same number may be used unlimited times."},
    {"num": 44, "leetcode_id": 46, "title": "Permutations", "difficulty": "Medium", "category": "Backtracking",
     "description": "Given an array nums of distinct integers, return all possible permutations."},
    {"num": 45, "leetcode_id": 78, "title": "Subsets", "difficulty": "Medium", "category": "Backtracking",
     "description": "Given an integer array nums of unique elements, return all possible subsets (the power set)."},
    {"num": 46, "leetcode_id": 79, "title": "Word Search", "difficulty": "Medium", "category": "Backtracking",
     "description": "Given an m x n board of characters and a string word, return true if word exists in the grid (adjacent cells, no reuse)."},
    {"num": 47, "leetcode_id": 37, "title": "Sudoku Solver", "difficulty": "Hard", "category": "Backtracking",
     "description": "Write a program to solve a Sudoku puzzle by filling the empty cells (represented by '.')."},
    {"num": 48, "leetcode_id": 51, "title": "N-Queens", "difficulty": "Hard", "category": "Backtracking",
     "description": "Place n queens on an n x n chessboard such that no two queens attack each other. Return all distinct solutions."},
    {"num": 49, "leetcode_id": 212, "title": "Word Search II", "difficulty": "Hard", "category": "Backtracking",
     "description": "Given an m x n board of characters and a list of strings words, return all words on the board. Use Trie for efficiency."},
    {"num": 50, "leetcode_id": 301, "title": "Remove Invalid Parentheses", "difficulty": "Hard", "category": "Backtracking",
     "description": "Given a string s with parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid. Return all possible results."},
]

assert len(PROBLEMS) == 47, f"Expected 47 problems, got {len(PROBLEMS)}"
logger.info(f"총 {len(PROBLEMS)}개 문제 로드 완료")

# ============================================================
# Cell 4: 페르소나 프롬프트 정의
# ============================================================

SYSTEM_PROMPT = """You are a code generation assistant for an academic experiment. You will generate Python code for LeetCode problems in a specific coding style (persona). Follow the persona instructions EXACTLY. Output ONLY the Python code — no explanations, no markdown fences, no comments about the code. Just pure Python code that could be saved directly as a .py file."""

VIBECODER_PERSONA = """Generate a Python solution for the following LeetCode problem in the "Vibecoder" style:

VIBECODER STYLE RULES (follow ALL strictly):
- Variable names: 1-2 characters only (x, n, d, res, ans, tmp, etc.)
- Comments: NONE
- Docstrings: NONE
- Type Hints: NONE
- Style: Compress into fewest lines possible, use list comprehensions aggressively, use magic numbers
- Error handling: NONE
- Class design: Cram all logic into minimal methods (God Class pattern)
- Import only what's needed, keep imports minimal

CRITICAL RULES:
1. The code must be functionally correct (would pass LeetCode tests)
2. Use the exact LeetCode class/method signatures
3. Python 3 only, standard library only (collections, heapq, functools OK)
4. Output ONLY Python code — no markdown, no explanations

Problem: {title} (LeetCode #{leetcode_id})
{description}"""

SENIOR_PERSONA = """Generate a Python solution for the following LeetCode problem in the "Senior Developer" style:

SENIOR DEVELOPER STYLE RULES (follow ALL strictly):
- Variable names: Meaningful full names (current_node, max_profit, visited_set, etc.)
- Comments: Inline comments on key logic
- Docstrings: Google Style docstring on ALL functions and classes
- Type Hints: On ALL parameters and return types
- Style: Separate functions, define constants, prioritize readability
- Error handling: Appropriate exception handling and edge case handling
- Class design: Follow SRP, separate methods, clear interfaces

CRITICAL RULES:
1. The code must be functionally correct (would pass LeetCode tests)
2. Use the exact LeetCode class/method signatures
3. Python 3 only, standard library only (collections, heapq, functools OK)
4. Output ONLY Python code — no markdown, no explanations

Problem: {title} (LeetCode #{leetcode_id})
{description}"""


# ============================================================
# Cell 5: API 호출 함수
# ============================================================

def generate_code(problem, persona_type, run_num, client):
    """
    단일 문제 + 페르소나에 대해 코드 생성.

    Args:
        problem: 문제 딕셔너리
        persona_type: "vibecoder" 또는 "senior"
        run_num: 실행 번호 (1-5)
        client: Anthropic 클라이언트

    Returns:
        생성된 코드 문자열 또는 None (실패 시)
    """
    template = VIBECODER_PERSONA if persona_type == "vibecoder" else SENIOR_PERSONA
    user_prompt = template.format(
        title=problem["title"],
        leetcode_id=problem["leetcode_id"],
        description=problem["description"]
    )

    for attempt in range(3):  # 최대 3회 재시도
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}]
            )

            code = response.content[0].text

            # 마크다운 코드 펜스 제거 (만약 포함되었다면)
            code = re.sub(r'^```python\s*\n?', '', code, flags=re.MULTILINE)
            code = re.sub(r'^```\s*$', '', code, flags=re.MULTILINE)
            code = code.strip()

            # 기본 유효성 검사
            if len(code) < 20:
                logger.warning(f"  코드가 너무 짧음 ({len(code)}자), 재시도 {attempt+1}/3")
                continue

            if "def " not in code and "class " not in code:
                logger.warning(f"  함수/클래스 정의 없음, 재시도 {attempt+1}/3")
                continue

            return code

        except Exception as e:
            logger.error(f"  API 오류: {e}")
            if attempt < 2:
                wait_time = 30 * (attempt + 1)
                logger.info(f"  {wait_time}초 대기 후 재시도...")
                time.sleep(wait_time)

    return None


# ============================================================
# Cell 6: 파일 저장 함수
# ============================================================

def save_code(problem, persona_type, run_num, code):
    """코드를 파일로 저장"""
    # 디렉토리명 생성
    safe_title = re.sub(r'[^a-z0-9]+', '_', problem["title"].lower()).strip('_')
    dir_name = f"problem_{problem['num']:03d}_{safe_title}"
    dir_path = os.path.join(OUTPUT_DIR, dir_name)
    os.makedirs(dir_path, exist_ok=True)

    # 파일명: {persona}_run{N}.py
    filename = f"{persona_type}_run{run_num}.py"
    filepath = os.path.join(dir_path, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    return filepath


def save_metadata():
    """문제 메타데이터를 CSV로 저장"""
    meta_path = os.path.join(OUTPUT_DIR, "problem_metadata.csv")
    with open(meta_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["problem_num", "leetcode_id", "title", "difficulty", "category"])
        writer.writeheader()
        for p in PROBLEMS:
            writer.writerow({
                "problem_num": p["num"],
                "leetcode_id": p["leetcode_id"],
                "title": p["title"],
                "difficulty": p["difficulty"],
                "category": p["category"],
            })
    logger.info(f"메타데이터 저장: {meta_path}")


# ============================================================
# Cell 7: 진행 상황 추적 (중단/재개 지원)
# ============================================================

PROGRESS_FILE = "generation_progress.json"

def load_progress():
    """이전 진행 상황 로드"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"completed": []}

def save_progress(progress):
    """진행 상황 저장"""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def is_completed(progress, problem_num, persona, run_num):
    """해당 작업이 이미 완료되었는지 확인"""
    key = f"{problem_num}_{persona}_run{run_num}"
    return key in progress["completed"]

def mark_completed(progress, problem_num, persona, run_num):
    """작업 완료 표시"""
    key = f"{problem_num}_{persona}_run{run_num}"
    if key not in progress["completed"]:
        progress["completed"].append(key)
    save_progress(progress)


# ============================================================
# Cell 8: 메인 생성 루프
# ============================================================

def main():
    """전체 코드 생성 파이프라인 실행"""
    import anthropic  # pip install anthropic

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_metadata()

    progress = load_progress()
    total_tasks = len(PROBLEMS) * 2 * N_RUNS  # 47 × 2 × 5 = 470
    completed_count = len(progress["completed"])

    logger.info(f"=" * 60)
    logger.info(f"ESWA n=5 코드 생성 시작")
    logger.info(f"  모델: {MODEL}")
    logger.info(f"  Temperature: {TEMPERATURE}")
    logger.info(f"  문제 수: {len(PROBLEMS)}")
    logger.info(f"  Runs: {N_RUNS}")
    logger.info(f"  총 작업: {total_tasks}")
    logger.info(f"  이미 완료: {completed_count}")
    logger.info(f"  남은 작업: {total_tasks - completed_count}")
    logger.info(f"=" * 60)

    success_count = 0
    fail_count = 0
    start_time = time.time()

    for run_num in range(1, N_RUNS + 1):
        logger.info(f"\n{'='*40} Run {run_num}/{N_RUNS} {'='*40}")

        for problem in PROBLEMS:
            for persona in ["vibecoder", "senior"]:
                # 이미 완료된 작업 건너뛰기
                if is_completed(progress, problem["num"], persona, run_num):
                    continue

                task_id = f"P{problem['num']:03d}_{persona}_run{run_num}"
                current = completed_count + success_count + fail_count + 1
                logger.info(f"[{current}/{total_tasks}] {task_id}: {problem['title']}")

                code = generate_code(problem, persona, run_num, client)

                if code:
                    filepath = save_code(problem, persona, run_num, code)
                    mark_completed(progress, problem["num"], persona, run_num)
                    success_count += 1
                    logger.info(f"  ✅ 저장: {filepath} ({len(code)}자)")
                else:
                    fail_count += 1
                    logger.error(f"  ❌ 실패: {task_id}")

                # Rate limiting: 요청 간 간격
                time.sleep(1.0)  # 1초 대기 (필요시 조정)

        logger.info(f"Run {run_num} 완료: 성공={success_count}, 실패={fail_count}")

    elapsed = time.time() - start_time
    logger.info(f"\n{'='*60}")
    logger.info(f"전체 생성 완료!")
    logger.info(f"  성공: {success_count}")
    logger.info(f"  실패: {fail_count}")
    logger.info(f"  소요 시간: {elapsed/60:.1f}분")
    logger.info(f"  출력 디렉토리: {OUTPUT_DIR}")
    logger.info(f"{'='*60}")

    if fail_count > 0:
        logger.warning(f"\n⚠️ {fail_count}개 실패 건이 있습니다.")
        logger.warning(f"   이 스크립트를 다시 실행하면 실패 건만 재시도합니다.")


if __name__ == "__main__":
    main()


# ============================================================
# Cell 9: 생성 결과 검증
# ============================================================

def verify_generation():
    """생성된 파일 구조 검증"""
    expected_files = len(PROBLEMS) * 2 * N_RUNS  # 470개
    actual_files = 0
    missing = []

    for problem in PROBLEMS:
        safe_title = re.sub(r'[^a-z0-9]+', '_', problem["title"].lower()).strip('_')
        dir_name = f"problem_{problem['num']:03d}_{safe_title}"
        dir_path = os.path.join(OUTPUT_DIR, dir_name)

        for persona in ["vibecoder", "senior"]:
            for run in range(1, N_RUNS + 1):
                filepath = os.path.join(dir_path, f"{persona}_run{run}.py")
                if os.path.exists(filepath):
                    actual_files += 1
                    # 파일 크기 검사
                    size = os.path.getsize(filepath)
                    if size < 50:
                        logger.warning(f"  ⚠️ 파일이 너무 작음: {filepath} ({size} bytes)")
                else:
                    missing.append(filepath)

    logger.info(f"\n📊 생성 검증 결과:")
    logger.info(f"  예상: {expected_files}개")
    logger.info(f"  실제: {actual_files}개")
    logger.info(f"  누락: {len(missing)}개")

    if missing:
        logger.warning(f"\n누락 파일 목록 (처음 10개):")
        for f in missing[:10]:
            logger.warning(f"  {f}")

    return actual_files == expected_files

# verify_generation()  # 생성 완료 후 실행
