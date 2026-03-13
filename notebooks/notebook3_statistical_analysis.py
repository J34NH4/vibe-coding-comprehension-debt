"""
================================================================================
ESWA 실험: n=5 통계 분석 + 시각화 (Notebook 3/3)
================================================================================
analysis_results_n5_median.csv → 통계 검정 + 그래프

보강 분석 포함:
  1. Shapiro-Wilk 정규성 검정
  2. Paired t-test + Wilcoxon signed-rank (병행)
  3. Cohen's d + matched-pairs rank-biserial correlation
  4. Benjamini-Hochberg 다중비교 보정
  5. Bootstrap 95% CI for Cohen's d
  6. 난이도별/카테고리별 하위그룹 분석

사용법 (Colab):
  1. !pip install scipy matplotlib numpy
  2. Notebook 2 실행 완료 후 이 스크립트 실행
  3. !python notebook3_statistical_analysis.py
================================================================================
"""

import csv
import math
import os
import warnings
import json
from collections import defaultdict

# scipy 사용 (Colab에는 기본 설치됨)
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

warnings.filterwarnings('ignore')

# ============================================================
# Cell 1: 데이터 로드
# ============================================================

INPUT_FILE = "analysis_results_n5_median.csv"

def load_data(filepath=INPUT_FILE):
    """Median 기반 데이터 로드"""
    vibe, senior = [], []
    with open(filepath, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in row:
                if key not in ("filepath", "persona", "title", "difficulty",
                               "category", "mi_rank"):
                    try:
                        row[key] = float(row[key]) if "." in str(row[key]) else int(row[key])
                    except (ValueError, TypeError):
                        pass
            row["has_docstring"] = str(row.get("has_docstring", "")).lower() == "true"
            row["has_type_hints"] = str(row.get("has_type_hints", "")).lower() == "true"

            if row["persona"] == "vibecoder":
                vibe.append(row)
            elif row["persona"] == "senior":
                senior.append(row)

    # 문제 번호 기준 정렬 (paired test를 위해)
    vibe.sort(key=lambda x: x["problem_num"])
    senior.sort(key=lambda x: x["problem_num"])

    assert len(vibe) == len(senior), f"쌍 불일치: vibe={len(vibe)}, senior={len(senior)}"
    return vibe, senior


# ============================================================
# Cell 2: 통계 함수
# ============================================================

def cohens_d_paired(x, y):
    """Cohen's d (paired samples)"""
    diffs = np.array(x) - np.array(y)
    return np.mean(diffs) / np.std(diffs, ddof=1) if np.std(diffs, ddof=1) > 0 else 0

def rank_biserial_matched(x, y):
    """Matched-pairs rank-biserial correlation (Kerby, 2014)"""
    diffs = np.array(x) - np.array(y)
    diffs = diffs[diffs != 0]  # 0 차이 제거
    if len(diffs) == 0:
        return 0
    ranks = stats.rankdata(np.abs(diffs))
    r_plus = np.sum(ranks[diffs > 0])
    r_minus = np.sum(ranks[diffs < 0])
    n = len(diffs)
    rc = (r_plus - r_minus) / (n * (n + 1) / 2)
    return rc

def bootstrap_ci_cohens_d(x, y, n_bootstrap=10000, ci=0.95, seed=42):
    """Bootstrap 95% CI for Cohen's d"""
    rng = np.random.RandomState(seed)
    x, y = np.array(x), np.array(y)
    n = len(x)
    d_samples = []

    for _ in range(n_bootstrap):
        idx = rng.randint(0, n, size=n)
        d = cohens_d_paired(x[idx], y[idx])
        d_samples.append(d)

    alpha = 1 - ci
    lower = np.percentile(d_samples, alpha / 2 * 100)
    upper = np.percentile(d_samples, (1 - alpha / 2) * 100)
    return lower, upper

def benjamini_hochberg(p_values):
    """Benjamini-Hochberg FDR 보정"""
    n = len(p_values)
    if n == 0:
        return []
    indexed = [(p, i) for i, p in enumerate(p_values) if p is not None]
    indexed.sort()
    adjusted = [None] * n

    prev = 1.0
    for rank, (p, orig_idx) in enumerate(reversed(indexed), 1):
        adj_p = min(p * len(indexed) / (len(indexed) - rank + 1), prev)
        adj_p = min(adj_p, 1.0)
        adjusted[orig_idx] = adj_p
        prev = adj_p

    return adjusted

def effect_size_label(d):
    d = abs(d)
    if d < 0.2: return "negligible"
    elif d < 0.5: return "small"
    elif d < 0.8: return "medium"
    elif d < 1.2: return "large"
    return "very large"

def rc_effect_label(rc):
    """Rank-biserial effect size label (Vargha & Delaney thresholds)"""
    rc = abs(rc)
    if rc < 0.11: return "negligible"
    elif rc < 0.28: return "small"
    elif rc < 0.43: return "medium"
    return "large"

def sig_stars(p):
    if p is None: return "n.s."
    if p < 0.001: return "***"
    elif p < 0.01: return "**"
    elif p < 0.05: return "*"
    return "n.s."


# ============================================================
# Cell 3: 메인 통계 분석
# ============================================================

def main():
    print(f"{'='*80}")
    print("📊 ESWA n=5 통계 분석 (Median 기반)")
    print(f"{'='*80}")

    vibe, senior = load_data()
    n = len(vibe)
    print(f"데이터: {n}쌍 (Vibecoder vs Senior)")

    # ============================================================
    # 3.1 정규성 검정
    # ============================================================
    print(f"\n{'='*60}")
    print("1️⃣ Shapiro-Wilk 정규성 검정 (차이값 D = Vibe - Senior)")
    print(f"{'='*60}")

    metrics_to_test = [
        ("Cyclomatic Complexity", "cc_average"),
        ("Maintainability Index", "mi_score"),
        ("Halstead Volume", "hal_volume"),
        ("Halstead Difficulty", "hal_difficulty"),
        ("Halstead Effort", "hal_effort"),
        ("Halstead Bugs", "hal_bugs"),
        ("Pylint Score", "pylint_score"),
        ("Pylint Total Issues", "pylint_total_issues"),
        ("Lines of Code", "lines_of_code"),
        ("Comment Lines", "comment_lines"),
        ("Bandit Total", "bandit_total"),
    ]

    normality_results = {}
    print(f"\n{'Metric':<30} {'W':>8} {'p':>10} {'Normal?':>10}")
    print("-" * 60)

    for name, key in metrics_to_test:
        v_vals = np.array([float(r[key]) for r in vibe])
        s_vals = np.array([float(r[key]) for r in senior])
        diffs = v_vals - s_vals

        # 모든 값이 동일하면 검정 불가
        if np.std(diffs) == 0:
            normality_results[key] = {"W": None, "p": None, "normal": None}
            print(f"{name:<30} {'N/A':>8} {'N/A':>10} {'(no var)':>10}")
            continue

        W, p = stats.shapiro(diffs)
        is_normal = p > 0.05
        normality_results[key] = {"W": W, "p": p, "normal": is_normal}
        print(f"{name:<30} {W:>8.4f} {p:>10.4f} {'✅ Yes' if is_normal else '❌ No':>10}")

    # ============================================================
    # 3.2 주요 통계 검정 (Paired t-test + Wilcoxon 병행)
    # ============================================================
    print(f"\n{'='*80}")
    print("2️⃣ 통계 검정 (Paired t-test + Wilcoxon signed-rank)")
    print(f"{'='*80}")

    stat_results = []
    all_p_values_t = []
    all_p_values_w = []

    header = (f"{'Metric':<25} {'Vibe M±SD':>14} {'Senior M±SD':>14} "
              f"{'t':>7} {'p(t)':>9} {'W':>7} {'p(W)':>9} {'d':>7} {'rc':>7} {'Sig':>5}")
    print(f"\n{header}")
    print("=" * len(header))

    for name, key in metrics_to_test:
        v_vals = np.array([float(r[key]) for r in vibe])
        s_vals = np.array([float(r[key]) for r in senior])

        v_m, v_s = np.mean(v_vals), np.std(v_vals, ddof=1)
        s_m, s_s = np.mean(s_vals), np.std(s_vals, ddof=1)

        # Paired t-test
        if np.std(v_vals - s_vals) > 0:
            t_stat, p_t = stats.ttest_rel(v_vals, s_vals)
        else:
            t_stat, p_t = None, None

        # Wilcoxon signed-rank
        diffs = v_vals - s_vals
        non_zero_diffs = diffs[diffs != 0]
        if len(non_zero_diffs) >= 10:
            w_stat, p_w = stats.wilcoxon(non_zero_diffs)
        else:
            w_stat, p_w = None, None

        # Effect sizes
        d = cohens_d_paired(v_vals, s_vals)
        rc = rank_biserial_matched(v_vals, s_vals)

        # Bootstrap CI
        if np.std(v_vals - s_vals) > 0:
            ci_low, ci_high = bootstrap_ci_cohens_d(v_vals, s_vals)
        else:
            ci_low, ci_high = 0, 0

        # 유의성: 정규성 결과에 따라 primary test 선택
        norm = normality_results.get(key, {})
        if norm.get("normal") is True:
            primary_p = p_t
            primary_test = "t-test"
        elif norm.get("normal") is False:
            primary_p = p_w if p_w is not None else p_t
            primary_test = "Wilcoxon" if p_w is not None else "t-test"
        else:
            primary_p = p_t
            primary_test = "t-test"

        sig = sig_stars(primary_p)

        all_p_values_t.append(p_t)
        all_p_values_w.append(p_w)

        v_str = f"{v_m:.2f}±{v_s:.2f}"
        s_str = f"{s_m:.2f}±{s_s:.2f}"
        t_str = f"{t_stat:.3f}" if t_stat is not None else "N/A"
        pt_str = f"{p_t:.6f}" if p_t is not None else "N/A"
        w_str = f"{w_stat:.0f}" if w_stat is not None else "N/A"
        pw_str = f"{p_w:.6f}" if p_w is not None else "N/A"

        print(f"{name:<25} {v_str:>14} {s_str:>14} {t_str:>7} {pt_str:>9} "
              f"{w_str:>7} {pw_str:>9} {d:>7.3f} {rc:>7.3f} {sig:>5}")

        stat_results.append({
            "Metric": name, "Key": key,
            "Vibe_Mean": v_m, "Vibe_SD": v_s,
            "Senior_Mean": s_m, "Senior_SD": s_s,
            "t_stat": t_stat, "p_ttest": p_t,
            "W_stat": w_stat, "p_wilcoxon": p_w,
            "Cohens_d": d, "d_CI_low": ci_low, "d_CI_high": ci_high,
            "rank_biserial_rc": rc,
            "d_effect": effect_size_label(d),
            "rc_effect": rc_effect_label(rc),
            "primary_test": primary_test,
            "primary_p": primary_p,
            "Significance": sig,
        })

    # ============================================================
    # 3.3 Benjamini-Hochberg 다중비교 보정
    # ============================================================
    print(f"\n{'='*60}")
    print("3️⃣ Benjamini-Hochberg FDR 보정")
    print(f"{'='*60}")

    primary_ps = [sr["primary_p"] for sr in stat_results]
    adjusted_ps = benjamini_hochberg(primary_ps)

    print(f"\n{'Metric':<30} {'Raw p':>12} {'BH adj. p':>12} {'Sig (adj)':>10}")
    print("-" * 66)
    for i, sr in enumerate(stat_results):
        raw_p = sr["primary_p"]
        adj_p = adjusted_ps[i]
        sr["p_adjusted_BH"] = adj_p
        sr["Sig_adjusted"] = sig_stars(adj_p) if adj_p is not None else "n.s."

        raw_str = f"{raw_p:.6f}" if raw_p is not None else "N/A"
        adj_str = f"{adj_p:.6f}" if adj_p is not None else "N/A"
        print(f"{sr['Metric']:<30} {raw_str:>12} {adj_str:>12} {sr['Sig_adjusted']:>10}")

    # ============================================================
    # 3.4 Bootstrap CI 출력
    # ============================================================
    print(f"\n{'='*60}")
    print("4️⃣ Cohen's d + Bootstrap 95% CI")
    print(f"{'='*60}")

    print(f"\n{'Metric':<30} {'d':>8} {'95% CI':>20} {'Effect':>12}")
    print("-" * 72)
    for sr in stat_results:
        ci_str = f"[{sr['d_CI_low']:.3f}, {sr['d_CI_high']:.3f}]"
        print(f"{sr['Metric']:<30} {sr['Cohens_d']:>8.3f} {ci_str:>20} {sr['d_effect']:>12}")

    # ============================================================
    # 3.5 Boolean 지표
    # ============================================================
    print(f"\n{'='*60}")
    print("5️⃣ 문서화 지표 (Boolean)")
    print(f"{'='*60}")

    v_doc = sum(1 for r in vibe if r["has_docstring"])
    s_doc = sum(1 for r in senior if r["has_docstring"])
    v_hint = sum(1 for r in vibe if r["has_type_hints"])
    s_hint = sum(1 for r in senior if r["has_type_hints"])

    print(f"  Docstring:  Vibe {v_doc}/{n} ({v_doc/n*100:.1f}%)  Senior {s_doc}/{n} ({s_doc/n*100:.1f}%)")
    print(f"  Type Hints: Vibe {v_hint}/{n} ({v_hint/n*100:.1f}%)  Senior {s_hint}/{n} ({s_hint/n*100:.1f}%)")

    # ============================================================
    # 3.6 난이도별 분석
    # ============================================================
    print(f"\n{'='*60}")
    print("6️⃣ 난이도별 MI 비교")
    print(f"{'='*60}")

    for diff in ["Medium", "Hard"]:
        v_mi = np.array([float(r["mi_score"]) for r in vibe if r["difficulty"] == diff])
        s_mi = np.array([float(r["mi_score"]) for r in senior if r["difficulty"] == diff])
        if len(v_mi) >= 3:
            t, p_t = stats.ttest_rel(v_mi, s_mi)
            d = cohens_d_paired(v_mi, s_mi)
            ci_low, ci_high = bootstrap_ci_cohens_d(v_mi, s_mi)
            print(f"  {diff} (n={len(v_mi)}): Vibe {np.mean(v_mi):.2f}±{np.std(v_mi, ddof=1):.2f}, "
                  f"Senior {np.mean(s_mi):.2f}±{np.std(s_mi, ddof=1):.2f}")
            print(f"    d={d:.3f} [{ci_low:.3f}, {ci_high:.3f}] {sig_stars(p_t)}")

    # ============================================================
    # 3.7 카테고리별 분석
    # ============================================================
    print(f"\n{'='*60}")
    print("7️⃣ 카테고리별 MI 비교")
    print(f"{'='*60}")

    categories = sorted(set(r["category"] for r in vibe))
    for cat in categories:
        v_mi = np.array([float(r["mi_score"]) for r in vibe if r["category"] == cat])
        s_mi = np.array([float(r["mi_score"]) for r in senior if r["category"] == cat])
        if len(v_mi) >= 3:
            t, p_t = stats.ttest_rel(v_mi, s_mi)
            d = cohens_d_paired(v_mi, s_mi)
            print(f"  {cat} (n={len(v_mi)}): d={d:.3f} {sig_stars(p_t)}")

    # ============================================================
    # 3.8 Pylint Density 분석
    # ============================================================
    print(f"\n{'='*60}")
    print("8️⃣ Pylint Density (issues/LOC)")
    print(f"{'='*60}")

    v_density = []
    s_density = []
    for v, s in zip(vibe, senior):
        v_loc = float(v["lines_of_code"])
        s_loc = float(s["lines_of_code"])
        v_issues = float(v["pylint_total_issues"])
        s_issues = float(s["pylint_total_issues"])
        if v_loc > 0 and s_loc > 0:
            v_density.append(v_issues / v_loc)
            s_density.append(s_issues / s_loc)

    v_d = np.array(v_density)
    s_d = np.array(s_density)
    t, p_t = stats.ttest_rel(v_d, s_d)
    d = cohens_d_paired(v_d, s_d)
    ci_low, ci_high = bootstrap_ci_cohens_d(v_d, s_d)
    print(f"  Vibe: {np.mean(v_d):.3f}±{np.std(v_d, ddof=1):.3f} issues/LOC")
    print(f"  Senior: {np.mean(s_d):.3f}±{np.std(s_d, ddof=1):.3f} issues/LOC")
    print(f"  Vibe/Senior ratio: {np.mean(v_d)/np.mean(s_d):.1f}x")
    print(f"  d={d:.3f} [{ci_low:.3f}, {ci_high:.3f}] {sig_stars(p_t)}")

    # ============================================================
    # Cell 4: CSV 결과 저장
    # ============================================================

    # statistical_results_n5.csv
    stat_fieldnames = [
        "Metric", "Key", "Vibe_Mean", "Vibe_SD", "Senior_Mean", "Senior_SD",
        "t_stat", "p_ttest", "W_stat", "p_wilcoxon",
        "Cohens_d", "d_CI_low", "d_CI_high", "rank_biserial_rc",
        "d_effect", "rc_effect", "primary_test", "primary_p",
        "p_adjusted_BH", "Significance", "Sig_adjusted",
    ]

    with open("statistical_results_n5.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=stat_fieldnames)
        writer.writeheader()
        for sr in stat_results:
            row = {k: sr.get(k, "") for k in stat_fieldnames}
            for k in row:
                if isinstance(row[k], float):
                    row[k] = f"{row[k]:.6f}" if "p_" in k or k == "p_adjusted_BH" else f"{row[k]:.4f}"
            writer.writerow(row)
    print(f"\n✅ statistical_results_n5.csv 저장")

    # summary_table_n5.csv (논문용 간결 테이블)
    with open("summary_table_n5.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Metric", "Vibecoder (M ± SD)", "Senior (M ± SD)",
                     "t", "p (t-test)", "W", "p (Wilcoxon)",
                     "Cohen's d", "95% CI", "BH adj. p", "Sig."])
        for sr in stat_results:
            w.writerow([
                sr["Metric"],
                f"{sr['Vibe_Mean']:.2f} ± {sr['Vibe_SD']:.2f}",
                f"{sr['Senior_Mean']:.2f} ± {sr['Senior_SD']:.2f}",
                f"{sr['t_stat']:.3f}" if sr['t_stat'] is not None else "N/A",
                f"{sr['p_ttest']:.4f}" if sr['p_ttest'] is not None else "N/A",
                f"{sr['W_stat']:.0f}" if sr['W_stat'] is not None else "N/A",
                f"{sr['p_wilcoxon']:.4f}" if sr['p_wilcoxon'] is not None else "N/A",
                f"{sr['Cohens_d']:.3f}",
                f"[{sr['d_CI_low']:.3f}, {sr['d_CI_high']:.3f}]",
                f"{sr['p_adjusted_BH']:.4f}" if sr['p_adjusted_BH'] is not None else "N/A",
                sr["Sig_adjusted"],
            ])
    print(f"✅ summary_table_n5.csv 저장")

    # ============================================================
    # Cell 5: 시각화
    # ============================================================

    print(f"\n{'='*60}")
    print("📊 시각화 생성 중...")
    print(f"{'='*60}")

    generate_all_plots(vibe, senior, stat_results)

    print(f"\n🎉 전체 통계 분석 + 시각화 완료!")


# ============================================================
# Cell 5: 시각화 함수들
# ============================================================

def generate_all_plots(vibe, senior, stat_results):
    """모든 그래프 생성"""
    n = len(vibe)
    colors = ['#FF6B6B', '#4ECDC4']

    # --- Figure 1: 주요 4개 지표 비교 Boxplot ---
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Comparison of Maintainability Metrics:\nVibecoder vs Senior Developer (n=47, median of 5 runs)",
                 fontsize=14, fontweight='bold')

    box_metrics = [
        ("Cyclomatic Complexity (Avg)", "cc_average", None),
        ("Maintainability Index", "mi_score", 65),
        ("Halstead Effort", "hal_effort", None),
        ("Pylint Score (0-10)", "pylint_score", None),
    ]

    for idx, (title, key, threshold) in enumerate(box_metrics):
        ax = axes[idx // 2][idx % 2]
        v_data = [float(r[key]) for r in vibe]
        s_data = [float(r[key]) for r in senior]

        bp = ax.boxplot([v_data, s_data], labels=["Vibecoder", "Senior"],
                       patch_artist=True, widths=0.6)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        for median in bp['medians']:
            median.set(color='#333333', linewidth=2)

        # 효과크기 표시
        sr = next((s for s in stat_results if s["Key"] == key), None)
        if sr:
            d_str = f"d={sr['Cohens_d']:.2f} {sr['Sig_adjusted']}"
            ax.text(0.02, 0.98, d_str, transform=ax.transAxes, fontsize=9,
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)

        if threshold:
            ax.axhline(y=threshold, color='#FFA500', linestyle='--', alpha=0.7,
                       label=f'Threshold ({threshold})')
            ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig("comparison_plots_n5.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✅ comparison_plots_n5.png")

    # --- Figure 2: 문서화 부채 ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle("Documentation Debt: Vibecoder vs Senior (n=47)", fontsize=14, fontweight='bold')

    v_doc = sum(1 for r in vibe if r["has_docstring"]) / n * 100
    s_doc = sum(1 for r in senior if r["has_docstring"]) / n * 100
    v_hint = sum(1 for r in vibe if r["has_type_hints"]) / n * 100
    s_hint = sum(1 for r in senior if r["has_type_hints"]) / n * 100

    bars1 = ax1.bar(["Vibecoder", "Senior"], [v_doc, s_doc], color=colors, width=0.5)
    ax1.set_title("Docstring Presence Rate", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Percentage (%)")
    ax1.set_ylim(0, 115)
    for bar, val in zip(bars1, [v_doc, s_doc]):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}%', ha='center', fontsize=12, fontweight='bold')

    bars2 = ax2.bar(["Vibecoder", "Senior"], [v_hint, s_hint], color=colors, width=0.5)
    ax2.set_title("Type Hints Presence Rate", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Percentage (%)")
    ax2.set_ylim(0, 115)
    for bar, val in zip(bars2, [v_hint, s_hint]):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}%', ha='center', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig("documentation_debt_n5.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✅ documentation_debt_n5.png")

    # --- Figure 3: 카테고리별 MI ---
    categories = sorted(set(r["category"] for r in vibe))
    v_means = [np.mean([float(r["mi_score"]) for r in vibe if r["category"] == c]) for c in categories]
    s_means = [np.mean([float(r["mi_score"]) for r in senior if r["category"] == c]) for c in categories]

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(categories))
    width = 0.35
    ax.bar(x - width/2, v_means, width, label='Vibecoder', color=colors[0], alpha=0.8)
    ax.bar(x + width/2, s_means, width, label='Senior', color=colors[1], alpha=0.8)
    ax.axhline(y=65, color='#FFA500', linestyle='--', alpha=0.7, label='MI Threshold (65)')
    ax.set_xlabel('Problem Category', fontsize=12)
    ax.set_ylabel('Maintainability Index (median of 5 runs)', fontsize=12)
    ax.set_title('MI by Problem Category (n=47)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig("category_comparison_n5.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✅ category_comparison_n5.png")

    # --- Figure 4: Halstead 상세 ---
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Halstead Metrics Comparison (n=47)", fontsize=14, fontweight='bold')
    for idx, (title, key) in enumerate([("Volume", "hal_volume"), ("Difficulty", "hal_difficulty"), ("Effort", "hal_effort")]):
        ax = axes[idx]
        v_data = [float(r[key]) for r in vibe]
        s_data = [float(r[key]) for r in senior]
        bp = ax.boxplot([v_data, s_data], labels=["Vibecoder", "Senior"], patch_artist=True, widths=0.6)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color); patch.set_alpha(0.7)
        for median in bp['medians']:
            median.set(color='#333333', linewidth=2)
        ax.set_title(f"Halstead {title}", fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig("halstead_comparison_n5.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✅ halstead_comparison_n5.png")

    # --- Figure 5: Pylint 경고 유형별 ---
    fig, ax = plt.subplots(figsize=(10, 6))
    issue_types = ["Convention", "Refactor", "Warning", "Error"]
    v_counts = [sum(int(r[f"pylint_{t.lower()}"]) for r in vibe) for t in issue_types]
    s_counts = [sum(int(r[f"pylint_{t.lower()}"]) for r in senior) for t in issue_types]

    x = np.arange(len(issue_types))
    width = 0.35
    bars1 = ax.bar(x - width/2, v_counts, width, label='Vibecoder', color=colors[0], alpha=0.8)
    bars2 = ax.bar(x + width/2, s_counts, width, label='Senior', color=colors[1], alpha=0.8)
    ax.set_xlabel('Issue Type', fontsize=12)
    ax.set_ylabel('Total Count', fontsize=12)
    ax.set_title('Pylint Issues by Type (n=47)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(issue_types)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, str(int(h)), ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig("pylint_breakdown_n5.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✅ pylint_breakdown_n5.png")

    # --- Figure 6 (NEW): Effect Size Forest Plot ---
    fig, ax = plt.subplots(figsize=(10, 6))
    metric_names = [sr["Metric"] for sr in stat_results if sr["Cohens_d"] != 0 or sr["d_CI_low"] != 0]
    ds = [sr["Cohens_d"] for sr in stat_results if sr["Cohens_d"] != 0 or sr["d_CI_low"] != 0]
    ci_lows = [sr["d_CI_low"] for sr in stat_results if sr["Cohens_d"] != 0 or sr["d_CI_low"] != 0]
    ci_highs = [sr["d_CI_high"] for sr in stat_results if sr["Cohens_d"] != 0 or sr["d_CI_low"] != 0]

    y_pos = np.arange(len(metric_names))
    errors = [[d - cl for d, cl in zip(ds, ci_lows)],
              [ch - d for d, ch in zip(ds, ci_highs)]]

    ax.errorbar(ds, y_pos, xerr=errors, fmt='o', color='#2E75B6', capsize=5,
               markersize=8, linewidth=2, capthick=2)
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(metric_names)
    ax.set_xlabel("Cohen's d (with 95% Bootstrap CI)", fontsize=12)
    ax.set_title("Effect Size Forest Plot (Vibecoder - Senior)", fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig("effect_size_forest_n5.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✅ effect_size_forest_n5.png")


if __name__ == "__main__":
    main()
