from model import MATRIX, QUESTIONS, ALPHABET
from text_processing import process_text
from data_manager import TruncatedMatrix
import numpy as np
from scipy import sparse
from dataclasses import dataclass


@dataclass
class QueryResult:
    url: str
    description: str
    metric: float


def k_best_vectors(vector: sparse.csr_matrix, k: int):
    best_values = np.sort(vector.todense(), axis=1)[:, ::-1]
    best_indices = np.argsort(vector.todense(), axis=1)[:, ::-1]
    return [(best_indices[0, i], best_values[0, i]) for i in range(k)]


def convert_to_dense(query):
    data = np.array([0 for _ in range(len(ALPHABET))], dtype=float)
    for w in query:
        data[ALPHABET[w]] = query[w]
    return data


def find_closest_vectors_svd(query, svd: TruncatedMatrix, k: int):
    dense_query = convert_to_dense(query)
    best = np.abs(((dense_query @ svd.U_S) @ svd.V) / svd.vector_lengths)
    return list(zip(np.argsort(best)[::-1][:k], np.sort(best)[::-1][:k]))


def search_query(query: str) -> list[QueryResult]:
    query_vector = process_text(query)
    res = find_closest_vectors_svd(query_vector, MATRIX, 20)
    base_url = "https://stackoverflow.com/questions/"

    results: list[QueryResult] = []

    for i, (ind, angle) in enumerate(res):
        results.append(
            QueryResult(
                f"{base_url}{QUESTIONS[ind].id}",
                QUESTIONS[ind].title,
                angle
            )
        )

    return results

