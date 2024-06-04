from numpy.typing import NDArray
from dataclasses import dataclass
import json
import pickle


@dataclass
class Document:
    title: str
    question_id: int
    text: str


@dataclass
class Vector:
    title: str
    question_id: int
    vector: dict[str, int]


@dataclass
class Question:
    title: str
    id: int


@dataclass
class TruncatedMatrix:
    k: int
    U_S: NDArray[float]
    sigma: NDArray[float]
    V: NDArray[float]
    vector_lengths: NDArray[float]


def load_alphabet() -> dict[str, int]:
    with open("../data/alphabet.json", "r", encoding="latin-1") as f:
        alphabet = json.load(f)
    return alphabet


def load_truncated_svd(truncation_level) -> TruncatedMatrix:
    with open(f"../data/matrices/svd_matrix_{truncation_level}.pickle", "rb") as file:
        svd = pickle.load(file)
    return svd


def load_questions() -> list[Question]:
    questions: list[Question] = []
    with open("../data/questions.pickle", "rb") as f:
        while True:
            try:
                questions.append(pickle.load(f))
            except EOFError:
                break
    return questions

