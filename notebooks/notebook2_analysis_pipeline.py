"""
================================================================================
ESWA 실험: n=5 정적 분석 파이프라인 (Notebook 2/3)
================================================================================
code_samples_n5/ → analysis_results_n5.csv

기존 analyze_pipeline.py를 n=5 구조로 확장:
  - 각 문제 × 페르소나 × run별 개별 분석
  - median 기반 대표값 산출
  - 분석 결과를 두 가지 형태로 저장:
    1) analysis_results_n5_raw.csv: 전체 raw 데이터 (47 × 2 × 5 = 470행)
    2) analysis_results_n5_median.csv: median 대표값 (47 × 2 = 94행)

사용법 (Colab):
  1. !pip install radon pylint bandit
  2. Notebook 1 실행 완료 후 이 스크립트 실행
  3. !python notebook2_analysis_pipeline.py
================================================================================
"""

import os
import csv
import json
import subprocess
import re
import math
import statistics
from pathlib import Path
from collections import defaultdict

# ============================================================
# Cell 1: 설정
# ============================================================
CODE_DIR = "code_samples_n5"
N_RUNS = 5
OUTPUT_RAW = "analysis_results_n5_raw.csv"
OUTPUT_MEDIAN = "analysis_results_n5_median.csv"

# ============================================================
# Cell 2: 분석 함수들 (기존 파이프라인에서 가져옴)
# ============================================================

