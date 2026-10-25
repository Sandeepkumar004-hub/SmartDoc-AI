
import json
from pathlib import Path

from backend.hybrid_search import HybridSearch


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "tests" / "evaluation_dataset.json"

SAMPLE_CHUNKS = [
    {
        "chunk_id": 1,
        "page_number": 1,
        "text": (
            "React and Node.js are used to build "
            "full-stack web applications."
        ),
    },
    {
        "chunk_id": 2,
        "page_number": 2,
        "text": (
            "SQL is useful for analyzing sales data "
            "and business performance."
        ),
    },
    {
        "chunk_id": 3,
        "page_number": 3,
        "text": (
            "Seismic waves help researchers study "
            "earthquakes and ground motion."
        ),
    },
]


def recall_at_k(
    results: list[dict],
    relevant_ids: list[int],
    k: int,
) -> float:
    """Calculate the fraction of relevant chunks found in top K."""
    if not relevant_ids:
        return 0.0

    retrieved_ids = {
        result["chunk_id"] for result in results[:k]
    }
    found = retrieved_ids.intersection(relevant_ids)

    return len(found) / len(set(relevant_ids))


def reciprocal_rank(
    results: list[dict],
    relevant_ids: list[int],
) -> float:
    """Return the reciprocal rank of the first relevant result."""
    relevant_set = set(relevant_ids)

    for rank, result in enumerate(results, start=1):
        if result["chunk_id"] in relevant_set:
            return 1.0 / rank

    return 0.0


def main() -> None:
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    search = HybridSearch()
    search.build_index(SAMPLE_CHUNKS)

    recall_scores = []
    reciprocal_ranks = []

    print("\nSmartDoc AI — Retrieval Evaluation")
    print("=" * 45)

    for item in dataset:
        query = item["query"]
        relevant_ids = item["relevant_chunk_ids"]

        results = search.search(query, top_k=3)

        recall = recall_at_k(results, relevant_ids, k=3)
        mrr = reciprocal_rank(results, relevant_ids)

        recall_scores.append(recall)
        reciprocal_ranks.append(mrr)

        ranked_ids = [
            result["chunk_id"] for result in results
        ]

        print(f"\nQuery: {query}")
        print(f"Relevant chunk IDs: {relevant_ids}")
        print(f"Retrieved chunk IDs: {ranked_ids}")
        print(f"Recall@3: {recall:.3f}")
        print(f"Reciprocal Rank: {mrr:.3f}")

    mean_recall = sum(recall_scores) / len(recall_scores)
    mean_mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print("\n" + "=" * 45)
    print(f"Mean Recall@3: {mean_recall:.3f}")
    print(f"Mean Reciprocal Rank (MRR): {mean_mrr:.3f}")


if __name__ == "__main__":
    main()
