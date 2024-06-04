from numpy.typing import NDArray
from dataclasses import dataclass


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

