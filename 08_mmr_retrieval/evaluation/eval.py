from config import get_settings
from diversity import calculate_diversity, document_overlap
from retrieval import compare_retrieval
from evaluation.questions import EVALUATION_CASES

def main() -> None:
    settings = get_settings()
    for index, query in enumerate(EVALUATION_CASES, start=1):
        comparison = compare_retrieval(settings=settings, query=query)
        similarity_stats = calculate_diversity(comparison.similarity)
        mmr_stats = calculate_diversity(comparison.mmr)

        print("=" * 80)
        print(f"Case {index}")
        print(f"Query: {query}")
        print(f"Similarity IDs: {list(similarity_stats.document_ids)}")
        print(f"MMR IDs: {list(mmr_stats.document_ids)}")
        print(f"Similarity types: {similarity_stats.unique_document_types}")
        print(f"MMR types: {mmr_stats.unique_document_types}")
        print(f"Similarity departments: {similarity_stats.unique_departments}")
        print(f"MMR departments: {mmr_stats.unique_departments}")
        print(
            f"Document overlap: "
            f"{document_overlap(comparison.similarity, comparison.mmr)}"
        )
        print(f"lambda_mult: {comparison.lambda_mult}")

if __name__ == "__main__":
    main()