def get_cyclomatic_complexity(filepath):
    """radon cc로 Cyclomatic Complexity 추출"""
    try:
        result = subprocess.run(
            ["radon", "cc", filepath, "-j"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return {"cc_average": 0, "cc_max": 0, "cc_total": 0, "cc_blocks": 0}

        data = json.loads(result.stdout)
        blocks = data.get(filepath, [])
        if not blocks:
            return {"cc_average": 0, "cc_max": 0, "cc_total": 0, "cc_blocks": 0}

        complexities = [b["complexity"] for b in blocks]
        return {
            "cc_average": sum(complexities) / len(complexities),
            "cc_max": max(complexities),
            "cc_total": sum(complexities),
            "cc_blocks": len(complexities),
        }
    except Exception as e:
        print(f"    CC 오류 ({filepath}): {e}")
        return {"cc_average": 0, "cc_max": 0, "cc_total": 0, "cc_blocks": 0}


def get_maintainability_index(filepath):
    """radon mi로 Maintainability Index 추출"""
    try:
        result = subprocess.run(
            ["radon", "mi", filepath, "-j"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return {"mi_score": 0, "mi_rank": ""}

        data = json.loads(result.stdout)
        info = data.get(filepath, {})
        if isinstance(info, dict):
            return {"mi_score": info.get("mi", 0), "mi_rank": info.get("rank", "")}
        return {"mi_score": 0, "mi_rank": ""}
    except Exception as e:
        print(f"    MI 오류 ({filepath}): {e}")
        return {"mi_score": 0, "mi_rank": ""}


def get_halstead_metrics(filepath):
    """radon hal로 Halstead 메트릭 추출"""
    defaults = {
        "hal_vocabulary": 0, "hal_length": 0, "hal_volume": 0,
        "hal_difficulty": 0, "hal_effort": 0, "hal_time": 0, "hal_bugs": 0
    }
    try:
        result = subprocess.run(
            ["radon", "hal", filepath, "-j"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return defaults

        data = json.loads(result.stdout)
        file_data = data.get(filepath, {})
        total = file_data.get("total", [])

        if not total:
            functions = file_data.get("functions", [])
            if not functions:
                return defaults
            all_h1 = sum(f.get("h1", 0) for f in functions)
            all_h2 = sum(f.get("h2", 0) for f in functions)
            all_N1 = sum(f.get("N1", 0) for f in functions)
            all_N2 = sum(f.get("N2", 0) for f in functions)
            vocabulary = all_h1 + all_h2
            length = all_N1 + all_N2
            if vocabulary > 0 and length > 0:
                volume = length * math.log2(vocabulary) if vocabulary > 1 else 0
                difficulty = (all_h1 / 2) * (all_N2 / all_h2) if all_h2 > 0 else 0
                effort = volume * difficulty
                return {
                    "hal_vocabulary": vocabulary, "hal_length": length,
                    "hal_volume": volume, "hal_difficulty": difficulty,
                    "hal_effort": effort, "hal_time": effort / 18,
                    "hal_bugs": volume / 3000
                }
            return defaults

        if isinstance(total, list):
            t = total[0] if total else {}
        elif isinstance(total, dict):
            t = total
        else:
            return defaults

        return {
            "hal_vocabulary": t.get("vocabulary", t.get("h1", 0) + t.get("h2", 0)),
            "hal_length": t.get("length", t.get("N1", 0) + t.get("N2", 0)),
            "hal_volume": t.get("volume", 0),
            "hal_difficulty": t.get("difficulty", 0),
            "hal_effort": t.get("effort", 0),
            "hal_time": t.get("time", 0),
            "hal_bugs": t.get("bugs", 0),
        }
    except Exception as e:
        print(f"    HAL 오류 ({filepath}): {e}")
        return defaults


def get_pylint_score(filepath):
    """Pylint 실행하여 점수와 메시지 추출"""
    defaults = {
        "pylint_score": 0, "pylint_convention": 0, "pylint_refactor": 0,
        "pylint_warning": 0, "pylint_error": 0, "pylint_total_issues": 0
    }
    try:
        # Step 1: 점수 추출
        result = subprocess.run(
            ["pylint", filepath,
             "--disable=C0114,C0115,C0116",  # docstring 경고 비활성화
             "--max-line-length=120",
             "--score=y"],
            capture_output=True, text=True, timeout=60
        )
        score = 0.0
        score_match = re.search(r'rated at (-?[\d.]+)/10', result.stdout)
        if score_match:
            score = float(score_match.group(1))

        # Step 2: 메시지 카운트 (JSON)
        result_json = subprocess.run(
            ["pylint", filepath,
             "--disable=C0114,C0115,C0116",
             "--max-line-length=120",
             "--output-format=json"],
            capture_output=True, text=True, timeout=60
        )
        counts = {"C": 0, "R": 0, "W": 0, "E": 0}
        try:
            messages = json.loads(result_json.stdout) if result_json.stdout.strip() else []
            for msg in messages:
                msg_type = msg.get("type", "")
                if msg_type == "convention": counts["C"] += 1
                elif msg_type == "refactor": counts["R"] += 1
                elif msg_type == "warning": counts["W"] += 1
                elif msg_type == "error": counts["E"] += 1
        except json.JSONDecodeError:
            pass

        total = sum(counts.values())
        return {
            "pylint_score": score,
            "pylint_convention": counts["C"], "pylint_refactor": counts["R"],
            "pylint_warning": counts["W"], "pylint_error": counts["E"],
            "pylint_total_issues": total,
        }
    except Exception as e:
        print(f"    Pylint 오류 ({filepath}): {e}")
        return defaults


def get_bandit_results(filepath):
    """Bandit 실행하여 보안 취약점 추출"""
    defaults = {
        "bandit_high": 0, "bandit_medium": 0, "bandit_low": 0,
        "bandit_total": 0, "bandit_confidence_high": 0
    }
    try:
        result = subprocess.run(
            ["bandit", filepath, "-f", "json", "-q"],
            capture_output=True, text=True, timeout=30
        )
        if not result.stdout.strip():
            return defaults

        data = json.loads(result.stdout)
        results_list = data.get("results", [])
        counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        confidence_high = 0

        for issue in results_list:
            severity = issue.get("issue_severity", "").upper()
            confidence = issue.get("issue_confidence", "").upper()
            if severity in counts: counts[severity] += 1
            if confidence == "HIGH": confidence_high += 1

        total = sum(counts.values())
        return {
            "bandit_high": counts["HIGH"], "bandit_medium": counts["MEDIUM"],
            "bandit_low": counts["LOW"], "bandit_total": total,
            "bandit_confidence_high": confidence_high,
        }
    except Exception as e:
        print(f"    Bandit 오류 ({filepath}): {e}")
        return defaults


def get_code_metadata(filepath):
    """코드 파일에서 기본 메타정보 추출"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")

        loc = len([l for l in lines if l.strip()])
        blank = len([l for l in lines if not l.strip()])
        comments = len([l for l in lines if l.strip().startswith("#")])
        has_docstring = '"""' in content or "'''" in content
        has_type_hints = "->" in content and "def " in content
        type_hint_in_params = bool(re.search(r'def \w+\(self,?\s*\w+\s*:', content))

        return {
            "lines_of_code": loc, "blank_lines": blank, "comment_lines": comments,
            "has_docstring": has_docstring,
            "has_type_hints": has_type_hints and type_hint_in_params,
        }
    except Exception as e:
        print(f"    메타 오류 ({filepath}): {e}")
        return {
            "lines_of_code": 0, "blank_lines": 0, "comment_lines": 0,
            "has_docstring": False, "has_type_hints": False,
        }


def analyze_file(filepath):
    """단일 파일 전체 분석"""
    result = {}
    result.update(get_cyclomatic_complexity(filepath))
    result.update(get_maintainability_index(filepath))
    result.update(get_halstead_metrics(filepath))
    result.update(get_pylint_score(filepath))
    result.update(get_bandit_results(filepath))
    result.update(get_code_metadata(filepath))
    return result


# ============================================================
# Cell 3: 메타데이터 로드
# ============================================================

def load_metadata():
    """problem_metadata.csv에서 문제 정보 로드"""
    meta_path = os.path.join(CODE_DIR, "problem_metadata.csv")
    metadata = {}
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                metadata[int(row["problem_num"])] = row
    else:
        print(f"⚠️ {meta_path} 없음 — Notebook 1을 먼저 실행하세요")
    return metadata


# ============================================================
# Cell 4: 메인 분석 루프 (n=5)
# ============================================================

def main():
    print(f"{'='*60}")
    print("📊 ESWA n=5 정적 분석 파이프라인")
    print(f"{'='*60}")

    metadata = load_metadata()
    print(f"메타데이터: {len(metadata)}개 문제")

    # 문제 디렉토리 탐색
    problem_dirs = sorted([
        d for d in os.listdir(CODE_DIR)
        if d.startswith("problem_") and os.path.isdir(os.path.join(CODE_DIR, d))
    ])
    print(f"디렉토리: {len(problem_dirs)}개 발견")

    # 도구 테스트
    test_dir = os.path.join(CODE_DIR, problem_dirs[0])
    test_files = [f for f in os.listdir(test_dir) if f.endswith('.py')]
    if test_files:
        test_file = os.path.join(test_dir, test_files[0])
        print(f"\n🧪 도구 테스트: {test_file}")
        test_result = analyze_file(test_file)
        print(f"  CC: {test_result['cc_average']:.2f}, MI: {test_result['mi_score']:.2f}, "
              f"Pylint: {test_result['pylint_score']:.2f}, LOC: {test_result['lines_of_code']}")

    # 전체 분석
    print(f"\n{'='*60}")
    print("📊 전체 분석 시작...")
    print(f"{'='*60}")

    all_results = []
    total_files = 0
    errors = 0

    for i, pdir in enumerate(problem_dirs):
        num_match = re.match(r'problem_(\d+)_', pdir)
        if not num_match:
            continue
        problem_num = int(num_match.group(1))
        meta = metadata.get(problem_num, {})

        for persona in ["vibecoder", "senior"]:
            for run_num in range(1, N_RUNS + 1):
                filepath = os.path.join(CODE_DIR, pdir, f"{persona}_run{run_num}.py")
                if not os.path.exists(filepath):
                    print(f"  ⚠️ {filepath} 없음")
                    errors += 1
                    continue

                result = analyze_file(filepath)
                result["filepath"] = filepath
                result["persona"] = persona
                result["problem_num"] = problem_num
                result["run_num"] = run_num
                result["leetcode_id"] = meta.get("leetcode_id", "")
                result["title"] = meta.get("title", "")
                result["difficulty"] = meta.get("difficulty", "")
                result["category"] = meta.get("category", "")

                all_results.append(result)
                total_files += 1

        if (i + 1) % 10 == 0 or i == len(problem_dirs) - 1:
            print(f"  [{i+1}/{len(problem_dirs)}] 완료 (파일: {total_files})")

    # ============================================================
    # Cell 5: Raw 결과 저장
    # ============================================================

    fieldnames = [
        "filepath", "persona", "problem_num", "run_num",
        "leetcode_id", "title", "difficulty", "category",
        "cc_average", "cc_max", "cc_total", "cc_blocks",
        "mi_score", "mi_rank",
        "hal_vocabulary", "hal_length", "hal_volume", "hal_difficulty",
        "hal_effort", "hal_time", "hal_bugs",
        "pylint_score", "pylint_convention", "pylint_refactor",
        "pylint_warning", "pylint_error", "pylint_total_issues",
        "bandit_high", "bandit_medium", "bandit_low", "bandit_total",
        "bandit_confidence_high",
        "lines_of_code", "blank_lines", "comment_lines",
        "has_docstring", "has_type_hints",
    ]

    with open(OUTPUT_RAW, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in all_results:
            writer.writerow({k: r.get(k, "") for k in fieldnames})

    print(f"\n✅ Raw 결과 저장: {OUTPUT_RAW} ({len(all_results)}행)")

    # ============================================================
    # Cell 6: Median 대표값 산출
    # ============================================================

    numeric_keys = [
        "cc_average", "cc_max", "cc_total", "cc_blocks",
        "mi_score",
        "hal_vocabulary", "hal_length", "hal_volume", "hal_difficulty",
        "hal_effort", "hal_time", "hal_bugs",
        "pylint_score", "pylint_convention", "pylint_refactor",
        "pylint_warning", "pylint_error", "pylint_total_issues",
        "bandit_high", "bandit_medium", "bandit_low", "bandit_total",
        "bandit_confidence_high",
        "lines_of_code", "blank_lines", "comment_lines",
    ]

    boolean_keys = ["has_docstring", "has_type_hints"]

    # 문제 × 페르소나별 그룹핑
    groups = defaultdict(list)
    for r in all_results:
        key = (r["problem_num"], r["persona"])
        groups[key].append(r)

    median_results = []
    variability_data = []  # intra-persona variability 기록

    for (problem_num, persona), runs in sorted(groups.items()):
        if len(runs) != N_RUNS:
            print(f"  ⚠️ Problem {problem_num} {persona}: {len(runs)} runs (expected {N_RUNS})")

        median_row = {
            "persona": persona,
            "problem_num": problem_num,
            "leetcode_id": runs[0]["leetcode_id"],
            "title": runs[0]["title"],
            "difficulty": runs[0]["difficulty"],
            "category": runs[0]["category"],
        }

        # 수치 지표: median
        for key in numeric_keys:
            values = [float(r[key]) for r in runs]
            median_row[key] = statistics.median(values)

            # MI에 대해 variability 기록
            if key == "mi_score":
                variability_data.append({
                    "problem_num": problem_num,
                    "persona": persona,
                    "mi_median": statistics.median(values),
                    "mi_mean": statistics.mean(values),
                    "mi_std": statistics.stdev(values) if len(values) > 1 else 0,
                    "mi_min": min(values),
                    "mi_max": max(values),
                    "mi_range": max(values) - min(values),
                })

        # Boolean 지표: majority vote (3/5 이상이면 True)
        for key in boolean_keys:
            true_count = sum(1 for r in runs if str(r[key]).lower() == "true")
            median_row[key] = true_count >= (N_RUNS // 2 + 1)

        # MI rank: median MI 기반 재계산
        mi = median_row["mi_score"]
        if mi > 19:
            median_row["mi_rank"] = "A"
        elif mi > 9:
            median_row["mi_rank"] = "B"
        else:
            median_row["mi_rank"] = "C"

        median_results.append(median_row)

    # Median 결과 저장
    median_fieldnames = [
        "persona", "problem_num", "leetcode_id", "title", "difficulty", "category",
    ] + numeric_keys + ["mi_rank"] + boolean_keys

    with open(OUTPUT_MEDIAN, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=median_fieldnames)
        writer.writeheader()
        for r in median_results:
            writer.writerow({k: r.get(k, "") for k in median_fieldnames})

    print(f"✅ Median 결과 저장: {OUTPUT_MEDIAN} ({len(median_results)}행)")

    # Variability 보고서 저장
    var_path = "intra_persona_variability.csv"
    with open(var_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "problem_num", "persona", "mi_median", "mi_mean", "mi_std",
            "mi_min", "mi_max", "mi_range"
        ])
        writer.writeheader()
        writer.writerows(variability_data)

    print(f"✅ Variability 보고서 저장: {var_path}")

    # ============================================================
    # Cell 7: 요약 통계 출력
    # ============================================================

    print(f"\n{'='*60}")
    print("📊 Median 기반 요약 통계")
    print(f"{'='*60}")

    vibe = [r for r in median_results if r["persona"] == "vibecoder"]
    senior = [r for r in median_results if r["persona"] == "senior"]

    def mean(lst): return sum(lst) / len(lst) if lst else 0
    def std(lst):
        if len(lst) < 2: return 0
        m = mean(lst)
        return (sum((x - m)**2 for x in lst) / (len(lst) - 1)) ** 0.5

    key_metrics = [
        ("MI Score", "mi_score"),
        ("CC Average", "cc_average"),
        ("Halstead Effort", "hal_effort"),
        ("Pylint Score", "pylint_score"),
        ("LOC", "lines_of_code"),
        ("Comment Lines", "comment_lines"),
        ("Bandit Total", "bandit_total"),
    ]

    print(f"\n{'Metric':<25} {'Vibecoder':>18} {'Senior':>18}")
    print("-" * 61)
    for name, key in key_metrics:
        v = [r[key] for r in vibe]
        s = [r[key] for r in senior]
        print(f"{name:<25} {mean(v):>7.2f} ± {std(v):<7.2f} {mean(s):>7.2f} ± {std(s):<7.2f}")

    # Intra-persona variability 요약
    print(f"\n{'='*60}")
    print("📊 Intra-Persona MI Variability (n=5 runs)")
    print(f"{'='*60}")

    for persona in ["vibecoder", "senior"]:
        var_data = [v for v in variability_data if v["persona"] == persona]
        avg_std = mean([v["mi_std"] for v in var_data])
        avg_range = mean([v["mi_range"] for v in var_data])
        max_range = max(v["mi_range"] for v in var_data)
        print(f"  {persona}: avg_std={avg_std:.2f}, avg_range={avg_range:.2f}, max_range={max_range:.2f}")

    print(f"\n🎉 분석 파이프라인 완료!")
    print(f"  다음 단계: python notebook3_statistical_analysis.py")


if __name__ == "__main__":
    main()
