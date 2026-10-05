import re
import json
import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import ndcg_score
from collections import defaultdict

# --- Load filtered users ---
filtered_user_ids = set()
with open("Eval/score_combined_recommendations/Users_filtered.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            user = json.loads(line)
            filtered_user_ids.add(user["User-ID"])

def extract_titles(llm_output, candidate_titles=None):
    lines = llm_output.splitlines()
    titles = []
    for line in lines:
        line = line.strip()

        # Match numbered list entries like:
        # "1. Title by Author"
        # "1) Title"
        match = re.match(r"^\s*\d+[\.\)]\s*(.+)$", line)
        if not match:
            continue

        entry = match.group(1)

        # Remove trailing author info if present
        entry = re.sub(r"\s+by\s+.*$", "", entry, flags=re.IGNORECASE)

        entry = entry.strip()

        if candidate_titles:
            # Fuzzy match: keep only if entry starts with or matches a candidate title
            for cand in candidate_titles:
                if entry.lower().startswith(cand.lower()):
                    titles.append(cand)
                    break
        else:
            titles.append(entry)

    return titles


def evaluate_record(candidate_books, llm_output, user_id, threshold=8):
    """
    Returns NDCG@5, NDCG(all), Spearman, reciprocal rank
    threshold: rating threshold to consider "relevant" for MRR
    """
    if not candidate_books:
        print(user_id)
        return None, None, None, None, None

    candidate_books = [
        b for b in candidate_books if b.get("rating", 0) > 0
    ]

    candidate_titles = [b["title"] for b in candidate_books]
    title_to_rating = {b["title"]: b.get("rating", 0) for b in candidate_books}

    # LLM predicted ranking
    pred_titles = extract_titles(llm_output, candidate_titles=candidate_titles)

    # y_true and y_score for NDCG
    max_rank = len(pred_titles)
    title_to_pred_score = {t: max_rank - i for i, t in enumerate(pred_titles)}

    y_true = [title_to_rating.get(t, 0) for t in candidate_titles]
    y_score = [title_to_pred_score.get(t, 0) for t in candidate_titles]

    y_true_arr = np.array([y_true])
    y_score_arr = np.array([y_score])

    ndcg_5 = ndcg_score(y_true_arr, y_score_arr, k=5)
    ndcg_10 = ndcg_score(y_true_arr, y_score_arr, k=10)
    ndcg_all = ndcg_score(y_true_arr, y_score_arr)

    # Spearman (only consider books with rating > 0)
    mask = np.array(y_true) > 0
    if np.sum(mask) > 1:
        spearman_corr, _ = spearmanr(np.array(y_true)[mask], np.array(y_score)[mask])
    else:
        spearman_corr = None

    # Reciprocal Rank (first book in pred_titles with rating >= threshold)
    rr = 0
    for i, t in enumerate(pred_titles, start=1):  # rank starts at 1
        if title_to_rating.get(t, 0) >= threshold:
            rr = 1 / i
            break

    return ndcg_5, ndcg_10, ndcg_all, spearman_corr, rr

with open("Eval/score_llm_recommendations/llm_only_ranking_all_users_8_results.json", "r", encoding="utf-8") as f:
    records = json.load(f)

per_model_metrics = defaultdict(lambda: {"ndcg": [], "ndcg_5": [], "ndcg_10": [], "rho": [], "rr": []})

for record in records:
    user_id = record.get("user_id")

    if user_id not in filtered_user_ids:
        continue  # skip users not in the filtered list
    candidate_books = record.get("candidate_books", [])
    ndcg_5, ndcg_10, ndcg_all, rho, rr = evaluate_record(candidate_books, record["llm_output"], user_id)

    model = record.get("model", "unknown")
    per_model_metrics[model]["ndcg"].append(ndcg_all)
    per_model_metrics[model]["ndcg_5"].append(ndcg_5)
    per_model_metrics[model]["ndcg_10"].append(ndcg_10)
    per_model_metrics[model]["rho"].append(rho)
    per_model_metrics[model]["rr"].append(rr)



print("\n=== Metrics for Highly Rate = 8 ===")
for model, metrics in per_model_metrics.items():
    ndcg_mean = np.mean(metrics["ndcg"])
    ndcg_5_mean = np.mean(metrics["ndcg_5"])
    ndcg_10_mean = np.mean(metrics["ndcg_10"])
    rho_vals = [r for r in metrics["rho"] if r is not None and not np.isnan(r)]
    rho_mean = np.mean(rho_vals) if rho_vals else None
    rr_mean = np.mean(metrics["rr"])

    print(f"\nModel: {model}")
    print("  NDCG:", ndcg_mean)
    print("  NDCG@5:", ndcg_5_mean)
    print("  NDCG@10:", ndcg_10_mean)
    print("  Spearman rho:", rho_mean)
    print("  MRR:", rr_mean)